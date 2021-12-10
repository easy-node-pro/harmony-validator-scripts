import json
import subprocess
from subprocess import Popen, PIPE, run
from ast import literal_eval

ourShard = 3
harmonyPath = '/home/serviceharmony/harmony/hmy'

remote_shard_0 = [harmonyPath, 'blockchain', 'latest-headers', '--node=https://api.s0.t.hmny.io']
result_remote_shard_0 = run(remote_shard_0, stdout=PIPE, stderr=PIPE, universal_newlines=True)
remote_data_shard_0 = json.loads(result_remote_shard_0.stdout)
remote_shard = [harmonyPath, 'blockchain', 'latest-headers', f'--node=https://api.s{ourShard}.t.hmny.io']
result_remote_shard = run(remote_shard, stdout=PIPE, stderr=PIPE, universal_newlines=True)
remote_data_shard = json.loads(result_remote_shard.stdout)
local_shard = [harmonyPath, 'blockchain', 'latest-headers']
result_local_shard = run(local_shard, stdout=PIPE, stderr=PIPE, universal_newlines=True)
local_data_shard = json.loads(result_local_shard.stdout)
print(f"""
Shard 0 Sync Status:
Local Server  - Epoch {local_data_shard['result']['beacon-chain-header']['epoch']} - Shard {local_data_shard['result']['beacon-chain-header']['shardID']} - Block {literal_eval(local_data_shard['result']['beacon-chain-header']['number'])}
Remote Server - Epoch {remote_data_shard_0['result']['shard-chain-header']['epoch']} - Shard {remote_data_shard_0['result']['shard-chain-header']['shardID']} - Block {literal_eval(remote_data_shard_0['result']['shard-chain-header']['number'])}
""")
if ourShard > 0:
    print(f"""
Shard {ourShard} Sync Status:
Local Server  - Epoch {local_data_shard['result']['shard-chain-header']['epoch']} - Shard {local_data_shard['result']['shard-chain-header']['shardID']} - Block {literal_eval(local_data_shard['result']['shard-chain-header']['number'])}
Remote Server - Epoch {remote_data_shard['result']['shard-chain-header']['epoch']} - Shard {remote_data_shard['result']['shard-chain-header']['shardID']} - Block {literal_eval(remote_data_shard['result']['shard-chain-header']['number'])}
    """)
print(f"""
Local Server Stats, Shard {ourShard}:
Beacon Chain Header:
Epoch: {local_data_shard['result']['beacon-chain-header']['epoch']}
Block: {literal_eval(local_data_shard['result']['beacon-chain-header']['number'])}
Shard: {local_data_shard['result']['beacon-chain-header']['shardID']}

Shard Chain Header:
Epoch: {local_data_shard['result']['shard-chain-header']['epoch']}
Block: {literal_eval(local_data_shard['result']['shard-chain-header']['number'])}
Shard: {local_data_shard['result']['shard-chain-header']['shardID']}

Remote Blockchain Stats, Shard {ourShard}:
Beacon Chain Header:
Epoch: {remote_data_shard['result']['beacon-chain-header']['epoch']}
Block: {literal_eval(remote_data_shard['result']['beacon-chain-header']['number'])}
Shard: {remote_data_shard['result']['beacon-chain-header']['shardID']}

Shard Chain Header:
Epoch: {remote_data_shard['result']['shard-chain-header']['epoch']}
Block: {literal_eval(remote_data_shard['result']['shard-chain-header']['number'])}
Shard: {remote_data_shard['result']['shard-chain-header']['shardID']}

Remote Blockchain Stats, Shard 0:
Beacon Chain Header:
Epoch: {remote_data_shard_0['result']['beacon-chain-header']['epoch']}
Block: {literal_eval(remote_data_shard_0['result']['beacon-chain-header']['number'])}
Shard: {remote_data_shard_0['result']['beacon-chain-header']['shardID']}

Shard Chain Header:
Epoch: {remote_data_shard_0['result']['shard-chain-header']['epoch']}
Block: {literal_eval(remote_data_shard_0['result']['shard-chain-header']['number'])}
Shard: {remote_data_shard_0['result']['shard-chain-header']['shardID']}
""")
