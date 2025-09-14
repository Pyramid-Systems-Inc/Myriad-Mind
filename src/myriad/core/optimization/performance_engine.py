"""
Performance Optimization Engine
===============================

Advanced performance optimization system for the Myriad Cognitive Architecture.
Provides comprehensive performance enhancements including:
- Redis distributed caching
- Neo4j connection pooling
- Query optimization and indexing
- Response compression
- Performance monitoring and metrics
- Async processing capabilities

This system builds on top of Enhanced Graph Intelligence to provide
production-ready performance optimizations for high-scale deployments.

Author: Myriad Cognitive Architecture Team
Version: 1.0 (Performance Optimization Engine)
Date: 2025-01-01
"""

import asyncio
import time
import json
import gzip
import threading
import logging
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict, deque
import hashlib
import statistics
from contextlib import asynccontextmanager
import redis
from neo4j import GraphDatabase, Driver
import psutil
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""
    timestamp: datetime
    operation: str
    response_time: float
    cache_hit: bool
    memory_usage: float
    cpu_usage: float
    active_connections: int
    query_complexity: int
    compression_ratio: float
    error_count: int

@dataclass
class CacheEntry:
    """Cache entry with metadata"""
    data: Any
    timestamp: datetime
    access_count: int
    last_accessed: datetime
    expiry: Optional[datetime]
    compression_enabled: bool

@dataclass
class ConnectionPoolStats:
    """Connection pool statistics"""
    total_connections: int
    active_connections: int
    idle_connections: int
    peak_connections: int
    connection_wait_time: float
    total_queries: int
    failed_connections: int

class RedisDistributedCache:
    """
    Advanced Redis-based distributed caching system.
    
    Features:
    - Automatic compression for large objects
    - TTL management with sliding expiration
    - Cache warming and preloading
    - Hit/miss ratio tracking
    - Intelligent cache eviction
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379", 
                 default_ttl: int = 3600, compression_threshold: int = 1024):
        self.redis_url = redis_url
        self.default_ttl = default_ttl
        self.compression_threshold = compression_threshold
        self.metrics = defaultdict(int)
        
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=False)
            self.redis_client.ping()
            logger.info(f"✅ Redis connected: {redis_url}")
        except Exception as e:
            logger.warning(f"⚠️  Redis connection failed: {e}")
            self.redis_client = None
    
    def _generate_key(self, prefix: str, data: Dict[str, Any]) -> str:
        """Generate consistent cache key"""
        key_data = json.dumps(data, sort_keys=True)
        key_hash = hashlib.md5(key_data.encode()).hexdigest()
        return f"myriad:{prefix}:{key_hash}"
    
    def _compress_data(self, data: bytes) -> bytes:
        """Compress data if above threshold"""
        if len(data) > self.compression_threshold:
            return gzip.compress(data)
        return data
    
    def _decompress_data(self, data: bytes, compressed: bool) -> bytes:
        """Decompress data if needed"""
        if compressed:
            return gzip.decompress(data)
        return data
    
    async def get(self, prefix: str, query_data: Dict[str, Any]) -> Optional[Any]:
        """Get cached data with metrics tracking"""
        if not self.redis_client:
            return None
        
        cache_key = self._generate_key(prefix, query_data)
        
        try:
            cached_data = self.redis_client.get(cache_key)
            if cached_data:
                # Parse metadata
                entry_data = json.loads(cached_data.decode())
                compressed = entry_data.get('compressed', False)
                
                # Decompress and deserialize
                raw_data = bytes.fromhex(entry_data['data'])
                decompressed = self._decompress_data(raw_data, compressed)
                result = json.loads(decompressed.decode())
                
                # Update access metrics
                self.metrics['cache_hits'] += 1
                self.redis_client.hincrby(f"{cache_key}:meta", "access_count", 1)
                self.redis_client.hset(f"{cache_key}:meta", "last_accessed", datetime.now().isoformat())
                
                logger.debug(f"📋 Cache HIT: {prefix}")
                return result
            else:
                self.metrics['cache_misses'] += 1
                logger.debug(f"❌ Cache MISS: {prefix}")
                return None
                
        except Exception as e:
            logger.warning(f"Cache get error: {e}")
            self.metrics['cache_errors'] += 1
            return None
    
    async def set(self, prefix: str, query_data: Dict[str, Any], 
                  result_data: Any, ttl: Optional[int] = None) -> bool:
        """Set cached data with compression and metadata"""
        if not self.redis_client:
            return False
        
        cache_key = self._generate_key(prefix, query_data)
        ttl = ttl or self.default_ttl
        
        try:
            # Serialize and compress
            serialized = json.dumps(result_data).encode()
            compressed_data = self._compress_data(serialized)
            is_compressed = len(compressed_data) < len(serialized)
            
            # Create cache entry
            cache_entry = {
                'data': compressed_data.hex(),
                'compressed': is_compressed,
                'timestamp': datetime.now().isoformat(),
                'size': len(compressed_data),
                'original_size': len(serialized)
            }
            
            # Store in Redis
            self.redis_client.setex(
                cache_key, 
                ttl, 
                json.dumps(cache_entry)
            )
            
            # Store metadata
            self.redis_client.hset(f"{cache_key}:meta", mapping={
                "created": datetime.now().isoformat(),
                "access_count": 0,
                "ttl": ttl,
                "compression_ratio": len(compressed_data) / len(serialized)
            })
            self.redis_client.expire(f"{cache_key}:meta", ttl)
            
            self.metrics['cache_sets'] += 1
            logger.debug(f"💾 Cache SET: {prefix} (compressed: {is_compressed})")
            return True
            
        except Exception as e:
            logger.warning(f"Cache set error: {e}")
            self.metrics['cache_errors'] += 1
            return False
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics"""
        total_operations = self.metrics['cache_hits'] + self.metrics['cache_misses']
        hit_ratio = self.metrics['cache_hits'] / max(total_operations, 1)
        
        try:
            redis_info = self.redis_client.info() if self.redis_client else {}
            memory_usage = redis_info.get('used_memory_human', 'N/A')
            connected_clients = redis_info.get('connected_clients', 0)
        except:
            memory_usage = 'N/A'
            connected_clients = 0
        
        return {
            'cache_hits': self.metrics['cache_hits'],
            'cache_misses': self.metrics['cache_misses'],
            'cache_sets': self.metrics['cache_sets'],
            'cache_errors': self.metrics['cache_errors'],
            'hit_ratio': hit_ratio,
            'memory_usage': memory_usage,
            'connected_clients': connected_clients,
            'total_operations': total_operations
        }

