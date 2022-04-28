import json
import subprocess
import os
import sys
from colorama import Style
from subprocess import Popen, PIPE, run
from ast import literal_eval
from datetime import datetime

# set these two settings here
ourShard = "3"
harmonyFolder = '/home/serviceharmony/harmony'

# print stuff
class PrintStuff:

    def __init__(self, reset: int=0):
        self.reset = reset
        self.print_stars = "*" * 93
        self.reset_stars = self.print_stars + Style.RESET_ALL

    def printStars(self) -> None:        
        p = self.print_stars
        if self.reset:
            p = self.reset_stars
        print(p)
        
    def stringStars(self) -> str:
        p = self.print_stars
        if self.reset:
            p = self.reset_stars
        return p

    @classmethod
    def printWhiteSpace(self) -> None:
        print("\n" * 8)

printWhiteSpace = PrintStuff.printWhiteSpace
printStars = PrintStuff().printStars
stringStars = PrintStuff().stringStars
printStarsReset = PrintStuff(reset=1).printStars
stringStarsReset = PrintStuff(reset=1).stringStars

def shardStats(ourShard) -> str:
    ourUptime = subprocess.getoutput("uptime")
    ourVersion = subprocess.getoutput(f"{harmonyFolder}/harmony -V")
    dbZeroSize = getDBSize('0')
    if ourShard == "0":
        print(f"""
* Uptime :: {ourUptime}\n\n Harmony DB 0 Size  ::  {dbZeroSize}
* {ourVersion}
{stringStars()}
        """)
    else:
        print(f"""
* Uptime :: {ourUptime}
*
* Harmony DB 0 Size  ::  {dbZeroSize}
* Harmony DB {ourShard} Size  ::   {getDBSize(str(ourShard))}
*
* {ourVersion}
*
{stringStars()}
        """)

def getDBSize(ourShard) -> str:
    harmonyDBSize = subprocess.getoutput(f"du -h {harmonyFolder}/harmony_db_{ourShard}")
    harmonyDBSize = harmonyDBSize.rstrip('\t')
    countTrim = len(harmonyFolder) + 13
    return harmonyDBSize[:-countTrim]
        
# gathering information
timeNow = datetime.now()
countTrim = len(harmonyFolder) + 13
remote_shard_0 = [f'{harmonyFolder}/hmy', 'blockchain', 'latest-headers', '--node=https://api.s0.t.hmny.io']
try:
    result_remote_shard_0 = run(remote_shard_0, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    remote_data_shard_0 = json.loads(result_remote_shard_0.stdout)
except (ValueError, KeyError, TypeError):
    print(f'Remote Shard 0 API not responding')
    sys.exit(1)
remote_shard = [f'{harmonyFolder}/hmy', 'blockchain', 'latest-headers', f'--node=https://api.s{ourShard}.t.hmny.io']
try:
    result_remote_shard = run(remote_shard, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    remote_data_shard = json.loads(result_remote_shard.stdout)
except (ValueError, KeyError, TypeError):
    print(f'Remote API not responding')
    sys.exit(1)
local_shard = [f'{harmonyFolder}/hmy', 'blockchain', 'latest-headers']
try:
    result_local_shard = run(local_shard, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    local_data_shard = json.loads(result_local_shard.stdout)
except (ValueError, KeyError, TypeError):
    print(f'Local client not running')
    sys.exit(1)
print(f"""
{stringStars()}
* Current Date & Time: {timeNow}
*
{stringStars()}
* Current Status on Shard {ourShard}:
*
* Shard 0 Sync Status:
* Local Server  - Epoch {local_data_shard['result']['beacon-chain-header']['epoch']} - Shard {local_data_shard['result']['beacon-chain-header']['shardID']} - Block {literal_eval(local_data_shard['result']['beacon-chain-header']['number'])}
* Remote Server - Epoch {remote_data_shard_0['result']['shard-chain-header']['epoch']} - Shard {remote_data_shard_0['result']['shard-chain-header']['shardID']} - Block {literal_eval(remote_data_shard_0['result']['shard-chain-header']['number'])}
*
{stringStars()}
    """)
if int(ourShard) > 0:
    print(f"""
* Shard {ourShard} Sync Status:
*
* Local Server  - Epoch {local_data_shard['result']['shard-chain-header']['epoch']} - Shard {local_data_shard['result']['shard-chain-header']['shardID']} - Block {literal_eval(local_data_shard['result']['shard-chain-header']['number'])}
* Remote Server - Epoch {remote_data_shard['result']['shard-chain-header']['epoch']} - Shard {remote_data_shard['result']['shard-chain-header']['shardID']} - Block {literal_eval(remote_data_shard['result']['shard-chain-header']['number'])}
*
{stringStars()}
    """)
    shardStats(ourShard)
