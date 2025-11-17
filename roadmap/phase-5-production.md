# Phase 5: Production Ready - Kubernetes & Scaling

**Duration**: 5-6 weeks  
**Goal**: Production-grade deployment with Kubernetes and scaling  
**Prerequisites**: Phase 4 complete

---

## Objectives

✅ Kubernetes deployment with Helm  
✅ Three-layer knowledge substrate (S3 + Redis + Graph)  
✅ Cognitive tier system (swift/base/max)  
✅ Monitoring and observability  
✅ CI/CD pipeline  
✅ Handle 1000+ queries/day

---

## Step 1: Containerize All Services

**File**: `src/Myriad.Services.Orchestrator/Dockerfile`

```dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 80

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["Myriad.Services.Orchestrator.csproj", "./"]
RUN dotnet restore
COPY . .
RUN dotnet build -c Release -o /app/build

FROM build AS publish
RUN dotnet publish -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "Myriad.Services.Orchestrator.dll"]
```

**Task**: Create Dockerfiles for all services (Orchestrator, GraphDB, Input/Output Processors, Agents)

**Acceptance**: All services run in Docker containers

---

## Step 2: Kubernetes Manifests

**File**: `k8s/orchestrator-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orchestrator
  namespace: myriad
spec:
  replicas: 3
  selector:
    matchLabels:
      app: orchestrator
  template:
    metadata:
      labels:
        app: orchestrator
    spec:
      containers:
      - name: orchestrator
        image: myriad/orchestrator:latest
        ports:
        - containerPort: 80
        env:
        - name: ASPNETCORE_ENVIRONMENT
          value: "Production"
        - name: GRAPHDB_URL
          value: "http://graphdb-service:80"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: orchestrator-service
  namespace: myriad
spec:
  selector:
    app: orchestrator
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: orchestrator-hpa
  namespace: myriad
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: orchestrator
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

**Acceptance**: Services deploy to Kubernetes and auto-scale

---

## Step 3: Helm Chart

**File**: `helm/myriad/Chart.yaml`

```yaml
apiVersion: v2
name: myriad
description: Myriad Cognitive Architecture
version: 1.0.0
appVersion: "1.0"
```

**File**: `helm/myriad/values.yaml`

```yaml
orchestrator:
  replicaCount: 3
  image:
    repository: myriad/orchestrator
    tag: latest
  resources:
    requests:
      memory: "512Mi"
      cpu: "500m"
    limits:
      memory: "2Gi"
      cpu: "2000m"

graphdb:
  replicaCount: 1
  image:
    repository: myriad/graphdb
    tag: latest
  persistence:
    enabled: true
    size: 10Gi

redis:
  enabled: true
  cluster:
    enabled: true
    nodes: 3

s3:
  bucket: myriad-packets
  region: us-east-1
```

**Acceptance**: Helm chart deploys entire stack

---

## Step 4: Cognitive Tier System

**File**: `src/Myriad.Services.Orchestrator/Policies/CognitivePolicyEngine.cs`

```csharp
namespace Myriad.Services.Orchestrator.Policies;

public class CognitivePolicyEngine
{
    private readonly Dictionary<string, PolicyConfiguration> _policies = new()
    {
        ["myriad-swift"] = new()
        {
            MaxAgentsPerQuery = 1,
            GraphTraversalDepth = 1,
            UseEnhancedIntelligence = false,
            UseCognitiveSynthesizer = false,
            MaxProcessingTimeMs = 500
        },
        ["myriad-base"] = new()
        {
            MaxAgentsPerQuery = 5,
            GraphTraversalDepth = 2,
            UseEnhancedIntelligence = true,
            UseCognitiveSynthesizer = true,
            MaxProcessingTimeMs = 3000
        },
        ["myriad-max"] = new()
        {
            MaxAgentsPerQuery = 15,
            GraphTraversalDepth = 3,
            UseEnhancedIntelligence = true,
            UseCognitiveSynthesizer = true,
            EnableSocraticLoop = true,
            MaxProcessingTimeMs = 10000
        }
    };
    
    public PolicyConfiguration GetPolicy(string model) =>
        _policies.TryGetValue(model, out var policy) 
            ? policy 
            : _policies["myriad-base"];
}

public record PolicyConfiguration
{
    public int MaxAgentsPerQuery { get; init; }
    public int GraphTraversalDepth { get; init; }
    public bool UseEnhancedIntelligence { get; init; }
    public bool UseCognitiveSynthesizer { get; init; }
    public bool EnableSocraticLoop { get; init; }
    public int MaxProcessingTimeMs { get; init; }
}
```

**Acceptance**: API accepts `model` parameter and applies correct policy

---

## Step 5: Monitoring with Prometheus

**File**: `src/Myriad.Services.Orchestrator/Metrics.cs`

```csharp
using Prometheus;

namespace Myriad.Services.Orchestrator;

public static class Metrics
{
    public static readonly Counter RequestCount = 
        Prometheus.Metrics.CreateCounter(
            "myriad_requests_total",
            "Total requests",
            new CounterConfiguration
            {
                LabelNames = new[] { "tier", "status" }
            });
    
    public static readonly Histogram RequestDuration = 
        Prometheus.Metrics.CreateHistogram(
            "myriad_request_duration_seconds",
            "Request duration",
            new HistogramConfiguration
            {
                LabelNames = new[] { "tier" }
            });
    
    public static readonly Gauge ActiveSessions = 
        Prometheus.Metrics.CreateGauge(
            "myriad_active_sessions",
            "Active user sessions");
    
