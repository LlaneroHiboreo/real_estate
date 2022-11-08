import json

def load_config():
    # Opening JSON file
    f = open('/Users/blackshuck/Documents/BLOCKCHAIN/dapp_university/realEstate/helpers/config.json')
    # Load JSON file
    conf = json.load(f)
    return conf