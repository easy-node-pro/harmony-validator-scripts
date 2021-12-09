import json
import subprocess
from subprocess import Popen, PIPE, run
from ast import literal_eval

# Set your shard # here
shard = 3

remote_shard_0 = ['/home/serviceharmony/harmony/hmy', 'blockchain', 'latest-headers', f'--node=https://api.s0.t.hmny.io']
result_remote_shard_0 = run(remote_shard_0, stdout=PIPE, stderr=PIPE, universal_newlines=True)
remote_data_shard_0 = json.loads(result_remote_shard_0.stdout)
remote_shard = ['/home/serviceharmony/harmony/hmy', 'blockchain', 'latest-headers', f'--node=https://api.s{shard}.t.hmny.io']
result_remote_shard = run(remote_shard, stdout=PIPE, stderr=PIPE, universal_newlines=True)
remote_data_shard = json.loads(result_remote_shard.stdout)
local_shard = ['/home/serviceharmony/harmony/hmy', 'blockchain', 'latest-headers']
result_local_shard = run(local_shard, stdout=PIPE, stderr=PIPE, universal_newlines=True)
local_data_shard = json.loads(result_local_shard.stdout)

print()
print(f"Shard {shard} Sync Status:")
print(f"Local Server  - Epoch {local_data_shard['result']['shard-chain-header']['epoch']} - Shard {local_data_shard['result']['shard-chain-header']['shardID']} - Block {literal_eval(local_data_shard['result']['shard-chain-header']['number'])}")
print(f"Remote Server - Epoch {remote_data_shard['result']['shard-chain-header']['epoch']} - Shard {remote_data_shard['result']['shard-chain-header']['shardID']} - Block {literal_eval(remote_data_shard['result']['shard-chain-header']['number'])}")
print()
print(f"Shard 0 Sync Status:")
print(f"Local Server  - Epoch {local_data_shard['result']['beacon-chain-header']['epoch']} - Shard {local_data_shard['result']['beacon-chain-header']['shardID']} - Block {literal_eval(local_data_shard['result']['beacon-chain-header']['number'])}")
print(f"Remote Server - Epoch {remote_data_shard_0['result']['shard-chain-header']['epoch']} - Shard {remote_data_shard_0['result']['shard-chain-header']['shardID']} - Block {literal_eval(remote_data_shard_0['result']['shard-chain-header']['number'])}")
print()
print(f"Local Server Stats, Shard {shard}:")
print("Beacon Chain Header:")
print(f"Epoch: {local_data_shard['result']['beacon-chain-header']['epoch']}")
print(f"Block: {literal_eval(local_data_shard['result']['beacon-chain-header']['number'])}")
print(f"Shard: {local_data_shard['result']['beacon-chain-header']['shardID']}")
print()
print("Shard Chain Header:")
print(f"Epoch: {local_data_shard['result']['shard-chain-header']['epoch']}")
print(f"Block: {literal_eval(local_data_shard['result']['shard-chain-header']['number'])}")
print(f"Shard: {local_data_shard['result']['shard-chain-header']['shardID']}")
print()
print(f"Remote Blockchain Stats, Shard {shard}:")
print("Beacon Chain Header:")
print(f"Epoch: {remote_data_shard['result']['beacon-chain-header']['epoch']}")
print(f"Block: {literal_eval(remote_data_shard['result']['beacon-chain-header']['number'])}")
print(f"Shard: {remote_data_shard['result']['beacon-chain-header']['shardID']}")
print()
print("Shard Chain Header:")
print(f"Epoch: {remote_data_shard['result']['shard-chain-header']['epoch']}")
print(f"Block: {literal_eval(remote_data_shard['result']['shard-chain-header']['number'])}")
print(f"Shard: {remote_data_shard['result']['shard-chain-header']['shardID']}")
print()
print(f"Remote Blockchain Stats, Shard 0:")
print("Beacon Chain Header:")
print(f"Epoch: {remote_data_shard_0['result']['beacon-chain-header']['epoch']}")
print(f"Block: {literal_eval(remote_data_shard_0['result']['beacon-chain-header']['number'])}")
print(f"Shard: {remote_data_shard_0['result']['beacon-chain-header']['shardID']}")
print()
print("Shard Chain Header:")
print(f"Epoch: {remote_data_shard_0['result']['shard-chain-header']['epoch']}")
print(f"Block: {literal_eval(remote_data_shard_0['result']['shard-chain-header']['number'])}")
print(f"Shard: {remote_data_shard_0['result']['shard-chain-header']['shardID']}")
print()