    public static readonly Counter NeurogenesisEvents = 
        Prometheus.Metrics.CreateCounter(
            "myriad_neurogenesis_total",
            "Total agent creations");
}
```

**File**: Add to `Program.cs`

```csharp
app.UseMetricServer(); // Expose /metrics endpoint
app.UseHttpMetrics(); // Collect HTTP metrics
```

**Acceptance**: Prometheus scrapes metrics successfully

---

## Step 6: CI/CD Pipeline

**File**: `.github/workflows/build-and-deploy.yml`

```yaml
name: Build and Deploy

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup .NET
      uses: actions/setup-dotnet@v3
      with:
        dotnet-version: 8.0.x
    
    - name: Restore dependencies
      run: dotnet restore
    
    - name: Build
      run: dotnet build --no-restore -c Release
    
    - name: Test
      run: dotnet test --no-build -c Release
    
    - name: Build Docker images
      run: |
        docker build -t myriad/orchestrator:${{ github.sha }} \
          -f src/Myriad.Services.Orchestrator/Dockerfile .
        docker build -t myriad/graphdb:${{ github.sha }} \
          -f src/Myriad.Services.GraphDatabase/Dockerfile .
    
    - name: Push to registry
      run: |
        echo "${{ secrets.DOCKER_PASSWORD }}" | \
          docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
        docker push myriad/orchestrator:${{ github.sha }}
        docker push myriad/graphdb:${{ github.sha }}
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to Kubernetes
      run: |
        helm upgrade --install myriad ./helm/myriad \
          --set orchestrator.image.tag=${{ github.sha }} \
          --set graphdb.image.tag=${{ github.sha }}
```

**Acceptance**: Code pushes trigger automated builds and deployments

---

## Step 7: Load Testing

**File**: `tests/load-test.js` (using k6)

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up
    { duration: '5m', target: 100 }, // Stay at 100
    { duration: '2m', target: 200 }, // Ramp to 200
    { duration: '5m', target: 200 }, // Stay at 200
    { duration: '2m', target: 0 },   // Ramp down
  ],
};

export default function () {
  const payload = JSON.stringify({
    query: 'Why was the lightbulb important for factories?',
    model: 'myriad-base'
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const res = http.post('http://localhost:5000/process', payload, params);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 3000ms': (r) => r.timings.duration < 3000,
    'has answer': (r) => JSON.parse(r.body).answer !== undefined,
  });

  sleep(1);
}
```

**Run**: `k6 run tests/load-test.js`

**Acceptance**: Handles 200 concurrent users with <3s response time

---

## Step 8: Observability Stack

**Grafana Dashboard** (JSON config):

```json
{
  "dashboard": {
    "title": "Myriad Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(myriad_requests_total[5m])"
          }
        ]
      },
      {
        "title": "Response Time (p95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, myriad_request_duration_seconds)"
          }
        ]
      },
      {
        "title": "Active Sessions",
        "targets": [
          {
            "expr": "myriad_active_sessions"
          }
        ]
      }
    ]
  }
}
```

**Acceptance**: Grafana displays real-time metrics

---

## Deployment Checklist

**Pre-Deployment**:

- [ ] All services containerized
- [ ] Helm chart tested locally (minikube)
- [ ] Environment variables configured
- [ ] Secrets created (DB passwords, API keys)
- [ ] Resource limits set appropriately

**Deployment**:

- [ ] Kubernetes cluster provisioned (GKE/EKS/AKS)
- [ ] Namespaces created
- [ ] Helm chart deployed
- [ ] Ingress controller configured
- [ ] SSL certificates installed
- [ ] DNS configured

**Post-Deployment**:

- [ ] Health checks passing
- [ ] Metrics being collected
- [ ] Logs aggregated (ELK/Loki)
- [ ] Alerts configured
- [ ] Load testing passed
- [ ] Auto-scaling validated

---

## Acceptance Criteria

- [ ] All services running on Kubernetes
- [ ] Auto-scaling works (scales up under load)
- [ ] Cognitive tiers implemented (swift/base/max)
- [ ] Prometheus collecting metrics
- [ ] Grafana dashboards operational
- [ ] CI/CD pipeline functional
- [ ] Load test: 1000+ queries/day handled
- [ ] Average response time < 2s (base tier)
- [ ] 99.9% uptime over 1 week
- [ ] Costs optimized ($2000-3000/month for 50K queries)

---

## Cost Estimates

**Monthly Infrastructure** (50K queries/day):

- Kubernetes cluster (3-6 nodes): $300-600
- Redis cluster: $150-300
- S3 storage (100GB): $2.30
- Data transfer: $50-100
- Monitoring (Prometheus/Grafana): $50-100
- **Total**: ~$552-1102/month

**Plus** optional:

- Managed Neo4j: $200-500/month
- Load balancer: $20/month
- CDN: $50-100/month

**Time Estimate**: 5-6 weeks

---

## Success Metrics

**Performance**:

- myriad-swift: < 500ms average
- myriad-base: < 2s average
- myriad-max: < 10s average

**Reliability**:

- 99.9% uptime
- < 0.1% error rate
- Auto-recovery from failures

**Scalability**:

- Handles 10x traffic spike
- Auto-scales within 2 minutes
- Cost scales linearly with usage

---

## Troubleshooting Guide

**Pod not starting**:

```bash
kubectl describe pod <pod-name> -n myriad
kubectl logs <pod-name> -n myriad
```

**High latency**:

```bash
# Check HPA status
kubectl get hpa -n myriad

# Check resource usage
kubectl top pods -n myriad
```

**Database connection issues**:

```bash
# Test connectivity
kubectl run -it --rm debug --image=busybox --restart=Never -- \
  wget -O- http://graphdb-service:80/health
```

---

**Phase Complete!** 🎉

System is now production-ready and deployed to Kubernetes.

[Back to Roadmap](README.md) | [View Architecture](../architecture/)
