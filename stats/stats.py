import json
import subprocess
from subprocess import Popen, PIPE, run
from ast import literal_eval

# set these two settings here
ourShard = 3
harmonyFolder = '/home/serviceharmony/harmony'

# gathering information
countTrim = len(harmonyFolder) + 13
remote_shard_0 = [f'{harmonyFolder}/hmy', 'blockchain', 'latest-headers', '--node=https://api.s0.t.hmny.io']
result_remote_shard_0 = run(remote_shard_0, stdout=PIPE, stderr=PIPE, universal_newlines=True)
remote_data_shard_0 = json.loads(result_remote_shard_0.stdout)
remote_shard = [f'{harmonyFolder}/hmy', 'blockchain', 'latest-headers', f'--node=https://api.s{ourShard}.t.hmny.io']
result_remote_shard = run(remote_shard, stdout=PIPE, stderr=PIPE, universal_newlines=True)
remote_data_shard = json.loads(result_remote_shard.stdout)
local_shard = [f'{harmonyFolder}/hmy', 'blockchain', 'latest-headers']
result_local_shard = run(local_shard, stdout=PIPE, stderr=PIPE, universal_newlines=True)
local_data_shard = json.loads(result_local_shard.stdout)

# get database sizes
def getDBSize(ourShard) -> str:
    harmonyDBSize = subprocess.getoutput(f"du -h {harmonyFolder}/harmony_db_{ourShard}")
    harmonyDBSize = harmonyDBSize.rstrip('\t')
    return harmonyDBSize[:-countTrim]

# get shard stats
def shardStats(ourShard) -> str:
    ourUptime = subprocess.getoutput("uptime")
    ourVersion = subprocess.getoutput(f"{harmonyFolder}/harmony -V")
    dbZeroSize = getDBSize('0')
    if ourShard == "0":
        print(f"""
* Uptime :: {ourUptime}\n\n Harmony DB 0 Size  ::  {dbZeroSize}
* {ourVersion}
***
        """)
    else:
        print(f"""
* Uptime :: {ourUptime}

* Harmony DB 0 Size  ::  {dbZeroSize}
        """)
        if ourShard > 0:
            print(f"""
* Harmony DB {ourShard} Size  ::   {getDBSize(str(ourShard))}
            """)
        print(f"""
* {ourVersion}
***
        """)

print(f"""
***
* Shard 0 Sync Status:
* Local Server  - Epoch {local_data_shard['result']['beacon-chain-header']['epoch']} - Shard {local_data_shard['result']['beacon-chain-header']['shardID']} - Block {literal_eval(local_data_shard['result']['beacon-chain-header']['number'])}
* Remote Server - Epoch {remote_data_shard_0['result']['shard-chain-header']['epoch']} - Shard {remote_data_shard_0['result']['shard-chain-header']['shardID']} - Block {literal_eval(remote_data_shard_0['result']['shard-chain-header']['number'])}
***
""")
if ourShard > 0:
    print(f"""
***
* Shard {ourShard} Sync Status:
* Local Server  - Epoch {local_data_shard['result']['shard-chain-header']['epoch']} - Shard {local_data_shard['result']['shard-chain-header']['shardID']} - Block {literal_eval(local_data_shard['result']['shard-chain-header']['number'])}
* Remote Server - Epoch {remote_data_shard['result']['shard-chain-header']['epoch']} - Shard {remote_data_shard['result']['shard-chain-header']['shardID']} - Block {literal_eval(remote_data_shard['result']['shard-chain-header']['number'])}
***
    """)

# run it all
shardStats(ourShard)
