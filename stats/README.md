# stats 
### This contains our versions of the stats.sh script in our guide.
The commands below will download and install our stats.sh script to use later to check your stats including cpu, disk, harmony version & block status. Choose only the shard you're going to run on below 0-3:

wget https://raw.githubusercontent.com/slugom-crypto/harmony-validator-scripts/main/stats/shard_0.sh && mv shard_0.sh stats.sh && chmod +x stats.sh

wget https://raw.githubusercontent.com/slugom-crypto/harmony-validator-scripts/main/stats/shard_1.sh && mv shard_1.sh stats.sh && chmod +x stats.sh

wget https://raw.githubusercontent.com/slugom-crypto/harmony-validator-scripts/main/stats/shard_2.sh && mv shard_2.sh stats.sh && chmod +x stats.sh

wget https://raw.githubusercontent.com/slugom-crypto/harmony-validator-scripts/main/stats/shard_3.sh && mv shard_3.sh stats.sh && chmod +x stats.sh

### Customizations
- Current scripts in this repo will only work in the same folder with your harmony binary file.
- Feel free to upgrade the contents of the script for your environment so they can run from any location.