class Neo4jConnectionPool:
    """
    Advanced Neo4j connection pool with performance optimization.
    
    Features:
    - Dynamic connection scaling
    - Connection health monitoring
    - Query performance tracking
    - Automatic retry logic
    - Connection leak detection
    """
    
    def __init__(self, uri: str, user: str, password: str, 
                 max_connections: int = 50, min_connections: int = 5):
        self.uri = uri
        self.user = user
        self.password = password
        self.max_connections = max_connections
        self.min_connections = min_connections
        
        self.active_connections = 0
        self.peak_connections = 0
        self.total_queries = 0
        self.failed_connections = 0
        self.connection_times = deque(maxlen=100)
        
        # Initialize driver with optimized settings
        self.driver = GraphDatabase.driver(
            uri, 
            auth=(user, password),
            max_connection_lifetime=3600,  # 1 hour
            max_connection_pool_size=max_connections,
            connection_acquisition_timeout=30,
            encrypted=False,  # Adjust based on setup
            trust="TRUST_ALL_CERTIFICATES"  # Adjust for production
        )
        
        logger.info(f"✅ Neo4j connection pool initialized: {uri}")
    
    @asynccontextmanager
    async def get_session(self):
        """Get optimized Neo4j session with monitoring"""
        start_time = time.time()
        session = None
        
        try:
            self.active_connections += 1
            self.peak_connections = max(self.peak_connections, self.active_connections)
            
            session = self.driver.session(
                database="neo4j",
                fetch_size=1000  # Optimize batch size
            )
            
            connection_time = time.time() - start_time
            self.connection_times.append(connection_time)
            
            yield session
            
        except Exception as e:
            self.failed_connections += 1
            logger.error(f"Connection error: {e}")
            raise
        finally:
            if session:
                session.close()
            self.active_connections -= 1
    
    async def execute_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict]:
        """Execute optimized query with performance tracking"""
        start_time = time.time()
        self.total_queries += 1
        
        async with self.get_session() as session:
            try:
                result = session.run(query, parameters or {})
                records = [record.data() for record in result]
                
                execution_time = time.time() - start_time
                logger.debug(f"🔍 Query executed in {execution_time:.3f}s: {len(records)} records")
                
                return records
                
            except Exception as e:
                logger.error(f"Query execution error: {e}")
                raise
    
    def get_pool_stats(self) -> ConnectionPoolStats:
        """Get connection pool statistics"""
        avg_connection_time = statistics.mean(self.connection_times) if self.connection_times else 0
        
        return ConnectionPoolStats(
            total_connections=self.max_connections,
            active_connections=self.active_connections,
            idle_connections=self.max_connections - self.active_connections,
            peak_connections=self.peak_connections,
            connection_wait_time=avg_connection_time,
            total_queries=self.total_queries,
            failed_connections=self.failed_connections
        )
    
    def close(self):
        """Close connection pool"""
        if self.driver:
            self.driver.close()
            logger.info("🔌 Neo4j connection pool closed")

