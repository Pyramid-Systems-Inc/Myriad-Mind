# Myriad Cognitive Architecture - Monitoring & Observability Guide

This guide provides comprehensive information on monitoring, observability, and operational best practices for the Myriad Cognitive Architecture.

---

## Table of Contents

1. [Overview](#overview)
2. [Monitoring Stack](#monitoring-stack)
3. [Accessing Monitoring Tools](#accessing-monitoring-tools)
4. [Prometheus Metrics](#prometheus-metrics)
5. [Grafana Dashboards](#grafana-dashboards)
6. [Alerting](#alerting)
7. [Backup & Recovery](#backup--recovery)
8. [Troubleshooting](#troubleshooting)
9. [Performance Optimization](#performance-optimization)

---

## Overview

Myriad implements production-grade monitoring infrastructure using industry-standard tools:

- **Prometheus**: Time-series metrics collection and storage
- **Grafana**: Visualization and dashboarding
- **Redis Exporter**: Redis performance metrics
- **Custom Metrics**: Application-level metrics from all services

### Architecture

```
┌─────────────────────────────────────────────────┐
│              Grafana Dashboards                 │
│         (Visualization & Alerting)              │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│              Prometheus Server                  │
│         (Metrics Collection & Storage)          │
└─────────────────┬───────────────────────────────┘
                  │
     ┌────────────┼────────────┬──────────────┐
     │            │            │              │
┌────▼────┐  ┌───▼────┐  ┌───▼────┐   ┌────▼─────┐
│ Service │  │ Service│  │ Neo4j  │   │  Redis   │
│ Metrics │  │ Metrics│  │ Metrics│   │ Exporter │
└─────────┘  └────────┘  └────────┘   └──────────┘
```

---

## Monitoring Stack

### Components

| Component | Image | Port | Purpose |
|-----------|-------|------|---------|
| Prometheus | `prom/prometheus:latest` | 9090 | Metrics collection and storage |
| Grafana | `grafana/grafana:latest` | 3000 | Visualization and dashboards |
| Redis Exporter | `oliver006/redis_exporter:latest` | 9121 | Redis metrics exposure |
| Neo4j | `neo4j:5` (with metrics) | 2004 | Neo4j Prometheus metrics |

### Starting the Monitoring Stack

```bash
# Start all services including monitoring
docker-compose up -d

# Start only monitoring services
docker-compose up -d prometheus grafana redis-exporter

# View logs
docker-compose logs -f prometheus grafana
```

---

## Accessing Monitoring Tools

### Prometheus

**URL**: http://localhost:9090

**Default Credentials**: No authentication required (development mode)

**Common Tasks**:

1. **Query Metrics**:
   - Navigate to Graph tab
   - Enter PromQL query
   - Execute and visualize

2. **Check Targets**:
   - Status → Targets
   - Verify all endpoints are "UP"

3. **View Alerts** (when configured):
   - Alerts tab
   - Check firing alerts

### Grafana

**URL**: http://localhost:3000

**Default Credentials**:
- Username: `admin`
- Password: `myriad_admin`

**First-Time Setup**:

1. Login with default credentials
2. Navigate to Dashboards
3. Open "Myriad Cognitive Architecture - System Overview"
4. Explore available panels and metrics

**Changing Password**:

```bash
# Update password in docker-compose.yml
environment:
  - GF_SECURITY_ADMIN_PASSWORD=your_new_password

# Restart Grafana
docker-compose restart grafana
```

---

## Prometheus Metrics

### Orchestrator Service Metrics

**Endpoint**: http://localhost:5000/metrics

#### Query Metrics

```promql
# Total queries processed (by status)
orchestrator_queries_total{status="success"}
orchestrator_queries_total{status="error"}
orchestrator_queries_total{status="invalid"}

# Query rate (queries per second)
rate(orchestrator_queries_total[5m])

# Query duration (95th percentile)
histogram_quantile(0.95, rate(orchestrator_query_duration_seconds_bucket[5m]))

# Average query duration
rate(orchestrator_query_duration_seconds_sum[5m]) / rate(orchestrator_query_duration_seconds_count[5m])
```

#### Task Metrics

```promql
# Success rate
rate(orchestrator_task_success_total[5m]) / (rate(orchestrator_task_success_total[5m]) + rate(orchestrator_task_failure_total[5m]))

# Total successful tasks
orchestrator_task_success_total

# Total failed tasks
orchestrator_task_failure_total
```

#### Agent Metrics

```promql
# Number of active agents
orchestrator_active_agents

# Neurogenesis rate (new agents created per minute)
rate(orchestrator_neurogenesis_total[1m]) * 60

# Agent discovery success rate
rate(orchestrator_agent_discovery_total{status="found"}[5m]) / rate(orchestrator_agent_discovery_total[5m])
```

### Neo4j Metrics

**Endpoint**: http://localhost:2004/metrics

```promql
# Database transaction rate
rate(neo4j_database_transaction_started_total[5m])

# Query execution time
neo4j_cypher_query_execution_latency_milliseconds

# Connection pool usage
neo4j_bolt_connections_opened_total
neo4j_bolt_connections_closed_total
```

### Redis Metrics

**Endpoint**: http://localhost:9121/metrics

```promql
# Connected clients
redis_connected_clients

# Memory usage
redis_memory_used_bytes / redis_memory_max_bytes

# Commands per second
rate(redis_commands_processed_total[1m])

# Cache hit rate
rate(redis_keyspace_hits_total[5m]) / (rate(redis_keyspace_hits_total[5m]) + rate(redis_keyspace_misses_total[5m]))
```

---

## Grafana Dashboards

### System Overview Dashboard

**Panels**:

1. **Query Rate** - Queries processed per second
2. **Query Duration** - 95th and 50th percentile response times
3. **Active Agents** - Current number of registered agents
4. **Task Success Rate** - Percentage of successful task completions
5. **Neurogenesis Activity** - Dynamic agent creation rate
6. **Total Queries Processed** - Cumulative count

### Creating Custom Dashboards

1. **Navigate to Dashboards** → New Dashboard
2. **Add Panel** → Select visualization type
3. **Configure Query**:
   ```promql
   # Example: Service uptime
   up{job="orchestrator"}
   ```
4. **Customize Display**:
   - Set thresholds
   - Choose colors
   - Add units
5. **Save Dashboard**

### Importing Dashboards

The system includes pre-configured dashboards in [`monitoring/grafana/dashboards/`](../monitoring/grafana/dashboards/).

To import additional dashboards:

1. Navigate to Dashboards → Import
2. Upload JSON file or paste JSON
3. Select Prometheus data source
4. Click Import

---

## Alerting

### Prometheus Alerting Rules

Create [`monitoring/prometheus-alerts.yml`](../monitoring/prometheus-alerts.yml):

```yaml
groups:
  - name: myriad_alerts
    interval: 30s
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: rate(orchestrator_task_failure_total[5m]) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High task failure rate detected"
          description: "Task failure rate is {{ $value }} failures/sec"

      # Service down
      - alert: ServiceDown
        expr: up{job=~"orchestrator|graphdb-manager"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.job }} is down"
          description: "Service has been down for more than 2 minutes"

      # High memory usage
      - alert: HighMemoryUsage
        expr: (redis_memory_used_bytes / redis_memory_max_bytes) > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Redis memory usage is high"
          description: "Memory usage is {{ $value | humanizePercentage }}"

      # Slow queries
      - alert: SlowQueries
        expr: histogram_quantile(0.95, rate(orchestrator_query_duration_seconds_bucket[5m])) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Query processing is slow"
          description: "95th percentile query duration is {{ $value }}s"
```

Update [`monitoring/prometheus.yml`](../monitoring/prometheus.yml) to include alerts:

```yaml
rule_files:
  - 'prometheus-alerts.yml'
```

### Grafana Alerting

1. **Edit Panel** → Alert tab
2. **Create Alert Rule**:
   - Condition: `WHEN avg() OF query(A, 5m, now) IS ABOVE 0.5`
   - No Data: Set to Alerting or No Data
   - Execution Error: Set to Alerting
3. **Add Notification Channel**:
   - Email, Slack, PagerDuty, etc.
4. **Save Dashboard**

---

## Backup & Recovery

### Automated Backup

**Script**: [`scripts/backup_neo4j.sh`](../scripts/backup_neo4j.sh)

**Manual Execution**:

```bash
./scripts/backup_neo4j.sh
```

**Cron Schedule** (Daily at 2 AM):

```bash
# Edit crontab
crontab -e

# Add this line
0 2 * * * /path/to/myriad/scripts/backup_neo4j.sh >> /var/log/myriad-backup.log 2>&1
```

**Backup Location**: `./backups/neo4j/myriad_backup_YYYYMMDD_HHMMSS.tar.gz`

**Retention**: Last 7 backups kept automatically

### Restore Process

```bash
# 1. Stop Neo4j
docker-compose stop neo4j

# 2. Extract backup
cd ./backups/neo4j
tar -xzf myriad_backup_20241010_020000.tar.gz

# 3. Restore database
docker exec neo4j neo4j-admin database restore \
  --from-path=/backups/myriad_backup_20241010_020000 \
  neo4j --force

# 4. Restart Neo4j
docker-compose start neo4j

# 5. Verify restoration
curl http://localhost:7474
```

### Backup Verification

```bash
# Check backup integrity
tar -tzf myriad_backup_20241010_020000.tar.gz

# List recent backups
ls -lht ./backups/neo4j/

# Check backup size
du -h ./backups/neo4j/
```

---

## Troubleshooting

### Common Issues

#### Prometheus Not Scraping Targets

**Symptoms**: Targets show as "DOWN" in Prometheus

**Solutions**:

1. **Check service health**:
   ```bash
   curl http://localhost:5000/health
   curl http://localhost:5000/metrics
   ```

2. **Verify network connectivity**:
   ```bash
   docker-compose exec prometheus ping orchestrator
   ```

3. **Check Prometheus logs**:
   ```bash
   docker-compose logs prometheus
   ```

4. **Validate configuration**:
   ```bash
   docker-compose exec prometheus promtool check config /etc/prometheus/prometheus.yml
   ```

#### Grafana Dashboard Shows No Data

**Symptoms**: Empty panels or "No Data" messages

**Solutions**:

1. **Verify data source**:
   - Configuration → Data Sources
   - Test connection to Prometheus

2. **Check time range**: Ensure selected time range has data

3. **Validate queries**: Run queries in Prometheus first

4. **Check permissions**: Ensure Grafana can access Prometheus

#### High Memory Usage

**Symptoms**: Services crashing or slow performance

**Solutions**:

1. **Check resource usage**:
   ```bash
   docker stats
   ```

2. **Adjust resource limits** in [`docker-compose.yml`](../docker-compose.yml):
   ```yaml
   deploy:
     resources:
       limits:
         memory: 1G  # Increase as needed
   ```

3. **Clear Redis cache**:
   ```bash
   docker-compose exec redis redis-cli FLUSHDB
   ```

4. **Restart services**:
   ```bash
   docker-compose restart
   ```

---

## Performance Optimization

### Metric Collection Optimization

**Reduce scrape interval** for less critical services:

```yaml
# In prometheus.yml
scrape_configs:
  - job_name: 'non-critical'
    scrape_interval: 60s  # Increased from 15s
```

### Grafana Query Optimization

1. **Use recording rules** for expensive queries
2. **Set appropriate refresh intervals**
3. **Limit time ranges** on dashboards
4. **Use query caching** in Grafana

### Storage Management

**Prometheus retention**:

```yaml
# In docker-compose.yml
command:
  - '--storage.tsdb.retention.time=30d'  # Adjust as needed
  - '--storage.tsdb.retention.size=10GB'
```

**Clean old data**:

```bash
# Remove old Prometheus data
docker-compose exec prometheus rm -rf /prometheus/data/*
docker-compose restart prometheus
```

---

## Best Practices

1. **Regular Backups**: Schedule daily Neo4j backups
2. **Monitor Metrics**: Check dashboards daily
3. **Set Alerts**: Configure alerts for critical metrics
4. **Review Performance**: Weekly performance reviews
5. **Update Documentation**: Keep runbooks current
6. **Test Recovery**: Periodically test backup restoration
7. **Capacity Planning**: Monitor resource trends
8. **Security**: Restrict access to monitoring tools in production

---

## Additional Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Neo4j Operations Manual](https://neo4j.com/docs/operations-manual/)
- [Redis Documentation](https://redis.io/documentation)

---

*Last Updated: 2025-10-10*