# harmony-validator-scripts
Created by Patrick @ [Slugom.ONE](https://Slugom.ONE "Slugom.ONE").

Scripts that go with our [Slugom.ONE Harmony ONE Validator Guide](https://guides.slugomcrypto.com "Slugom.ONE Harmony ONE Validator Guide") to help you more easily setup your node.

### node-quickstart
This is a template to use to build a markdown file to use when setting up nodes in the future.

### stats - This contains our versions of the stats.sh script in our guide.
The commands below will download and install our stats.sh script to use later to check your stats including cpu, disk, harmony version & block status. 
Choose only the shard you're going to run on below 0-3:

`wget https://raw.githubusercontent.com/slugom-crypto/harmony-validator-scripts/main/stats/shard_0.sh && mv shard_0.sh stats.sh && chmod +x stats.sh`

`wget https://raw.githubusercontent.com/slugom-crypto/harmony-validator-scripts/main/stats/shard_1.sh && mv shard_1.sh stats.sh && chmod +x stats.sh`

`wget https://raw.githubusercontent.com/slugom-crypto/harmony-validator-scripts/main/stats/shard_2.sh && mv shard_2.sh stats.sh && chmod +x stats.sh`

`wget https://raw.githubusercontent.com/slugom-crypto/harmony-validator-scripts/main/stats/shard_3.sh && mv shard_3.sh stats.sh && chmod +x stats.sh`

### systemd 
This contains our systemd file harmony.service that we use with our [Slugom.ONE Harmony ONE Validator Guide](https://guides.slugomcrypto.com "Slugom.ONE Harmony ONE Validator Guide") - Only use this if you setup a user named serviceharmony and keep your harmony binary at ~/harmony/harmony

### upgrade - This contains our version of the upgrade_harmony.sh script in our guide.
This will download and install your upgrade_harmony.sh script to use later to backup, upgrade harmony, dump a new harmony.conf file and restart your service. **Only download and run this script if you use *~/harmony* as a folder** for your files on your nodes:

`wget https://raw.githubusercontent.com/slugom-crypto/harmony-validator-scripts/main/upgrade/upgrade_harmony.sh && chmod +x upgrade_harmony.sh`
