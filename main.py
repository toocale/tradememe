from web3 import Web3
import time
import abi
import verified
import tokenbalance
import lpprovider
import config
import swapper
# For Base Testnet, you can use: "https://base-goerli.g.alchemy.com/v2/YOUR_ALCHEMY_API_KEY"

# Initialize Web3 with Alchemy
web3 = Web3(Web3.HTTPProvider(config.alchemy_base_mainnet_url))

# Check connection to Base network
if web3.is_connected():
    print("Connected to Base network")
else:
    print("Failed to connect to Base network")

# Uniswap V2 Factory contract address on Ethereum (replace with the correct Base address)
factory_address = config.factory_address
router_address = config.router_address
router_address = Web3.to_checksum_address(router_address)


# Create contract instance for Uniswap Factory
factory_contract = web3.eth.contract(address=factory_address, abi=abi.factory_abi)
latest_block = web3.eth.block_number

# Create an event filter for PairCreated events
pair_created_event = factory_contract.events.PairCreated.create_filter(from_block=latest_block-1000)

print("Listening for new pairs on Uniswap...")

# Continuously check for new events
def format_reserve(reserve, decimals):
    return reserve / (10 ** decimals)
while True:
    try:
        new_entries = pair_created_event.get_new_entries()
        for event in new_entries:
            token0 = event['args']['token0']
            token1 = event['args']['token1']
            pair_address = event['args']['pair']
            #print(f"New Pair Created: Token0: {token0}, Token1: {token1}, Pair Address: {pair_address}")
            # Create a contract instance for the new pair
            pair_contract = web3.eth.contract(address=pair_address, abi=abi.pair_abi)

            # Fetch reserves (liquidity amounts) from the pair contract
            reserve0, reserve1, _ = pair_contract.functions.getReserves().call()

            # Get token names
            token0_contract = web3.eth.contract(address=Web3.to_checksum_address(token0), abi=abi.erc20_abi)
            token1_contract = web3.eth.contract(address=Web3.to_checksum_address(token1), abi=abi.erc20_abi)

            token0_name = token0_contract.functions.name().call()
            token1_name = token1_contract.functions.name().call()

            token0_decimals = token0_contract.functions.decimals().call()
            token1_decimals = token1_contract.functions.decimals().call()

            # Format reserves to human-readable format
            formatted_reserve0 = format_reserve(reserve0, token0_decimals)
            formatted_reserve1 = format_reserve(reserve1, token1_decimals)
            if token1_name == 'ETH' or token1_name == 'Wrapped Ether': 
                token1_name = token0_name
                token1 = token0
                formatted_reserve1 = formatted_reserve0
        

            # Output the token names and formatted reserves
            #print(f"Token0 Name: {token0_name}, Reserve: {formatted_reserve0:.2f} {token0_name}")
            eth_liquidity = formatted_reserve0
            tokenliquidity = formatted_reserve1
            print (f"weth :{eth_liquidity}")
            print ( f"token: {tokenliquidity}")
            print(f"Token1 Name: {token1_name}, Contract: {token1} Liquidity:  {formatted_reserve0:.2f} {token0_name} : {formatted_reserve1:.2f} {token1_name}")
            
            if eth_liquidity > 4 and (token1 == tokenbalance.WETH_CONTRACT or token0 == tokenbalance.WETH_CONTRACT) and lpprovider.lp_provider(pair_address) == "buy":
                goodcontract= verified.verified_contract(token1)
                print(goodcontract)
                if goodcontract == 'verified':
                    print("contract verified")
                    print("swapping")
                    while True:
                        try:# Swap WETH for the token
                            amount_in = tokenbalance.balanceofweth()# web3.to_wei(0.000001, 'ether')  # Amount of WETH to swap
                            amount_in = tokenbalance.balanceofweth()# web3.to_wei(0.000001, 'ether')  # Amount of WETH to swap
                            #amount_in1 =   web3.to_wei(0.000001, 'ether')
                            to_address = swapper.web3.eth.default_account
                            # Amount of WETH to swap
                            
                            if amount_in > 0:
                                amount_out_min = 0  # Minimum amount of tokens you want to receive
                                to_address = swapper.web3.eth.default_account  # Address to receive the tokens
                                weth_address = Web3.to_checksum_address("0x4200000000000000000000000000000000000006")  # Wrapped Ether Address
                                token_to_swap_address = Web3.to_checksum_address(token1)
                                swapper.swap_weth(amount_in, amount_out_min, to_address, weth_address, token_to_swap_address)    
                                time.sleep(180)
                                amount_in1 = tokenbalance.balanceoftoken(token1)
                            # swap tokens for weth
                        
                            if amount_in1 > 0:    
                                amount_out_min = 0  # Minimum amount of tokens you want to receive
                                to_address = swapper.web3.eth.default_account  # Address to receive the tokens
                                weth_address = Web3.to_checksum_address("0x4200000000000000000000000000000000000006")  # Wrapped Ether Address
                                token_to_swap_address = Web3.to_checksum_address(token1)
                                
                                swapper.swap_tokens(amount_in1, amount_out_min, to_address, weth_address, token_to_swap_address)
                                break
                        except ConnectionError:
                            print("Connection error. Retrying...")
                            time.sleep(1)
                            continue
        

        # Add a small sleep to avoid spamming the network (adjust the sleep time as needed)
        time.sleep(2)
    except ConnectionError:
        continue