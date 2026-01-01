#!/bin/bash
# Local Cookbook - System Resource Checker (Bash Wrapper)
# Quick system check script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "Local Cookbook - System Check (Bash)"
echo "=========================================="
echo ""

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed. Please install uv first."
    exit 1
fi

# Check if Python package is installed
if [ ! -f "pyproject.toml" ]; then
    echo "Installing dependencies..."
    uv sync
fi

# Quick GPU check
echo "=== GPU Check ==="
if command -v nvidia-smi &> /dev/null; then
    echo "NVIDIA GPUs detected:"
    nvidia-smi --query-gpu=index,name,memory.total --format=csv,noheader | \
        awk -F',' '{printf "  GPU %s: %s (%s)\n", $1, $2, $3}'
    TOTAL_VRAM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | \
        awk '{sum+=$1} END {printf "%.2f", sum/1024}')
    echo "  Total VRAM: ${TOTAL_VRAM} GB"
else
    echo "  No NVIDIA GPUs detected (nvidia-smi not found)"
fi
echo ""

# Quick CPU check
echo "=== CPU Check ==="
if [ -f /proc/cpuinfo ]; then
    CPU_MODEL=$(grep -m1 "model name" /proc/cpuinfo | cut -d':' -f2 | sed 's/^ *//')
    PHYSICAL_CORES=$(grep -c "^processor" /proc/cpuinfo)
    echo "  Model: $CPU_MODEL"
    echo "  Cores: $PHYSICAL_CORES"
elif command -v sysctl &> /dev/null; then
    CPU_MODEL=$(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo "Unknown")
    PHYSICAL_CORES=$(sysctl -n hw.physicalcpu 2>/dev/null || echo "Unknown")
    echo "  Model: $CPU_MODEL"
    echo "  Cores: $PHYSICAL_CORES"
fi
echo ""

# Quick Memory check
echo "=== Memory Check ==="
if command -v free &> /dev/null; then
    TOTAL_MEM=$(free -g | grep Mem | awk '{print $2}')
    AVAIL_MEM=$(free -g | grep Mem | awk '{print $7}')
    echo "  Total RAM: ${TOTAL_MEM} GB"
    echo "  Available RAM: ${AVAIL_MEM} GB"
elif command -v vm_stat &> /dev/null; then
    # macOS
    TOTAL_MEM=$(sysctl -n hw.memsize | awk '{printf "%.2f", $1/1024/1024/1024}')
    echo "  Total RAM: ${TOTAL_MEM} GB"
else
    echo "  Could not determine memory (install 'free' or check manually)"
fi
echo ""

# Run full Python check
echo "=========================================="
echo "Running Full Compatibility Check..."
echo "=========================================="
echo ""

if [ -f "local_cookbook/main.py" ]; then
    uv run python -m local_cookbook.main check
else
    echo "Python modules not found. Installing..."
    uv sync
    uv run python -m local_cookbook.main check
fi
