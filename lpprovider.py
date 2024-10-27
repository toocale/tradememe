from web3 import Web3
import time
import abi
import config

from eth_abi.abi import decode
from eth_utils import function_signature_to_4byte_selector

# Connect to Ethereum node
web3 = Web3(Web3.HTTPProvider(config.alchemy_base_mainnet_url))

# LP Token Pair contract address (replace with actual pair contract address)
def lp_provider(contract):
    counter = 0
    lp_provider = 0
    locked_status = 0
    buy = "buy"
    while counter < 60:
        counter+=1
        pair_address = web3.to_checksum_address(contract)
        # Instantiate contract
        #pair_contract = web3.eth.contract(address=pair_address, abi=abi.erc20_abi)

        lp_token_address = pair_address

        # Define the block range (for example, the last 10 blocks)
        latest_block = web3.eth.block_number
        from_block = latest_block - 10
        print(f"Current block: {from_block}")

        to_block = latest_block

        # Create a filter to capture all transactions involving the LP token contract in the block range
        logs = web3.eth.get_logs({
            "fromBlock": from_block,
            "toBlock": to_block,
            "address": lp_token_address
        })

        # Extract the transaction hashes from the logs
        tx_hashes = set([log.transactionHash.hex() for log in logs])
        #contract = web3.eth.contract(address=lp_token_address, abi=abi.contract_abi)

        # Output the number of transactions and their transaction hashes
        #print(f"Number of transactions: {len(tx_hashes)}")
        #print("Transaction Hashes:")
        # Fetch and display transaction details for each transaction hash


        for tx_hash in tx_hashes:
            tx = web3.eth.get_transaction(tx_hash)
            tx_hex ="0x" + tx.hash.hex()
            txh=web3.eth.get_transaction(tx_hex)
            
            #print(f"Transaction Hash: {tx_hex}")
            #print(f"From: {tx['from']}")
            #print(f"To: {tx['to']}")
            #print(f"Gas Used: {tx['gas']}")
            #print(f"Value: {tx['value']} wei\n")
            txh_input= (txh['input'])   
            input_data = tx.input
            # Get the method ID (first 4 bytes of the input data)
            method_id = "0x" + input_data[:10].hex()  # 0x + 8 hex characters = 4 bytes
            #print("Method ID:", method_id)            
            if method_id.startswith(config.addliquidity_methodid) or method_id == config.addliquidity_methodid:
                print("Liquidity added")
                lp_provider+=1
            if method_id.startswith(config.removeliquidity_methodid) or method_id == config.removeliquidity_methodid:
                print("Liquidity removed")
                lp_provider-=1
            if method_id.startswith(config.lockliquidity_methodid) or method_id == config.lockliquidity_methodid:
                print("Liquidity locked")
                locked_status = 1
                break
            if counter > 10: 

                break
            if lp_provider>10:
                break
        time.sleep(60*60)
        #print("1111111111111111111111111111")
                
    if (locked_status == 1 and lp_provider > 2) or lp_provider > 10:
        return buy
    print(lp_provider," ",locked_status)
        
#lp_provider("0x2674ea06e9e4131a5c07bfd204ca704e8c08c6e2")