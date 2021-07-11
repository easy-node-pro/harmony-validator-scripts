# harmony-validator-scripts
Scripts that go with our [Slugom.ONE Harmony ONE Validator Guide](https://guides.slugomcrypto.com "Slugom.ONE Harmony ONE Validator Guide") to help you more easily setup your node.

### Create a stats.sh script the easy way
This will download and install your stats.sh script to use later to check your block status. Choose only the shard you're going to run on below:

`wget https://raw.githubusercontent.com/slugom-crypto/harmony-validator-scripts/main/stats/shard_0.sh && mv shard_0.sh stats.sh && chmod +x stats.sh`

`wget https://raw.githubusercontent.com/slugom-crypto/harmony-validator-scripts/main/stats/shard_0.sh && mv shard_1.sh stats.sh && chmod +x stats.sh`

`wget https://raw.githubusercontent.com/slugom-crypto/harmony-validator-scripts/main/stats/shard_0.sh && mv shard_2.sh stats.sh && chmod +x stats.sh`

`wget https://raw.githubusercontent.com/slugom-crypto/harmony-validator-scripts/main/stats/shard_0.sh && mv shard_3.sh stats.sh && chmod +x stats.sh`

### Create a upgrade_harmony.sh script the easy way
This will download and install your upgrade_harmony.sh script to use later to backup, upgrade harmony, dump a new harmony.conf file and restart your service. **Only download and run this script if you use *~/harmony* as a folder** for your files on your nodes:

`wget https://raw.githubusercontent.com/slugom-crypto/harmony-validator-scripts/main/upgrade/upgrade_harmony.sh && chmod +x upgrade_harmony.sh`