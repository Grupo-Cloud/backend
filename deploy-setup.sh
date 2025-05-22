#!/bin/bash
# deploy-setup.sh - Complete deployment setup script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PROJECT_ID="proyectocloud-455517"
REGION="us-central1"
ZONE="us-central1-a"
SERVICE_NAME="notebooklmini-backend"
CLOUD_SQL_INSTANCE="pg-db"  # Fixed: Just the instance name, not the full connection string
GCS_BUCKET="documents-1f8ab091a27a451caf02da6239f9f50a"
QDRANT_INSTANCE_NAME="qdrant-instance"

echo -e "${GREEN}🚀 Starting deployment setup for NotebookLMini${NC}"

# 1. Enable required APIs
echo -e "${YELLOW}📡 Enabling required Google Cloud APIs...${NC}"
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    sqladmin.googleapis.com \
    storage.googleapis.com \
    compute.googleapis.com \
    --project=$PROJECT_ID

# 2. Create GCS bucket for documents
echo -e "${YELLOW}🗂️  Creating GCS bucket for documents...${NC}"
gsutil mb -p $PROJECT_ID gs://$GCS_BUCKET || echo "Bucket already exists"

# 3. Create Compute Engine instance for Qdrant (Fixed image reference)
echo -e "${YELLOW}🖥️  Creating Compute Engine instance for Qdrant...${NC}"
gcloud compute instances create $QDRANT_INSTANCE_NAME \
    --project=$PROJECT_ID \
    --zone=$ZONE \
    --machine-type=e2-medium \
    --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
    --metadata-from-file=startup-script=startup-script.sh \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --tags=qdrant-server \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=20GB \
    --boot-disk-type=pd-standard \
    --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --reservation-affinity=any

# 4. Create firewall rule for Qdrant
echo -e "${YELLOW}🔥 Creating firewall rule for Qdrant...${NC}"
gcloud compute firewall-rules create allow-qdrant \
    --project=$PROJECT_ID \
    --direction=INGRESS \
    --priority=1000 \
    --network=default \
    --action=ALLOW \
    --rules=tcp:6333,tcp:6334 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=qdrant-server || echo "Firewall rule already exists"

# 5. Wait a moment for instance to be ready, then get external IP
echo -e "${YELLOW}🔍 Waiting for instance to be ready and getting external IP...${NC}"
sleep 30  # Wait for instance to be fully created
QDRANT_IP=$(gcloud compute instances describe $QDRANT_INSTANCE_NAME --zone=$ZONE --format="get(networkInterfaces[0].accessConfigs[0].natIP)")
echo -e "${GREEN}Qdrant External IP: $QDRANT_IP${NC}"

# 6. Grant Cloud Build service account necessary permissions
echo -e "${YELLOW}🔐 Setting up IAM permissions...${NC}"
CLOUD_BUILD_SA=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")@cloudbuild.gserviceaccount.com

# Cloud Run deployment permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$CLOUD_BUILD_SA" \
    --role="roles/run.admin"

# Cloud SQL permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$CLOUD_BUILD_SA" \
    --role="roles/cloudsql.client"

# Storage permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$CLOUD_BUILD_SA" \
    --role="roles/storage.admin"

# Service account user (for Cloud Run)
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$CLOUD_BUILD_SA" \
    --role="roles/iam.serviceAccountUser"

echo -e "${GREEN}✅ Deployment setup completed!${NC}"
echo -e "${GREEN}📋 Next steps:${NC}"
echo -e "1. Create a Cloud Build trigger manually in the Console"
echo -e "2. Set substitution variables in the trigger"
echo -e "3. Push your code to trigger the first build"
echo -e "4. Wait for Qdrant instance to fully start (~5 minutes)"
echo -e "5. Check Qdrant dashboard at http://$QDRANT_IP:6333/dashboard"
echo -e "6. Monitor Cloud Build at https://console.cloud.google.com/cloud-build/builds"

# Create environment file template
cat > .env.example << EOF
# Database (Cloud SQL)
POSTGRES_HOST=/cloudsql/$PROJECT_ID:$REGION:$CLOUD_SQL_INSTANCE
POSTGRES_USER=cloud
POSTGRES_PASSWORD=cloud123
POSTGRES_DB=postgres

# JWT Secrets
JWT_SECRET_KEY=oXEvSSFm4-KJ_0TstrJ83IYVVPD36kgvSh-MJOQn4SvO3ZOxQU7ay6hf-r-ylrkqt8uhnYQP5OMrSa7v2GTMow
JWT_REFRESH_KEY=k9B8HmVBS49Ghasr70v7AUA6OLOaSoEwdu00sWkFsOcj4s6y8kxHBcqXB1jmnOwfQbcn_4S6WO2zfAmUEWgOJQ

# Google API
GOOGLE_API_KEY=AIzaSyA42jL2yYqlY8_DANM-fdZ5p75EChQ-F04

# S3-Compatible Storage (Google Cloud Storage)
S3_HOST=storage.googleapis.com
S3_ACCESS_KEY=GOOGPKETNBL3JG6CK7H6LZNA
S3_SECRET_KEY=gxOgTXDvhvm8XS0ZVoaBHGDpurakzC90a+VnDVu5
S3_SECURE=true
S3_TYPE=gcs
S3_DOCUMENT_BUCKET=$GCS_BUCKET

# Qdrant
QDRANT_HOST=$QDRANT_IP
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=chunks
EOF

echo -e "${GREEN}📝 Created .env.example with your configuration${NC}"

# Prevent Git Bash from closing immediately
echo -e "${YELLOW}Script completed. Press any key to close...${NC}"
read -n 1 -s