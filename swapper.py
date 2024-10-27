from web3 import Web3
import time
import abi
import config



# Alchemy Base Mainnet API URL (replace YOUR_ALCHEMY_API_KEY with your actual key)
alchemy_base_mainnet_url = f"https://base-mainnet.g.alchemy.com/v2/{config.ALCHEMY_API_KEY}"
web3 = Web3(Web3.HTTPProvider(alchemy_base_mainnet_url))

# Ensure you're connected
if not web3.is_connected():
    raise Exception("Failed to connect to the BASE network")

# Set your account
web3.eth.default_account = Web3.to_checksum_address(config.wallet_address)  # Replace with your wallet address

# Addresses (replace with actual addresses)
  # Token you want to receive
router_address = Web3.to_checksum_address(config.router_address)  # Uniswap V2 Router or equivalent
max_fee_per_gas = 20000000
max_priority_fee_per_gas = 3000000

#print(web3.eth.max_fee_per_gas)
print("Nonce: ", web3.eth.get_transaction_count(web3.eth.default_account))
def swap_weth(amount_in, amount_out_min, to_address, weth_address, token_to_swap_address):
    # Step 1: Approve the router to spend WETH
    weth_contract = web3.eth.contract(address=weth_address, abi=abi.erc20_abi)
#"""
    # Approve the router to spend amount_in WETH
    approve_txn = weth_contract.functions.approve(router_address, amount_in).build_transaction({
        'from': web3.eth.default_account,
        'gas': 200000,
        #'gasPrice': 60,  # Adjust gas price as needed
        'nonce': web3.eth.get_transaction_count(web3.eth.default_account),
        'maxFeePerGas':max_fee_per_gas,
        'maxPriorityFeePerGas':max_priority_fee_per_gas
    })

    # Sign and send the transaction
    signed_txn = web3.eth.account.sign_transaction(approve_txn, config.private_key)  # Replace with your private key
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    # Wait for the transaction to be mined
    print(f"Approving transaction ...........")
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Approval SUCCESSUL ")

    # Step 2: Perform the swap
    router_contract = web3.eth.contract(address=router_address, abi= abi.router_abi)
    
    # Create the path for the swap (WETH -> Token)
    path = [weth_address, token_to_swap_address]
    deadline = int(time.time()) + 600  # 10 minutes from now

    swap_txn = router_contract.functions.swapExactTokensForTokens(
        amount_in,
        amount_out_min,
        path,
        to_address,
        deadline
    ).build_transaction({
        'from': web3.eth.default_account,
        'gas': 200000,
        #'gasPrice': web3.toWei('0.0001', 'gwei'),  # Adjust gas price as needed
        'nonce': web3.eth.get_transaction_count(web3.eth.default_account) ,
        'maxFeePerGas':max_fee_per_gas,
        'maxPriorityFeePerGas':max_priority_fee_per_gas  # Increment nonce
    })

    # Sign and send the swap transaction
    signed_swap_txn = web3.eth.account.sign_transaction(swap_txn, config.private_key)  # Replace with your private key
    swap_tx_hash = web3.eth.send_raw_transaction(signed_swap_txn.raw_transaction)

    # Wait for the transaction to be mined
    print(f"Swapping Weth transaction ...........")
    swap_receipt = web3.eth.wait_for_transaction_receipt(swap_tx_hash)
    print(f"Swap  Weth successful")

# Example Usag
#"""
amount_in = web3.to_wei(0.000001, 'ether')  # Amount of WETH to swap
amount_out_min = 0  # Minimum amount of tokens you want to receive
to_address = web3.eth.default_account  # Address to receive the tokens
weth_address = Web3.to_checksum_address("0x4200000000000000000000000000000000000006")  # Wrapped Ether Address
token_to_swap_address = Web3.to_checksum_address("0xbd01f780da6e7c9ad4d11a5010c8d46a12901491")  # Address to receive the tokens

#swap_weth(amount_in, amount_out_min, to_address, weth_address, token_to_swap_address)




#sell token
def swap_tokens(amount_in, amount_out_min, to_address, weth_address, token_to_swap_address):
    # Step 1: Approve the router to spend WETH
    weth_contract = web3.eth.contract(address= token_to_swap_address, abi=abi.erc20_abi)
#"""  
    # Approve the router to spend amount_in WETH
    approve_txn = weth_contract.functions.approve(router_address, amount_in).build_transaction({
        'from': web3.eth.default_account,
        'gas': 200000,
        #'gasPrice': 60,  # Adjust gas price as needed
        'nonce': web3.eth.get_transaction_count(web3.eth.default_account),
        'maxFeePerGas':max_fee_per_gas,
        'maxPriorityFeePerGas':max_priority_fee_per_gas
    })

    # Sign and send the transaction
    signed_txn = web3.eth.account.sign_transaction(approve_txn, config.private_key)  # Replace with your private key
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    # Wait for the transaction to be mined
    print(f"Approving transaction ...........")
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Approval SUCCESSUL ")

    # Step 2: Perform the swap
    router_contract = web3.eth.contract(address=router_address, abi= abi.router_abi)
    
    # Create the path for the swap (token -> weth)
    path = [token_to_swap_address, weth_address]
    deadline = int(time.time()) + 600  # 10 minutes from now

    swap_txn = router_contract.functions.swapExactTokensForTokens(
        amount_in,
        amount_out_min,
        path,
        to_address,
        deadline
    ).build_transaction({
        'from': web3.eth.default_account,
        'gas': 200000,
        #'gasPrice': web3.toWei('0.0001', 'gwei'),  # Adjust gas price as needed
        'nonce': web3.eth.get_transaction_count(web3.eth.default_account) ,
        'maxFeePerGas':max_fee_per_gas,
        'maxPriorityFeePerGas':max_priority_fee_per_gas  # Increment nonce
    })

    # Sign and send the swap transaction
    signed_swap_txn = web3.eth.account.sign_transaction(swap_txn, config.private_key)  # Replace with your private key
    swap_tx_hash = web3.eth.send_raw_transaction(signed_swap_txn.raw_transaction)

    # Wait for the transaction to be mined
    print(f"Swapping token transaction ...........")
    swap_receipt = web3.eth.wait_for_transaction_receipt(swap_tx_hash)
    print(f"Swap Token successful")

# Example Usage
"""
amount_in = web3.to_wei(0.000001, 'ether')  # Amount of WETH to swap
amount_out_min = 0  # Minimum amount of tokens you want to receive
to_address = web3.eth.default_account  # Address to receive the tokens
weth_address = Web3.to_checksum_address("0x4200000000000000000000000000000000000006")  # Wrapped Ether Address
token_to_swap_address = Web3.to_checksum_address("0xbd01f780da6e7c9ad4d11a5010c8d46a12901491")  # Address to receive the tokens
"""
#swap_tokens(amount_in, amount_out_min, to_address, weth_address, token_to_swap_address)
