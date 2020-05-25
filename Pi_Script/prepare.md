```
# echo 'Acquire::http { Proxy "http://apt-proxy.iiitb.me:3142/"; }' | sudo tee -a /etc/apt/apt.conf.d/proxy
# sudo su
# apt update && apt upgrade
# reboot

# Install Nexmon dependencies
sudo apt install -y raspberrypi-kernel-headers git libgmp3-dev gawk qpdf bison flex make automake autoconf texinfo libtool tcpdump screen

# Clone Nexmon from gitlab server
git clone --depth=1 https://github.com/seemoo-lab/nexmon.git
cd nexmon
NEXROOT=$(pwd)

# build libISL
cd $NEXROOT/buildtools/isl-0.10
autoreconf -f -i
./configure
make
make install
ln -s /usr/local/lib/libisl.so /usr/lib/arm-linux-gnueabihf/libisl.so.10

# Build libMPFR
cd $NEXROOT/buildtools/mpfr-3.1.4
autoreconf -f -i
./configure
make
make install
ln -s /usr/local/lib/libmpfr.so /usr/lib/arm-linux-gnueabihf/libmpfr.so.4

# Setup build environment for compiling patches
cd $NEXROOT
source setup_env.sh
make

# Install Nexmon CSI
cd $NEXROOT/patches/bcm43455c0/7_45_189/
git clone --depth=1 https://github.com/seemoo-lab/nexmon_csi.git
cd nexmon_csi
make backup-firmware
make install-firmware

# Install Nexutil
cd $NEXROOT/utilities/nexutil/
make
make install

# Install MakeCSIParams
cd $NEXROOT/patches/bcm43455c0/7_45_189/nexmon_csi/utils/makecsiparams
make
ln -s $PWD/makecsiparams /usr/local/bin/mcp

# # Load modified firmware on reboot
# mv /lib/modules/4.19.93-v7+/kernel/drivers/net/wireless/broadcom/brcm80211/brcmfmac/brcmfmac.ko $NEXROOT/patches/bcm43455c0/7_45_189/nexmon_csi/brcmfmac_4.19.y-nexmon/brcmfmac.ko.orig
# cp $NEXROOT/patches/bcm43455c0/7_45_189/nexmon_csi/brcmfmac_4.19.y-nexmon/brcmfmac.ko /lib/modules/4.19.93-v7+/kernel/drivers/net/wireless/broadcom/brcm80211/brcmfmac/brcmfmac.ko
# depmod -a
```