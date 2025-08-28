#!/bin/bash

# ==============================================================================
# Top500 Benchmark Local Runner
#
# This script automates the setup and execution of the geerlingguy/top500-benchmark
# project on a single Ubuntu machine (localhost). It handles dependency
# installation, repository cloning, compilation, and execution of the HPL benchmark.
#
# It is designed to be run as the root user.
# ==============================================================================

# --- Exit immediately if a command exits with a non-zero status ---
set -e

# --- Helper Functions for logging ---
log_info() {
    echo -e "\n[INFO] --------------------------------------------------"
    echo -e "[INFO] $1"
    echo -e "[INFO] --------------------------------------------------"
}

log_success() {
    echo -e "[SUCCESS] $1"
}

log_warning() {
    echo -e "[WARNING] $1"
}

log_error() {
    echo -e "[ERROR] $1" >&2
    exit 1
}

# ==============================================================================
# 1. System Update and Dependency Installation
# ==============================================================================
log_info "Updating system packages and installing benchmark dependencies..."
apt-get update -y
# --- HPL benchmark requires a Fortran compiler, MPI libraries, and build tools ---
apt-get install -y git build-essential gfortran openmpi-bin libopenmpi-dev automake autoconf

log_success "Dependencies installed."

# ==============================================================================
# 2. Clone the Benchmark Repository
# ==============================================================================
log_info "Cloning the top500-benchmark repository..."
REPO_DIR="/opt/top500-benchmark"
if [ ! -d "$REPO_DIR" ]; then
    git clone https://github.com/geerlingguy/top500-benchmark.git "$REPO_DIR"
    log_success "Repository cloned to $REPO_DIR."
else
    log_warning "Repository directory already exists. Skipping clone."
fi

cd "$REPO_DIR"

# ==============================================================================
# 3. Compile the HPL Benchmark
# ==============================================================================
log_info "Compiling the High-Performance Linpack (HPL) benchmark..."
# --- The make command will build the xhpl executable ---
make arch=Linux_PII_FBLAS

# --- Verify that the executable was created ---
if [ ! -f "bin/Linux_PII_FBLAS/xhpl" ]; then
    log_error "HPL compilation failed. The xhpl executable was not found."
fi

log_success "HPL benchmark compiled successfully."

# ==============================================================================
# 4. Run the Benchmark
# ==============================================================================
log_info "Running the HPL benchmark..."
log_warning "This process can be CPU-intensive and may take a significant amount of time."

# --- Use mpirun to execute the compiled benchmark ---
# The -np flag specifies the number of processes. We'll use the number of available cores.
NUM_CORES=$(nproc)
log_info "Using $NUM_CORES processes for the benchmark."

mpirun --allow-run-as-root -np "$NUM_CORES" bin/Linux_PII_FBLAS/xhpl

# ==============================================================================
# Finalization
# ==============================================================================
log_info "Benchmark finished!"
log_success "The results are displayed above. Look for the Gflops value."