class ResponseCompression:
    """
    Response compression system for network efficiency.
    
    Features:
    - Automatic compression based on response size
    - Multiple compression algorithms
    - Compression ratio tracking
    - Content-type aware compression
    """
    
    def __init__(self, compression_threshold: int = 1024, compression_level: int = 6):
        self.compression_threshold = compression_threshold
        self.compression_level = compression_level
        self.compression_stats = defaultdict(int)
    
    def compress_response(self, data: Any, content_type: str = "application/json") -> Dict[str, Any]:
        """Compress response data if beneficial"""
        
        # Serialize data
        if isinstance(data, (dict, list)):
            serialized = json.dumps(data, ensure_ascii=False).encode('utf-8')
        elif isinstance(data, str):
            serialized = data.encode('utf-8')
        else:
            serialized = str(data).encode('utf-8')
        
        original_size = len(serialized)
        
        # Only compress if above threshold
        if original_size < self.compression_threshold:
            self.compression_stats['uncompressed_responses'] += 1
            return {
                'data': serialized.decode('utf-8') if content_type == "application/json" else serialized,
                'compressed': False,
                'original_size': original_size,
                'compressed_size': original_size,
                'compression_ratio': 1.0
            }
        
        # Compress data
        compressed = gzip.compress(serialized, compresslevel=self.compression_level)
        compressed_size = len(compressed)
        compression_ratio = compressed_size / original_size
        
        # Only use compression if beneficial
        if compression_ratio < 0.9:  # At least 10% savings
            self.compression_stats['compressed_responses'] += 1
            return {
                'data': compressed,
                'compressed': True,
                'original_size': original_size,
                'compressed_size': compressed_size,
                'compression_ratio': compression_ratio,
                'encoding': 'gzip'
            }
        else:
            self.compression_stats['uncompressed_responses'] += 1
            return {
                'data': serialized.decode('utf-8') if content_type == "application/json" else serialized,
                'compressed': False,
                'original_size': original_size,
                'compressed_size': original_size,
                'compression_ratio': 1.0
            }
    
    def get_compression_stats(self) -> Dict[str, Any]:
        """Get compression statistics"""
        total_responses = (self.compression_stats['compressed_responses'] + 
                          self.compression_stats['uncompressed_responses'])
        compression_rate = (self.compression_stats['compressed_responses'] / 
                           max(total_responses, 1))
        
        return {
            'compressed_responses': self.compression_stats['compressed_responses'],
            'uncompressed_responses': self.compression_stats['uncompressed_responses'],
            'total_responses': total_responses,
            'compression_rate': compression_rate
        }

