#!/bin/bash

# Exit on error
set -e

export NAME="eips/web"
export NAMESPACE="eips"
export CONTAINER_NAME="eips-web"
export DEPLOYMENT_NAME="$NAMESPACE-eips-web"

# Figure out our docker tags
export BUILD_ID="$(date +%Y%m%d%H%M%S)"
export REGISTRY="image.mikes.network/$NAME"
export TAG="$REGISTRY:$BUILD_ID"

echo "Building $TAG..."

# Build & send it
docker build -f devops/dockerfiles/Dockerfile.web -t $TAG .
docker tag $TAG $REGISTRY:latest
docker push $TAG
docker push $REGISTRY:latest

echo "Setting image for deployment/$DEPLOYMENT_NAME to $DEPLOYMENT_NAME=$TAG"
kubectl -n $NAMESPACE set image deployment/$DEPLOYMENT_NAME $CONTAINER_NAME=$TAG

echo "Complete"