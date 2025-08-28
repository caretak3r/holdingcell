#!/bin/bash

# ==============================================================================
# Zsh, Oh My Zsh, and Powerlevel10k Setup Script
#
# This script automates the installation and configuration of Zsh, Oh My Zsh,
# the Powerlevel10k theme, and other useful plugins for a powerful shell
# experience on Ubuntu.
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
# 1. System Update and Prerequisite Installation
# ==============================================================================
log_info "Updating system packages and installing prerequisites..."
apt-get update -y
apt-get install -y zsh git curl wget

log_success "Prerequisites installed."

# ==============================================================================
# 2. Install Oh My Zsh
# ==============================================================================
log_info "Installing Oh My Zsh..."
if [ ! -d "/root/.oh-my-zsh" ]; then
    # The installer will back up an existing .zshrc and create a new one.
    # We use the --unattended flag to prevent it from trying to chsh.
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
    log_success "Oh My Zsh installed."
else
    log_warning "Oh My Zsh is already installed."
fi

# ==============================================================================
# 3. Change Default Shell to Zsh
# ==============================================================================
log_info "Changing the default shell for the root user to Zsh..."
if [[ "$SHELL" != */zsh ]]; then
    chsh -s "$(which zsh)"
    log_success "Default shell changed to Zsh. This will take effect on the next login."
else
    log_warning "Default shell is already Zsh."
fi

# ==============================================================================
# 4. Install Powerlevel10k Theme and Plugins
# ==============================================================================
log_info "Installing Powerlevel10k theme and plugins..."

# --- Define custom plugins directory ---
ZSH_CUSTOM=${ZSH_CUSTOM:-/root/.oh-my-zsh/custom}

# --- Install Powerlevel10k ---
if [ ! -d "${ZSH_CUSTOM}/themes/powerlevel10k" ]; then
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git "${ZSH_CUSTOM}/themes/powerlevel10k"
    log_success "Powerlevel10k theme installed."
else
    log_warning "Powerlevel10k theme is already installed."
fi

# --- Install zsh-autosuggestions ---
if [ ! -d "${ZSH_CUSTOM}/plugins/zsh-autosuggestions" ]; then
    git clone https://github.com/zsh-users/zsh-autosuggestions "${ZSH_CUSTOM}/plugins/zsh-autosuggestions"
    log_success "zsh-autosuggestions plugin installed."
else
    log_warning "zsh-autosuggestions plugin is already installed."
fi

# --- Install zsh-syntax-highlighting ---
if [ ! -d "${ZSH_CUSTOM}/plugins/zsh-syntax-highlighting" ]; then
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git "${ZSH_CUSTOM}/plugins/zsh-syntax-highlighting"
    log_success "zsh-syntax-highlighting plugin installed."
else
    log_warning "zsh-syntax-highlighting plugin is already installed."
fi

# ==============================================================================
# 5. Configure .zshrc
# ==============================================================================
log_info "Configuring .zshrc file..."

# --- Set the theme to Powerlevel10k ---
sed -i 's/ZSH_THEME=".*"/ZSH_THEME="powerlevel10k\/powerlevel10k"/' /root/.zshrc

# --- Add the plugins to the plugins list ---
sed -i 's/plugins=(git)/plugins=(\n  git\n  zsh-autosuggestions\n  zsh-syntax-highlighting\n)/' /root/.zshrc

log_success ".zshrc configured."

# ==============================================================================
# Finalization
# ==============================================================================
log_info "Zsh setup script finished!"
log_success "Your shell environment has been upgraded."
log_warning "IMPORTANT: To apply changes, you must log out and log back in, or start a new zsh session."

log_info "First-Time Setup for Powerlevel10k:"
echo "---------------------------------------------------------------------------------"
echo "The first time you start Zsh, the Powerlevel10k configuration wizard will run."
echo "You can also run it manually at any time with the command:"
echo "   p10k configure"
echo ""
echo "Follow the prompts to customize your shell's appearance."
echo "---------------------------------------------------------------------------------"

