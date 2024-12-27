import aiohttp
import json
import asyncio
import subprocess
import argparse
import requests

# Set the path to the harmony binary
hmy_app = "/home/serviceharmony/harmony/hmy"
# Set the path to the passphrase file, if not using passphrase.txt then comment out the line and uncomment the next line to manually enter a password for each wallet in hmy
passphrase_file = "--passphrase-file /home/serviceharmony/harmony/passphrase.txt"
# passphrase_file = "--passphrase"
# Set the wallet to send rewards to from your validator
rewards_wallet = "one1_SET_REWARDS_WALLET_ADDRESS_HERE"
# Use the harmony mainnet rpc endpoint or customize
api_server = "https://api.s0.t.hmny.io"
url = "https://rpc.s0.t.hmny.io"
# Set the amount of ONE coins to reserve in validator wallet for gas fees
reserve_amount = 5
# Set the gas price for the transactions
gas_price = 100
# Set the ntfy.sh url to send notifications
ntfy_url = "https://ntfy.sh/CUSTOMIZE_THIS_URL"

async def collect_rewards(address):
    # Run the collect-rewards command and capture output
    command = f"{hmy_app} staking collect-rewards --delegator-addr {address} --gas-price {gas_price} {passphrase_file} --node='{api_server}'"
    process = await asyncio.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = await process.communicate()

    # Check if the command was successful
    if process.returncode == 0:
        return True
    else:
        print(f"Failed to collect rewards for address {address[:4]}...{address[-4:]}: {stderr.decode('utf-8')}")
        return False

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
                print(f"Failed to parse balance response for address {address[:4]}...{address[-4:]}: {e}")
                print(f"Response: {await response.text()}")
                return None
        else:
            print(f"Failed to get balance for address {address[:4]}...{address[-4:]}: {response.status}")
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
                print(f"Failed to parse delegations response for address {address[:4]}...{address[-4:]}: {e}")
                print(f"Response: {await response.text()}")
                return None
        else:
            print(f"Failed to get delegations for address {address[:4]}...{address[-4:]}: {response.status}")
            print(f"Response: {await response.text()}")
            return None

async def transfer_rewards(address, amount):
    # Run the transfer command
    command = f"{hmy_app} transfer --amount {amount} --from {address} --from-shard 0 --to {rewards_wallet} --to-shard 0 --gas-price {gas_price} {passphrase_file} --node='{api_server}'"
    output = await asyncio.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = await output.communicate()
    if output.returncode!= 0:
        print(f"Failed to transfer {amount} $ONE for address {address}: {stderr.decode('utf-8')}")
    else:
        return amount
    return 0

async def main():
    parser = argparse.ArgumentParser(description="Get balance and pending rewards")
    parser.add_argument("-b", "--balance", action="store_true", help="Show balance and pending rewards")
    args = parser.parse_args()

    # Extract addresses (same as before)
    command = f"{hmy_app} keys list"
    output = subprocess.check_output(command, shell=True).decode('utf-8')
    lines = output.split('\n')
    addresses = []
    for line in lines[1:]:
        columns = line.split()
        if len(columns) > 1:
            address = columns[1]
            addresses.append(address)

    total_pending = 0
    rewards_message = ""
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

            if args.balance:
                rewards_message += f"Address: {address[:4]}...{address[-4:]}, Balance: {round(balance, 2)} ONE, Pending Rewards: {round(pending_rewards, 2)} ONE\n"
            total_pending += pending_rewards

    if args.balance:
        rewards_message += f"\nTotal pending rewards: {round(total_pending, 4)} $ONE"
        requests.post(f"{ntfy_url}", data=rewards_message)
    else:
        # Run the collect-rewards, get-balance, and transfer commands for each address
        for address in addresses:
            # Collect rewards
            task = asyncio.create_task(collect_rewards(address))
            collected = await task
            if not collected:
                continue

            # Get balance
            task = asyncio.create_task(get_balance(session, address))
            balance = await task
            if balance is None:
                continue

            # Calculate transfer amount
            transfer_amount = max(0, float(balance) - reserve_amount)

            # Transfer rewards
            if transfer_amount > 0:
                amount_transferred = await transfer_rewards(address, transfer_amount)
                rewards_message += f"Transferred {round(amount_transferred, 4)} $ONE for {address[:4]}...{address[-4:]} to rewards wallet.\n"
            else:
                print(f"Not enough rewards to transfer for address {address[:4]}...{address[-4:]}")

        rewards_message += f"\nTotal rewards transferred: {round(total_pending, 4)} $ONE"
        print(rewards_message)
        requests.post(f"{ntfy_url}", data=rewards_message)

if __name__ == "__main__":
    asyncio.run(main())