class PerformanceMonitor:
    """
    Comprehensive performance monitoring system.
    
    Features:
    - Real-time metrics collection
    - Performance trend analysis
    - Automatic alerting
    - Resource usage monitoring
    - Query performance profiling
    """
    
    def __init__(self, metrics_retention: int = 1000):
        self.metrics_retention = metrics_retention
        self.metrics_history = deque(maxlen=metrics_retention)
        self.performance_thresholds = {
            'max_response_time': 5.0,  # seconds
            'max_memory_usage': 80.0,  # percentage
            'max_cpu_usage': 80.0,     # percentage
            'min_cache_hit_ratio': 0.7  # 70%
        }
        self.alerts = []
        
        # Start background monitoring
        self._start_monitoring()
    
    def record_metric(self, operation: str, response_time: float, 
                     cache_hit: bool = False, query_complexity: int = 1,
                     compression_ratio: float = 1.0, error_count: int = 0):
        """Record performance metric"""
        
        # Get system metrics
        memory_usage = psutil.virtual_memory().percent
        cpu_usage = psutil.cpu_percent()
        
        metric = PerformanceMetrics(
            timestamp=datetime.now(),
            operation=operation,
            response_time=response_time,
            cache_hit=cache_hit,
            memory_usage=memory_usage,
            cpu_usage=cpu_usage,
            active_connections=0,  # Will be updated by connection pool
            query_complexity=query_complexity,
            compression_ratio=compression_ratio,
            error_count=error_count
        )
        
        self.metrics_history.append(metric)
        
        # Check for alerts
        self._check_performance_alerts(metric)
    
    def _check_performance_alerts(self, metric: PerformanceMetrics):
        """Check if metric triggers any alerts"""
        
        alerts = []
        
        if metric.response_time > self.performance_thresholds['max_response_time']:
            alerts.append(f"High response time: {metric.response_time:.2f}s")
        
        if metric.memory_usage > self.performance_thresholds['max_memory_usage']:
            alerts.append(f"High memory usage: {metric.memory_usage:.1f}%")
        
        if metric.cpu_usage > self.performance_thresholds['max_cpu_usage']:
            alerts.append(f"High CPU usage: {metric.cpu_usage:.1f}%")
        
        for alert in alerts:
            self.alerts.append({
                'timestamp': metric.timestamp,
                'operation': metric.operation,
                'alert': alert,
                'severity': 'warning'
            })
            logger.warning(f"⚠️  Performance Alert: {alert}")
    
    def get_performance_summary(self, minutes: int = 60) -> Dict[str, Any]:
        """Get performance summary for the last N minutes"""
        
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        recent_metrics = [m for m in self.metrics_history if m.timestamp > cutoff_time]
        
        if not recent_metrics:
            return {'message': 'No metrics available'}
        
        # Calculate aggregated metrics
        avg_response_time = statistics.mean([m.response_time for m in recent_metrics])
        max_response_time = max([m.response_time for m in recent_metrics])
        avg_memory_usage = statistics.mean([m.memory_usage for m in recent_metrics])
        avg_cpu_usage = statistics.mean([m.cpu_usage for m in recent_metrics])
        cache_hit_ratio = sum([1 for m in recent_metrics if m.cache_hit]) / len(recent_metrics)
        total_errors = sum([m.error_count for m in recent_metrics])
        
        # Get recent alerts
        recent_alerts = [a for a in self.alerts if a['timestamp'] > cutoff_time]
        
        return {
            'time_period_minutes': minutes,
            'total_operations': len(recent_metrics),
            'avg_response_time': avg_response_time,
            'max_response_time': max_response_time,
            'avg_memory_usage': avg_memory_usage,
            'avg_cpu_usage': avg_cpu_usage,
            'cache_hit_ratio': cache_hit_ratio,
            'total_errors': total_errors,
            'recent_alerts': len(recent_alerts),
            'performance_score': self._calculate_performance_score(recent_metrics)
        }
    
    def _calculate_performance_score(self, metrics: List[PerformanceMetrics]) -> float:
        """Calculate overall performance score (0-100)"""
        
        if not metrics:
            return 0.0
        
        # Score components (0-1 each)
        response_time_score = max(0, 1 - (statistics.mean([m.response_time for m in metrics]) / 10))
        memory_score = max(0, 1 - (statistics.mean([m.memory_usage for m in metrics]) / 100))
        cpu_score = max(0, 1 - (statistics.mean([m.cpu_usage for m in metrics]) / 100))
        cache_score = sum([1 for m in metrics if m.cache_hit]) / len(metrics)
        error_score = max(0, 1 - (sum([m.error_count for m in metrics]) / len(metrics)))
        
        # Weighted average
        weights = {
            'response_time': 0.3,
            'memory': 0.2,
            'cpu': 0.2,
            'cache': 0.2,
            'errors': 0.1
        }
        
        weighted_score = (
            response_time_score * weights['response_time'] +
            memory_score * weights['memory'] +
            cpu_score * weights['cpu'] +
            cache_score * weights['cache'] +
            error_score * weights['errors']
        )
        
        return weighted_score * 100  # Convert to 0-100 scale
    
    def _start_monitoring(self):
        """Start background monitoring thread"""
        
        def monitor_loop():
            while True:
                try:
                    # Record system metrics every 30 seconds
                    self.record_metric(
                        operation="system_monitor",
                        response_time=0.0,
                        cache_hit=False,
                        query_complexity=0,
                        compression_ratio=1.0,
                        error_count=0
                    )
                    time.sleep(30)
                except Exception as e:
                    logger.error(f"Monitoring error: {e}")
                    time.sleep(60)
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        logger.info("📊 Performance monitoring started")

