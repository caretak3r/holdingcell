#!/bin/bash

# K3s Cluster Verification Script
# This script verifies that k3s is running and can create/delete basic Kubernetes objects

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Set KUBECONFIG
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

print_status "Starting K3s cluster verification..."

# Check if k3s is installed
if ! command -v k3s &> /dev/null; then
    print_error "k3s is not installed"
    exit 1
fi
print_success "k3s is installed at $(which k3s)"

# Check if k3s service is running
if ! systemctl is-active --quiet k3s; then
    print_error "k3s service is not running"
    print_warning "Attempting to start k3s..."
    sudo systemctl start k3s
    if ! systemctl is-active --quiet k3s; then
        print_error "Failed to start k3s service"
        exit 1
    fi
fi
print_success "k3s service is running"

# Check kubectl access to cluster
if ! kubectl cluster-info &> /dev/null; then
    print_error "Cannot access kubernetes cluster"
    exit 1
fi
print_success "kubectl can access the cluster"

# Display cluster info
print_status "Cluster nodes:"
kubectl get nodes

print_status "Existing pods in all namespaces:"
kubectl get pods -A

# Test 1: Deploy busybox pod
print_status "Deploying busybox pod..."
kubectl run busybox --image=busybox:1.36 --restart=Never -- sleep 3600

# Wait for pod to be ready
print_status "Waiting for busybox pod to be ready..."
kubectl wait --for=condition=Ready pod/busybox --timeout=60s

print_status "Busybox pod details:"
kubectl describe pod busybox

# Test 2: Create secret
print_status "Creating test secret..."
kubectl create secret generic test-secret --from-literal=username=admin --from-literal=password=secret123

print_status "Listing secrets:"
kubectl get secrets

# Test 3: Create configmap
print_status "Creating test configmap..."
kubectl create configmap test-config --from-literal=app.name=test-app --from-literal=app.version=1.0

print_status "Listing configmaps:"
kubectl get configmaps

# Test 4: Create namespace
print_status "Creating test namespace..."
kubectl create namespace test-namespace

# Test 5: Create deployment
print_status "Creating nginx deployment in test namespace..."
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: test-namespace
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
EOF

print_status "Checking deployment status..."
kubectl get all -n test-namespace

# Wait for deployment to be ready
print_status "Waiting for nginx deployment to be ready..."
kubectl wait --for=condition=Available deployment/nginx-deployment -n test-namespace --timeout=120s

print_success "All tests passed! K3s cluster is working correctly."

# Cleanup
print_status "Starting cleanup..."

print_status "Deleting busybox pod..."
kubectl delete pod busybox

print_status "Deleting test secret..."
kubectl delete secret test-secret

print_status "Deleting test configmap..."
kubectl delete configmap test-config

print_status "Deleting test namespace (and all resources in it)..."
kubectl delete namespace test-namespace

print_success "Cleanup completed successfully!"
print_success "K3s cluster verification complete - everything is working as expected!"
