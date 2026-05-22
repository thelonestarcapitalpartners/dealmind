#!/usr/bin/env bash
set -e

# Usage: ./scripts/build_and_push_image.sh ghcr.io/<org>/dealmind-backend:latest
IMAGE=${1:-}
if [ -z "$IMAGE" ]; then
  echo "Usage: $0 <image:tag>"
  exit 1
fi

# Build prod image
docker build -f backend/Dockerfile.prod -t $IMAGE .

# Push
docker push $IMAGE

echo "Pushed $IMAGE"
