#!/bin/bash

# ==============================================================================
# LLM Local Setup Script
#
# This script installs the necessary dependencies to run Large Language Models
# (LLMs) locally on an Ubuntu server with an NVIDIA GPU. It installs Python,
# the CUDA Toolkit, PyTorch, and other essential libraries.
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

# --- Function to check if a command exists ---
command_exists() {
    command -v "$1" &> /dev/null
}

# ==============================================================================
# 1. System Update & Build Dependencies
# ==============================================================================
log_info "Updating system packages and installing build dependencies for Python..."
apt-get update -y
# --- Dependencies for Python compilation ---
apt-get install -y \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    curl \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    wget \
    gnupg \
    software-properties-common

log_success "System packages and build dependencies updated."

# ==============================================================================
# 2. Install Python 3.13.7 from Source & Install UV
# ==============================================================================
log_info "Installing Python 3.13.7 from source..."
PYTHON_VERSION="3.13.7"
if ! command_exists python${PYTHON_VERSION%.*}; then
    cd /tmp
    wget "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz"
    tar -xf "Python-${PYTHON_VERSION}.tgz"
    cd "Python-${PYTHON_VERSION}"
    ./configure --enable-optimizations
    make -j$(nproc)
    # Use altinstall to avoid replacing the system's default python3
    make altinstall
    cd /
    rm -rf /tmp/Python-${PYTHON_VERSION}*
    log_success "Python ${PYTHON_VERSION} installed successfully."
else
    log_warning "Python ${PYTHON_VERSION%.*} appears to be already installed."
fi

# --- Verify installation ---
command_exists python${PYTHON_VERSION%.*} || log_error "Python ${PYTHON_VERSION} installation failed."
PY_EXECUTABLE=$(which python${PYTHON_VERSION%.*})
${PY_EXECUTABLE} --version

log_info "Installing uv package manager..."
curl -LsSf https://astral.sh/uv/install.sh | sh
source /root/.cargo/env
command_exists uv || log_error "uv installation failed."
log_success "uv installed successfully."
uv --version


# ==============================================================================
# 3. Install NVIDIA CUDA Toolkit & Detect GPU
# ==============================================================================
log_info "Checking for NVIDIA GPU and installing CUDA Toolkit if found..."

# --- Check for NVIDIA GPU ---
if ! lspci | grep -i nvidia; then
    log_error "No NVIDIA GPU detected. This script requires an NVIDIA GPU for local LLM acceleration."
    exit 1
fi

log_info "NVIDIA GPU detected. Identifying model..."
# The nvidia-smi command is available after the driver is installed.
# The first setup script should handle driver installation.
if command_exists nvidia-smi; then
    nvidia-smi -L
else
    log_warning "nvidia-smi command not found. Cannot list GPU model. Please ensure NVIDIA drivers are installed."
fi


if ! command_exists nvcc; then
    log_info "Installing CUDA Toolkit..."
    # --- Install CUDA Toolkit from NVIDIA's official repository ---
    # Reference: https://developer.nvidia.com/cuda-downloads
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
    dpkg -i cuda-keyring_1.1-1_all.deb
    rm cuda-keyring_1.1-1_all.deb
    apt-get update
    apt-get -y install cuda-toolkit-12-5

    # --- Add CUDA to the PATH for the root user ---
    echo 'export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}' >> /root/.bashrc
    echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}' >> /root/.bashrc
    export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
    export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
    
    log_success "NVIDIA CUDA Toolkit installed. A reboot is highly recommended."
else
    log_warning "NVIDIA CUDA Toolkit (nvcc) is already installed."
fi

# --- Verify installation ---
command_exists nvcc || log_error "CUDA Toolkit installation failed."
log_success "CUDA Toolkit is ready."
nvcc --version

# ==============================================================================
# 4. Install Python LLM Libraries using UV
# ==============================================================================
log_info "Installing essential Python libraries for LLMs using uv..."

# --- Create a virtual environment for the LLM packages ---
uv venv /opt/llm_env --python ${PY_EXECUTABLE}
# --- Install packages into the new environment ---
/opt/llm_env/bin/uv pip install \
    torch \
    torchvision \
    torchaudio \
    --index-url https://download.pytorch.org/whl/cu121

# --- Install Hugging Face and other supporting libraries ---
/opt/llm_env/bin/uv pip install \
    transformers \
    accelerate \
    bitsandbytes \
    sentencepiece

log_success "Core Python LLM libraries installed successfully in /opt/llm_env."

# ==============================================================================
# Finalization
# ==============================================================================
log_info "LLM setup script finished!"
log_success "Your server is now equipped to run local LLMs with Python ${PYTHON_VERSION}."
log_warning "A REBOOT IS STRONGLY RECOMMENDED to ensure the NVIDIA driver and CUDA toolkit are loaded correctly."
log_info "Next Steps:"
echo "1. Activate the Python environment: source /opt/llm_env/bin/activate"
echo "2. Write and run a Python script to download and use a model from the Hugging Face Hub."
echo "3. To deactivate the environment, simply run: deactivate"

