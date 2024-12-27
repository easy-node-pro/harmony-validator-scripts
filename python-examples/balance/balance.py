# balances.py
import aiohttp
import json
import asyncio
import subprocess

url = "https://rpc.s0.t.hmny.io"

async def get_balance(session, address):
    payload = json.dumps({
      "jsonrpc": "2.0",
      "id": 1,
      "method": "hmyv2_getBalance",
      "params": [
        address
      ]
    })
    headers = {
      'Content-Type': 'application/json'
    }

    async with session.post(url, headers=headers, data=payload) as response:
        if response.status == 200:
            try:
                balance_response = await response.json()
                balance = balance_response['result']
                # Convert to ONE (1 ONE = 1e18 atto)
                balance_in_one = balance / 1e18
                return balance_in_one
            except Exception as e:
                print(f"Failed to parse balance response for address {address}: {e}")
                print(f"Response: {await response.text()}")
                return None
        else:
            print(f"Failed to get balance for address {address}: {response.status}")
            print(f"Response: {await response.text()}")
            return None

async def get_pending_rewards(session, address):
    payload = json.dumps({
      "jsonrpc": "2.0",
      "id": 1,
      "method": "hmyv2_getDelegationsByDelegator",
      "params": [
        address
      ]
    })
    headers = {
      'Content-Type': 'application/json'
    }

    async with session.post(url, headers=headers, data=payload) as response:
        if response.status == 200:
            try:
                delegations_response = await response.json()
                delegations = delegations_response['result']
                total_pending = 0
                for delegation in delegations:
                    total_pending += delegation['reward'] / 1e18
                return total_pending
            except Exception as e:
                print(f"Failed to parse delegations response for address {address}: {e}")
                print(f"Response: {await response.text()}")
                return None
        else:
            print(f"Failed to get delegations for address {address}: {response.status}")
            print(f"Response: {await response.text()}")
            return None

async def main():
    # Extract addresses (same as before)
    command = "/home/serviceharmony/harmony/hmy keys list"
    output = subprocess.check_output(command, shell=True).decode('utf-8')
    lines = output.split('\n')
    addresses = []
    for line in lines[1:]:
        columns = line.split()
        if len(columns) > 1:
            address = columns[1]
            addresses.append(address)

    async with aiohttp.ClientSession() as session:
        # Run the get-balance and get-pending-rewards commands for each address
        for address in addresses:
            # Get balance
            balance = await get_balance(session, address)
            if balance is None:
                continue

            # Get pending rewards
            pending_rewards = await get_pending_rewards(session, address)
            if pending_rewards is None:
                continue

            print(f"Address: {address}, Balance: {balance} ONE, Pending Rewards: {pending_rewards} ONE")

if __name__ == "__main__":
    asyncio.run(main())