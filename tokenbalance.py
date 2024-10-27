import requests

API_KEY = 'RINMGYS9IUZQHGYK6PU495NC4R2K1HEU68'
WETH_CONTRACT = '0x4200000000000000000000000000000000000006'  # Mainnet WETH contract
ADDRESS = '0x19Ef1cCFd42FCAbeE06000c89cA9E5f6709E9f80'

def balanceofweth():
    weth_url = f"https://api.basescan.org/api?module=account&action=tokenbalance&contractaddress={WETH_CONTRACT}&address={ADDRESS}&tag=latest&apikey={API_KEY}"

    response = requests.get(weth_url)
    data = response.json()

    if data['status'] == '1':
        balance_wei = int(data['result'])
        balance_eth = balance_wei / (10**18)  # Convert from Wei to Ether
        print(f"WETH Balance: {balance_eth} WETH")
        return int(balance_wei)
    else:
        print(f"Error: {data['message']}")
def balanceoftoken(token_CONTRACT):
    token_url = f"https://api.basescan.org/api?module=account&action=tokenbalance&contractaddress={token_CONTRACT}&address={ADDRESS}&tag=latest&apikey={API_KEY}"

    response = requests.get(token_url)
    data = response.json()

    if data['status'] == '1':
        balance_wei = int(data['result'])
        balance_eth = balance_wei / (10**18)  # Convert from Wei to Ether
        print(f"WETH Balance: {balance_eth} WETH")
        return int(balance_wei)
    else:
        print(f"Error: {data['message']}")


#print("Balance of WETH: ",int(balanceofweth())) 
#print("Balance of Token: ",int(balanceoftoken("0xe3f5bc5f1e9b8e7c1fd3cf19114e133ade524ebb")))