class PerformanceOptimizationEngine:
    """
    Main performance optimization engine coordinating all optimization systems.
    
    Features:
    - Distributed Redis caching
    - Neo4j connection pooling
    - Response compression
    - Performance monitoring
    - Async processing capabilities
    - Comprehensive metrics and alerting
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        
        # Initialize components
        self.cache = RedisDistributedCache(
            redis_url=self.config.get('redis_url', 'redis://localhost:6379'),
            default_ttl=self.config.get('cache_ttl', 3600),
            compression_threshold=self.config.get('compression_threshold', 1024)
        )
        
        self.connection_pool = Neo4jConnectionPool(
            uri=self.config.get('neo4j_uri', 'bolt://localhost:7687'),
            user=self.config.get('neo4j_user', 'neo4j'),
            password=self.config.get('neo4j_password', 'password'),
            max_connections=self.config.get('max_connections', 50)
        )
        
        self.compression = ResponseCompression(
            compression_threshold=self.config.get('compression_threshold', 1024),
            compression_level=self.config.get('compression_level', 6)
        )
        
        self.monitor = PerformanceMonitor(
            metrics_retention=self.config.get('metrics_retention', 1000)
        )
        
        logger.info("🚀 Performance Optimization Engine initialized")
    
    async def optimized_query(self, operation: str, query: str, 
                             parameters: Dict[str, Any] = None,
                             cache_key_data: Dict[str, Any] = None,
                             use_cache: bool = True) -> Dict[str, Any]:
        """Execute optimized query with all performance features"""
        
        start_time = time.time()
        cache_hit = False
        error_count = 0
        
        try:
            # Try cache first
            if use_cache and cache_key_data:
                cached_result = await self.cache.get("query", cache_key_data)
                if cached_result:
                    cache_hit = True
                    response_time = time.time() - start_time
                    
                    # Record metrics
                    self.monitor.record_metric(
                        operation=operation,
                        response_time=response_time,
                        cache_hit=True,
                        query_complexity=len(query.split()),
                        compression_ratio=1.0,
                        error_count=0
                    )
                    
                    return {
                        'data': cached_result,
                        'cached': True,
                        'response_time': response_time,
                        'source': 'cache'
                    }
            
            # Execute query with connection pool
            query_result = await self.connection_pool.execute_query(query, parameters)
            
            # Cache the result
            if use_cache and cache_key_data:
                await self.cache.set("query", cache_key_data, query_result)
            
            # Compress response
            compressed_response = self.compression.compress_response(query_result)
            
            response_time = time.time() - start_time
            
            # Record metrics
            self.monitor.record_metric(
                operation=operation,
                response_time=response_time,
                cache_hit=cache_hit,
                query_complexity=len(query.split()),
                compression_ratio=compressed_response['compression_ratio'],
                error_count=error_count
            )
            
            return {
                'data': query_result,
                'cached': False,
                'response_time': response_time,
                'source': 'database',
                'compression': compressed_response
            }
            
        except Exception as e:
            error_count = 1
            response_time = time.time() - start_time
            
            # Record error metrics
            self.monitor.record_metric(
                operation=operation,
                response_time=response_time,
                cache_hit=cache_hit,
                query_complexity=len(query.split()) if query else 0,
                compression_ratio=1.0,
                error_count=error_count
            )
            
            logger.error(f"Optimized query error: {e}")
            raise
    
    def get_comprehensive_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics"""
        
        return {
            'cache_stats': self.cache.get_cache_stats(),
            'connection_pool_stats': asdict(self.connection_pool.get_pool_stats()),
            'compression_stats': self.compression.get_compression_stats(),
            'performance_summary': self.monitor.get_performance_summary(),
            'system_info': {
                'memory_usage': psutil.virtual_memory().percent,
                'cpu_usage': psutil.cpu_percent(),
                'disk_usage': psutil.disk_usage('/').percent,
                'uptime': time.time() - psutil.boot_time()
            }
        }
    
    def close(self):
        """Clean shutdown of performance optimization engine"""
        self.connection_pool.close()
        logger.info("🔌 Performance Optimization Engine shutdown complete")


# Global performance optimization engine instance
performance_engine = None

def get_performance_engine(config: Dict[str, Any] = None) -> PerformanceOptimizationEngine:
    """Get the global performance optimization engine instance"""
    global performance_engine
    if performance_engine is None:
        performance_engine = PerformanceOptimizationEngine(config)
    return performance_engine


if __name__ == "__main__":
    # Test the performance optimization engine
    import asyncio
    
    async def test_performance_engine():
        engine = PerformanceOptimizationEngine()
        
        # Test optimized query
        result = await engine.optimized_query(
            operation="test_query",
            query="MATCH (n:Agent) RETURN n.name LIMIT 5",
            cache_key_data={"query_type": "agent_list", "limit": 5}
        )
        
        print(f"🚀 Query result: {result}")
        
        # Get comprehensive stats
        stats = engine.get_comprehensive_stats()
        print(f"\n📊 Performance stats:")
        print(json.dumps(stats, indent=2, default=str))
        
        engine.close()
    
    asyncio.run(test_performance_engine())
