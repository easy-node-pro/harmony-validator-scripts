import json
import socket
import subprocess
import requests
import os
import dotenv
from dotenv import load_dotenv
from os import environ
from subprocess import Popen, PIPE, run
from ast import literal_eval

ourShard = 3
harmonyFolder = '/home/serviceharmony/harmony'

# will use easynode.env file for VSTATS_BOT token, or add your token on line 20 below in the ''
if os.path.exists('~/.easynode.env'):
    load_dotenv('~/.easynode.env')
    vstats_token = environ.get('VSTATS_BOT')
else:
    vstats_token = ''

# get remote stats for shard 0, then the #'d shard, if it's 0 just make it the same.
remote_shard_0 = [f'{harmonyFolder}/hmy', 'blockchain', 'latest-headers', '--node=https://api.s0.t.hmny.io']
result_remote_shard_0 = run(remote_shard_0, stdout=PIPE, stderr=PIPE, universal_newlines=True)
remote_data_shard_0 = json.loads(result_remote_shard_0.stdout)
if ourShard > 0:
    remote_shard = [f'{harmonyFolder}/hmy', 'blockchain', 'latest-headers', f'--node=https://api.s{ourShard}.t.hmny.io']
    result_remote_shard = run(remote_shard, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    remote_data_shard = json.loads(result_remote_shard.stdout)
else:
    remote_shard = remote_data_shard_0
    result_remote_shard = result_remote_shard_0
    remote_data_shard = remote_data_shard_0

# get local server stats
local_shard = [f'{harmonyFolder}/hmy', 'blockchain', 'latest-headers']
result_local_shard = run(local_shard, stdout=PIPE, stderr=PIPE, universal_newlines=True)
local_data_shard = json.loads(result_local_shard.stdout)

# notifier of problems
def sendWebhook(subject, message):
    webhook_url_vstats = f'https://vstats.one/api/easynode/stats?api_token={vstats_token}&alert-type=danger&subject={subject}&message={message}'
    requests.request("GET", webhook_url_vstats)

# do math to see if we're in sync
shard_0_blocks = literal_eval(local_data_shard['result']['beacon-chain-header']['number']) - literal_eval(remote_data_shard_0['result']['shard-chain-header']['number'])
if ourShard > 0:
    shard_n_blocks = literal_eval(local_data_shard['result']['shard-chain-header']['number']) - literal_eval(remote_data_shard['result']['shard-chain-header']['number'])

# if lower blocks on shard 0
if shard_0_blocks <= -10 or shard_0_blocks >= 10:
    print(f"""
***
* Local Server Not In Sync With Blockchain on Shard 0 !!!
* Send Notification here! Result 1: {literal_eval(local_data_shard['result']['beacon-chain-header']['number'])} Result 2: {literal_eval(remote_data_shard_0['result']['shard-chain-header']['number'])}
***
    """)
    # send webhook to vStats bot
    sendWebhook('Shard 0 Behind', f"From your server {socket.gethostname()}\nLocal Epoch {local_data_shard['result']['beacon-chain-header']['epoch']} Block: {literal_eval(local_data_shard['result']['beacon-chain-header']['number'])}\nRemote Epoch {remote_data_shard_0['result']['shard-chain-header']['epoch']} Block: {literal_eval(remote_data_shard_0['result']['shard-chain-header']['number'])}\nOff by {shard_0_blocks} blocks.")
else:
    print(f"""
***
* Your server is in sync on shard 0.
***
    """)

# only if not on shard 0.
if ourShard > 0:
# if lower blocks on shard 3
    if shard_n_blocks <= -10 or shard_n_blocks >= 10:
        print(f"""
***
* Local Server Not In Sync With Blockchain on Shard {ourShard}!!!
* Send Notification here! Result 1: {literal_eval(local_data_shard['result']['shard-chain-header']['number'])} Result 2: {literal_eval(remote_data_shard['result']['shard-chain-header']['number'])}
***
        """)
        sendWebhook(f'Shard {ourShard} Behind', f"From your server {socket.gethostname()}\nLocal Epoch   {local_data_shard['result']['shard-chain-header']['epoch']} Block: {literal_eval(local_data_shard['result']['shard-chain-header']['number'])}\nRemote Epoch {remote_data_shard['result']['shard-chain-header']['epoch']} Block: {literal_eval(remote_data_shard['result']['shard-chain-header']['number'])}\nOff by {shard_n_blocks} blocks.")
    else:
        print(f"""
***
* Your server is in sync on shard 3.
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