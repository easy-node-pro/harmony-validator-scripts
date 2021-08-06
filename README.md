# EasyNode.ONE Presents "The EasyNode.ONE Admin Companion Guide Repository"
Created by Patrick @ [EasyNode.ONE](http://EasyNode.ONE "EasyNode.ONE").

Scripts that go with our [EasyNode.ONE Harmony ONE Validator Guide](https://guides.easynode.one "EasyNode.ONE Harmony ONE Validator Guide") to help you more easily setup your node.

## Here's a breakdown of each folder's contents:

### node-quickstart
This is a template to use to build a markdown file to use when setting up nodes in the future.

### rclone.conf
This contains a copy of our rclone file configured for any node. To be used for remote installations.

### stats
This contains our versions of the stats.sh script in our guide. 

The commands below will download and install our stats.sh script to use later to check your stats including cpu, disk, harmony version & block status. 

Choose only the shard you're going to run on below 0-3:

`wget https://raw.githubusercontent.com/easy-node-one/harmony-validator-scripts/main/stats/shard_0.sh && mv shard_0.sh stats.sh && chmod +x stats.sh`

`wget https://raw.githubusercontent.com/easy-node-one/harmony-validator-scripts/main/stats/shard_1.sh && mv shard_1.sh stats.sh && chmod +x stats.sh`

`wget https://raw.githubusercontent.com/easy-node-one/harmony-validator-scripts/main/stats/shard_2.sh && mv shard_2.sh stats.sh && chmod +x stats.sh`

`wget https://raw.githubusercontent.com/easy-node-one/harmony-validator-scripts/main/stats/shard_3.sh && mv shard_3.sh stats.sh && chmod +x stats.sh`

### systemd 
This contains our systemd service file pre-configured for the user serviceharmony. To be used for remote installations.

### upgrade
This contains our version of the upgrade_harmony.sh script in our guide. Use the command below in the same directory with your harmony binary to download a copy of our script. Run this when updates to harmony are required by the developers by running `./upgrade_harmony.sh`

`wget https://raw.githubusercontent.com/easy-node-one/harmony-validator-scripts/main/upgrade/upgrade_harmony.sh && chmod +x upgrade_harmony.sh`
