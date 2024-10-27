import requests
import config


def verified_contract(contract):
    contract_address = contract
    caddress = "verified"
    url = f"https://api.basescan.org/api?module=contract&action=getsourcecode&address={contract_address}&apikey={config.explorer_key}"

    # Send the request
    response = requests.get(url)

    # Parse the response
    data = response.json()

    if data['status'] == '1':
        # Contract is found, check for verification
        if data['result'][0]['SourceCode']:
            print("Contract is verified.")
            return caddress
        else:
            print("Contract is not verified.")
    else:
        print(f"Error: {data['message']}")
        

