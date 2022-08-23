import json
import subprocess
import os
import socket
import dotenv
from os import environ
from subprocess import Popen, PIPE, run
from ast import literal_eval
from dotenv import load_dotenv
from simple_term_menu import TerminalMenu
from datetime import datetime

def askYesNo(question: str) -> bool:
    YesNoAnswer = ""
    while not YesNoAnswer.startswith(("Y", "N")):
        YesNoAnswer = input(f"{question}: ").upper()
    if YesNoAnswer.startswith("Y"):
        return True
    return False

def setVar(fileName, keyName, updateName):
    if environ.get(keyName):
        dotenv.unset_key(fileName, keyName)
    dotenv.set_key(fileName, keyName, updateName)
    return

serverHostName = socket.gethostname()
userHomeDir = os.path.expanduser("~")
dotenv_file = f"{userHomeDir}/.easynode.env"
timeNow = datetime.now()

if os.path.isdir(f"{userHomeDir}/harmony"):
    harmonyFolder = f"{userHomeDir}/harmony"
elif os.path.isfile(f"{userHomeDir}/harmony"):
    harmonyFolder = f"{userHomeDir}"

if os.path.isfile(f"{userHomeDir}/.easynode.env"):
    load_dotenv(dotenv_file)
else:
    os.system(f"touch {userHomeDir}/.easynode.env")

if environ.get("SHARD"):
    ourShard = environ.get("SHARD")
else:
    # ask shard and record here
    os.system("clear")
    print("***")
    print("* First Boot - Gathering more information about your server                                 *")
    print("***")
    print("* Which shard do you want this node run on?                                                 *")
    print("***")
    menuOptions = ["[0] - Shard 0", "[1] - Shard 1", "[2] - Shard 2", "[3] - Shard 3", ]
    terminal_menu = TerminalMenu(menuOptions, title="* Which Shard will this node operate on? ")
    ourShard = str(terminal_menu.show())
    setVar(dotenv_file, "SHARD", ourShard)

if environ.get("NETWORK_SWITCH"):
    ourNetwork = environ.get("NETWORK_SWITCH")
   
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
def getDBSize(ourShard, harmonyFolder) -> str:
    checkSymlink = f'du -h {harmonyFolder}/harmony_db_{ourShard}'
    if os.path.islink(checkSymlink):
        harmonyFolder = os.path.relpath(checkSymlink)
    harmonyDBSize = subprocess.getoutput(f"du -h {harmonyFolder}/harmony_db_{ourShard}")
    harmonyDBSize = harmonyDBSize.rstrip('\t')
    return harmonyDBSize[:-countTrim]

# get shard stats
def shardStats(ourShard) -> str:
    ourUptime = subprocess.getoutput("uptime")
    ourVersion = subprocess.getoutput(f"{harmonyFolder}/harmony -V")
    dbZeroSize = getDBSize('0', harmonyFolder)
    if ourShard == "0":
        print(f"""
* Harmony DB 0 Size  ::  {dbZeroSize}
*
* {ourVersion}
* Uptime :: {ourUptime}
***
        """)
    else:
        print(f"""
*
* Harmony DB 0 Size  ::  {dbZeroSize}
* Harmony DB {ourShard} Size  ::   {getDBSize(str(ourShard), harmonyFolder)}
*
* {ourVersion}
* Uptime :: {ourUptime}
***
        """)

# print it out

if int(ourShard) != "0":
    print(f"""
***
* Current Date & Time: {timeNow}
*
***
* Current Status of our server {serverHostName} currently on Shard {environ.get('SHARD')}:
*
* Shard 0 Sync Status:
* Local Server  - Epoch {local_data_shard['result']['beacon-chain-header']['epoch']} (Always 1 epoch behind Remote Server) - Shard 0 not required on Shard {environ.get('SHARD')}
* Remote Server - Epoch {remote_data_shard_0['result']['shard-chain-header']['epoch']} - Shard {remote_data_shard_0['result']['shard-chain-header']['shardID']} - Block {literal_eval(remote_data_shard_0['result']['shard-chain-header']['number'])}
*
***
""")
else:
    print(f"""
***
* Current Date & Time: {timeNow}
*
***
* Current Status of our server {serverHostName} currently on Shard {environ.get('SHARD')}:
*
* Shard 0 Sync Status:
* Local Server  - Epoch {local_data_shard['result']['beacon-chain-header']['epoch']} - Shard {local_data_shard['result']['beacon-chain-header']['shardID']} - Block {literal_eval(local_data_shard['result']['beacon-chain-header']['number'])}
* Remote Server - Epoch {remote_data_shard_0['result']['shard-chain-header']['epoch']} - Shard {remote_data_shard_0['result']['shard-chain-header']['shardID']} - Block {literal_eval(remote_data_shard_0['result']['shard-chain-header']['number'])}
*
***
""")

# run it all
shardStats(ourShard)
