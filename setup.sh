#!/bin/bash

# ==============================================================================
# Ubuntu Server Setup Script
#
# This script automates the installation and configuration of essential
# development tools, Kubernetes utilities, NVIDIA drivers, and other useful
# packages on a fresh Ubuntu server.
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
# 1. System Update and Upgrade
# ==============================================================================
log_info "Updating and upgrading system packages..."
apt-get update -y
apt-get upgrade -y
apt-get install -y software-properties-common curl wget gpg apt-transport-https ca-certificates lsb-release

log_success "System packages updated and upgraded."

# ==============================================================================
# 2. Install Essential Development Tools
# ==============================================================================
log_info "Installing essential development tools (build-essential, git, golang)..."
apt-get install -y build-essential git

# --- Install Golang ---
if ! command_exists go; then
    GOLANG_VERSION="1.22.5"
    ARCH=$(dpkg --print-architecture)
    case "$ARCH" in
        amd64) GO_ARCH="amd64" ;;
        arm64) GO_ARCH="arm64" ;;
        *) log_error "Unsupported architecture: $ARCH for Golang installation." ;;
    esac

    wget "https://golang.org/dl/go${GOLANG_VERSION}.linux-${GO_ARCH}.tar.gz" -O /tmp/go.tar.gz
    tar -C /usr/local -xzf /tmp/go.tar.gz
    rm /tmp/go.tar.gz

    # --- Add Go to PATH for the root user ---
    echo 'export PATH=$PATH:/usr/local/go/bin' >> /root/.bashrc
    export PATH=$PATH:/usr/local/go/bin
    log_success "Golang added to PATH."
else
    log_warning "Golang is already installed."
fi

# --- Verify installations ---
command_exists gcc || log_error "GCC (build-essential) installation failed."
command_exists git || log_error "Git installation failed."
command_exists go || log_error "Golang installation failed."
log_success "Essential development tools installed."
go version

# ==============================================================================
# 3. Install Oh My Bash
# ==============================================================================
log_info "Installing Oh My Bash..."
if [ ! -d "/root/.oh-my-bash" ]; then
    bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)" --unattended
    # Use bash as the default shell for root
    chsh -s /bin/bash root
    log_success "Oh My Bash installed."
else
    log_warning "Oh My Bash is already installed."
fi

# ==============================================================================
# 4. Install Kubernetes Tools (kubectl, helm)
# ==============================================================================
log_info "Installing Kubernetes tools (kubectl, helm)..."

# --- Install kubectl ---
if ! command_exists kubectl; then
    curl -fsSL "https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key" | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
    echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /' | tee /etc/apt/sources.list.d/kubernetes.list
    apt-get update -y
    apt-get install -y kubectl
    log_success "kubectl installed."
else
    log_warning "kubectl is already installed."
fi

# --- Install Helm ---
if ! command_exists helm; then
    curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | tee /usr/share/keyrings/helm.gpg > /dev/null
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | tee /etc/apt/sources.list.d/helm-stable-debian.list
    apt-get update -y
    apt-get install -y helm
    log_success "Helm installed."
else
    log_warning "Helm is already installed."
fi

# --- Verify installations ---
command_exists kubectl || log_error "kubectl installation failed."
command_exists helm || log_error "Helm installation failed."
log_success "Kubernetes tools installed."
kubectl version --client
helm version

# ==============================================================================
# 5. Install Kubernetes Dependencies (Containerd)
# ==============================================================================
log_info "Installing Kubernetes dependencies (containerd)..."
if ! command_exists containerd; then
    apt-get install -y containerd
    # Configure containerd
    mkdir -p /etc/containerd
    containerd config default | tee /etc/containerd/config.toml
    # Set systemd as the cgroup driver
    sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
    systemctl restart containerd
    systemctl enable containerd
    log_success "containerd installed and configured."
else
    log_warning "containerd seems to be already installed."
fi

# --- Verify installation ---
systemctl is-active --quiet containerd || log_error "containerd service is not running."
log_success "Kubernetes dependencies installed."

# ==============================================================================
# 6. Install NVIDIA Drivers and nvtop
# ==============================================================================
log_info "Checking for NVIDIA GPU and installing drivers if found..."

# --- Check for NVIDIA GPU ---
if lspci | grep -i nvidia; then
    log_info "NVIDIA GPU detected. Installing drivers..."
    # Add the official graphics-drivers PPA
    add-apt-repository ppa:graphics-drivers/ppa -y
    apt-get update -y

    # Install recommended drivers
    ubuntu-drivers autoinstall
    log_success "NVIDIA drivers installed. A reboot is recommended to load them properly."

    # --- Install nvtop ---
    log_info "Installing nvtop..."
    apt-get install -y nvtop
    command_exists nvtop || log_error "nvtop installation failed."
    log_success "nvtop installed."

else
    log_warning "No NVIDIA GPU detected. Skipping driver installation."
fi

# ==============================================================================
# 7. Install Homebrew
# ==============================================================================
log_info "Installing Homebrew..."
if ! command_exists brew; then
    # Homebrew installation needs to be run as a non-root user, but we can install it for root.
    # We will execute the script under a temporary user if needed, or directly if the script allows.
    # The official installer handles this by prompting. We automate it.
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" < /dev/null

    # Add Homebrew to the root user's PATH
    (echo; echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"') >> /root/.bashrc
    eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
    log_success "Homebrew installed and configured for the root user."
else
    log_warning "Homebrew is already installed."
fi

# --- Verify installation ---
command_exists brew || log_error "Homebrew installation failed."
log_success "Homebrew is ready to use."

# ==============================================================================
# Finalization
# ==============================================================================
log_info "Setup script finished!"
log_success "All tools have been installed and configured."
log_warning "Please reboot the server to ensure all changes, especially NVIDIA drivers, are applied correctly."
log_info "To start using the new environment, run: source /root/.bashrc"
