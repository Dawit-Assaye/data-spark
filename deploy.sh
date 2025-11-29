#!/bin/bash

# DataSpark Cloud Run Deployment Script
# This script builds and deploys the DataSpark application to Google Cloud Run

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 DataSpark Cloud Run Deployment${NC}"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ Error: gcloud CLI is not installed${NC}"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo -e "${YELLOW}⚠️  Not authenticated with gcloud. Please run: gcloud auth login${NC}"
    exit 1
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}❌ Error: No GCP project set${NC}"
    echo "Please set a project with: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo -e "${GREEN}✓ Using GCP Project: ${PROJECT_ID}${NC}"

# Enable required APIs
echo -e "${YELLOW}Enabling required APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com --quiet
gcloud services enable run.googleapis.com --quiet
gcloud services enable containerregistry.googleapis.com --quiet

# Set region
REGION=${REGION:-us-central1}
echo -e "${GREEN}✓ Using region: ${REGION}${NC}"

# Build and push image
echo -e "${YELLOW}Building Docker image...${NC}"
docker build -t gcr.io/${PROJECT_ID}/dataspark .

echo -e "${YELLOW}Pushing image to Container Registry...${NC}"
docker push gcr.io/${PROJECT_ID}/dataspark

# Deploy to Cloud Run
echo -e "${YELLOW}Deploying to Cloud Run...${NC}"
gcloud run deploy dataspark \
  --image gcr.io/${PROJECT_ID}/dataspark \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10 \
  --set-env-vars PORT=8080 \
  --quiet

# Get the service URL
SERVICE_URL=$(gcloud run services describe dataspark --region ${REGION} --format 'value(status.url)')

echo ""
echo -e "${GREEN}✅ Deployment successful!${NC}"
echo -e "${GREEN}🌐 Service URL: ${SERVICE_URL}${NC}"
echo ""
echo -e "${YELLOW}⚠️  Don't forget to set your GEMINI_API_KEY as a secret:${NC}"
echo "   gcloud run services update dataspark --update-secrets=GEMINI_API_KEY=your-secret-name:latest --region ${REGION}"

