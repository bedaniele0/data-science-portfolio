# Deployment Guide - Walmart Demand Forecasting API

**Author**: Ing. Daniel Varela Perez
**Email**: bedaniele0@gmail.com
**Tel**: +52 55 4189 3428
**Date**: December 5, 2024
**Version**: 1.0.0

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Deployment](#local-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Kubernetes Deployment](#kubernetes-deployment)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Python**: 3.10+ (for local deployment)
- **Git**: 2.30+

### System Requirements

**Minimum**:
- CPU: 2 cores
- RAM: 2 GB
- Disk: 5 GB

**Recommended**:
- CPU: 4 cores
- RAM: 8 GB
- Disk: 20 GB
- SSD storage

---

## Local Deployment

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/walmart-demand-forecasting.git
cd walmart-demand-forecasting
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Verify Model Files

```bash
# Check model exists
ls -lh models/lightgbm_model.pkl

# Check feature catalog
ls -lh data/processed/feature_catalog.txt
```

### Step 5: Run API

```bash
# Development mode (with auto-reload)
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Step 6: Test API

```bash
# Health check
curl http://localhost:8000/health

# Make prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"item_id": "FOODS_1_001_CA_1", "store_id": "CA_1", "date": "2016-05-01"}'
```

### Step 7: Access Documentation

Open browser: `http://localhost:8000/docs`

---

## Docker Deployment

### Step 1: Build Docker Image

```bash
docker build -t walmart-forecasting-api:1.0.0 .
```

### Step 2: Run Container

```bash
docker run -d \
  --name walmart-forecasting-api \
  -p 8000:8000 \
  -v $(pwd)/models:/app/models:ro \
  -v $(pwd)/logs:/app/logs \
  --restart unless-stopped \
  walmart-forecasting-api:1.0.0
```

### Step 3: Check Status

```bash
# Check container logs
docker logs -f walmart-forecasting-api

# Check health
docker exec walmart-forecasting-api curl http://localhost:8000/health
```

### Using Docker Compose (Recommended)

### Step 1: Start Services

```bash
docker-compose up -d
```

### Step 2: Check Status

```bash
# View logs
docker-compose logs -f

# Check health
curl http://localhost:8000/health
```

### Step 3: Stop Services

```bash
docker-compose down
```

### Update Model

```bash
# Copy new model
cp new_model.pkl models/lightgbm_model.pkl

# Restart API
docker-compose restart api
```

---

## Cloud Deployment

### AWS (Elastic Container Service)

#### Prerequisites
- AWS account
- AWS CLI configured
- ECR repository created

#### Step 1: Push Image to ECR

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag walmart-forecasting-api:1.0.0 \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com/walmart-forecasting:1.0.0

# Push image
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/walmart-forecasting:1.0.0
```

#### Step 2: Create ECS Task Definition

```json
{
  "family": "walmart-forecasting",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/walmart-forecasting:1.0.0",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "memory": 2048,
      "cpu": 1024,
      "essential": true,
      "environment": [
        {
          "name": "LOG_LEVEL",
          "value": "INFO"
        }
      ],
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3
      }
    }
  ],
  "requiresCompatibilities": ["FARGATE"],
  "networkMode": "awsvpc",
  "cpu": "1024",
  "memory": "2048"
}
```

#### Step 3: Create ECS Service

```bash
aws ecs create-service \
  --cluster walmart-forecasting-cluster \
  --service-name walmart-forecasting-service \
  --task-definition walmart-forecasting:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
  --load-balancer "targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=api,containerPort=8000"
```

### Google Cloud Platform (Cloud Run)

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT_ID/walmart-forecasting

# Deploy to Cloud Run
gcloud run deploy walmart-forecasting \
  --image gcr.io/PROJECT_ID/walmart-forecasting \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10
```

### Azure (Container Instances)

```bash
# Login to Azure
az login

# Create resource group
az group create --name walmart-forecasting-rg --location eastus

# Create container instance
az container create \
  --resource-group walmart-forecasting-rg \
  --name walmart-forecasting-api \
  --image walmart-forecasting-api:1.0.0 \
  --dns-name-label walmart-forecasting \
  --ports 8000 \
  --cpu 2 \
  --memory 4
```

---

## Kubernetes Deployment

### Step 1: Create Deployment

`k8s/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: walmart-forecasting-api
  labels:
    app: walmart-forecasting
spec:
  replicas: 3
  selector:
    matchLabels:
      app: walmart-forecasting
  template:
    metadata:
      labels:
        app: walmart-forecasting
    spec:
      containers:
      - name: api
        image: walmart-forecasting-api:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: LOG_LEVEL
          value: "INFO"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Step 2: Create Service

`k8s/service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: walmart-forecasting-service
spec:
  type: LoadBalancer
  selector:
    app: walmart-forecasting
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

### Step 3: Deploy

