sudo add-apt-repository ppa:graphics-drivers/ppa --yes
sudo apt update
sudo apt install nvidia-driver-575

dpkg-query -W --showformat='${Package} ${Status}\n' | grep -v deinstall | awk '{ print $1 }' | \
    grep -E 'nvidia.*-[0-9]+$' | \
    xargs -r -L 1 sudo apt-mark hold


sudo apt install --fix-broken
sudo dpkg --configure -a
sudo apt install --fix-broken


sudo apt-get remove --purge '^nvidia-.*'
sudo apt-get remove --purge '^libnvidia-.*'
sudo apt-get remove --purge '^cuda-.*'


# Mark unhold
dpkg-query -W --showformat='${Package} ${Status}\n' | grep -v deinstall | awk '{ print $1 }' | \
    grep -E 'nvidia.*-[0-9]+$' | \
    xargs -r -L 1 sudo apt-mark unhold

# Upgrade driver
sudo modprobe -r -f $(lsmod | grep '^nvidia' | awk '{ print $1 }')
sudo apt update && sudo apt upgrade
nvidia-smi

# Mark hold again
dpkg-query -W --showformat='${Package} ${Status}\n' | grep -v deinstall | awk '{ print $1 }' | \
    grep -E 'nvidia.*-[0-9]+$' | \
    xargs -r -L 1 sudo apt-mark hold
