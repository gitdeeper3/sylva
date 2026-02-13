# Deployment Guide

## 🐳 Docker Deployment

### Production Deployment
```bash
# Build image
docker build -t sylva-fire:latest .

# Run container
docker run -d \
  --name sylva \
  -p 8080:8080 \
  -v /data/sylva:/app/data \
  sylva-fire:latest
```

Docker Compose

```bash
docker-compose up -d
```

☁️ Cloud Deployment

AWS

```bash
# ECS deployment
ecs-cli configure --region eu-west-1 --cluster sylva
ecs-cli compose --file docker-compose.yml up
```

Google Cloud

```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/sylva
gcloud run deploy --image gcr.io/PROJECT-ID/sylva
```

📱 Mobile Deployment

· Android APK: /dist/sylva-mobile.apk
· iOS: TestFlight beta access

🔧 Configuration

Environment variables:

· SYLVA_ENV: production/staging/development
· SYLVA_DATA_DIR: /path/to/data
· SYLVA_LOG_LEVEL: INFO/DEBUG/WARNING
· SYLVA_API_KEY: API authentication key

✅ Post-Deployment Verification

1. Run health check: curl http://localhost:8080/health
2. Verify data ingestion
3. Test alert system
4. Validate with historical case studies
