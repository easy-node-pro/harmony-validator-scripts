#! /bin/bash
mkdir -p ~/harmony/harmony_backup
cp ~/harmony/harmony ~/harmony/harmony_backup
cd ~/harmony
curl -LO https://harmony.one/binary && mv binary harmony && chmod +x harmony
./harmony -V
./harmony dumpconfig harmony.conf
sudo service harmony restart
sleep 10
./stats.sh