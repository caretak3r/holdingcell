mkdir -p /opt/pydeps
cd /opt/pydeps
uv init
uv add gpu-benchmark


# install pyenv 
curl -fsSL https://pyenv.run | bash