```bash
# Apply configurations
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Check status
kubectl get pods
kubectl get svc

# View logs
kubectl logs -f deployment/walmart-forecasting-api
```

### Step 4: Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: walmart-forecasting-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: walmart-forecasting-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## Monitoring & Maintenance

### Health Monitoring

```bash
# Continuous health check
watch -n 10 'curl -s http://localhost:8000/health | jq'
```

### Log Monitoring

```bash
# Docker
docker logs -f walmart-forecasting-api

# Docker Compose
docker-compose logs -f api

# Kubernetes
kubectl logs -f deployment/walmart-forecasting-api
```

### Performance Monitoring

**Prometheus Configuration** (`prometheus.yml`):

```yaml
scrape_configs:
  - job_name: 'walmart-forecasting'
    static_configs:
      - targets: ['api:8000']
```

**Grafana Dashboard**:
- Request rate
- Response time (p50, p95, p99)
- Error rate
- CPU/Memory usage

### Backup Strategy

```bash
# Backup models
tar -czf models-backup-$(date +%Y%m%d).tar.gz models/

# Backup to S3
aws s3 cp models-backup-$(date +%Y%m%d).tar.gz s3://walmart-forecasting-backups/
```

### Update Procedure

1. **Build new image**:
   ```bash
   docker build -t walmart-forecasting-api:1.1.0 .
   ```

2. **Test locally**:
   ```bash
   docker run -p 8001:8000 walmart-forecasting-api:1.1.0
   curl http://localhost:8001/health
   ```

3. **Rolling update** (Kubernetes):
   ```bash
   kubectl set image deployment/walmart-forecasting-api api=walmart-forecasting-api:1.1.0
   kubectl rollout status deployment/walmart-forecasting-api
   ```

4. **Rollback if needed**:
   ```bash
   kubectl rollout undo deployment/walmart-forecasting-api
   ```

---

## Troubleshooting

### Issue: Model not loading

**Symptoms**:
- `/health` shows `model_loaded: false`
- 503 errors on predictions

**Solutions**:
```bash
# Check model file exists
ls -lh models/lightgbm_model.pkl

# Check file permissions
chmod 644 models/lightgbm_model.pkl

# Check logs
docker logs walmart-forecasting-api

# Verify model path in container
docker exec walmart-forecasting-api ls -lh /app/models/
```

### Issue: High latency

**Solutions**:
1. Use batch endpoint for multiple predictions
2. Increase worker count:
   ```bash
   uvicorn src.api.main:app --workers 4
   ```
3. Enable caching
4. Scale horizontally (add more instances)

### Issue: Out of memory

**Solutions**:
```bash
# Increase Docker memory
docker run -m 4g walmart-forecasting-api:1.0.0

# Or in docker-compose.yml
services:
  api:
    mem_limit: 4g
```

### Issue: Connection refused

**Solutions**:
```bash
# Check if container is running
docker ps

# Check if port is exposed
netstat -an | grep 8000

# Check firewall rules
sudo ufw status

# Allow port 8000
sudo ufw allow 8000
```

---

## Security Checklist

- [ ] API running behind HTTPS
- [ ] Authentication enabled (API keys/JWT)
- [ ] Rate limiting configured
- [ ] Input validation (Pydantic schemas)
- [ ] Non-root user in container
- [ ] Security scanning (Snyk, Trivy)
- [ ] Secrets in environment variables
- [ ] Regular dependency updates
- [ ] Log monitoring for anomalies
- [ ] Backup strategy in place

---

## Performance Optimization

### 1. Enable Caching

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def predict_cached(item_id, date):
    return predict(item_id, date)
```

### 2. Use Connection Pooling

```python
# For database connections
from sqlalchemy import create_engine, pool

engine = create_engine(
    "postgresql://...",
    poolclass=pool.QueuePool,
    pool_size=10,
    max_overflow=20
)
```

### 3. Async Endpoints (for I/O-bound operations)

```python
@app.post("/predict")
async def predict(request: PredictionRequest):
    # Use async operations
    return await async_predict(request)
```

---

## Production Checklist

**Before Going Live**:

- [ ] Load testing completed (target: 1000 req/s)
- [ ] Monitoring and alerting configured
- [ ] Backup and recovery tested
- [ ] Security audit completed
- [ ] Documentation updated
- [ ] API rate limiting enabled
- [ ] HTTPS configured
- [ ] Authentication implemented
- [ ] Error handling tested
- [ ] Logging configured (centralized)
- [ ] Health checks working
- [ ] Auto-scaling configured
- [ ] Disaster recovery plan documented
- [ ] Team trained on deployment process
- [ ] Rollback procedure tested

---

## Support

For deployment issues or questions:

**Author**: Ing. Daniel Varela Perez
**Email**: bedaniele0@gmail.com
**Phone**: +52 55 4189 3428

---

**Last Updated**: December 5, 2024
**Guide Version**: 1.0.0
**API Version**: 1.0.0
