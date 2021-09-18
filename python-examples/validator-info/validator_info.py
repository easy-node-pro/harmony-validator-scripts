from icecream import ic
from requests import post

rpc_url = "https://api.harmony.one"


def run():
    wallet = "one18julyys26h67r4vq3zexzpfmvt9vpn0g75phmu"

    data = {
        "jsonrpc": "2.0",
        "method": "hmyv2_getValidatorInformation",
        "params": [wallet],
        "id": 1,
    }

    response = post(rpc_url, json=data)
    ic(response.text)
        

if __name__ == "__main__":
    run()
