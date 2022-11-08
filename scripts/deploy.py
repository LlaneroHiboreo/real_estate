from brownie import RealEstate, Escrow, accounts, network
from web3 import Web3
from helpers.helper import load_config
import json

def deploy_realstate():
    if network.show_active() == 'development':
        deployer=accounts[0]
        print("[*] Using development - ganache network")
    elif network.show_active() == 'goerli_infura_node':
        deployer = accounts.load('blockchain_courses')
        print("[*] Using Infura node in Goerli network")

    # deploy real estate contract
    realstate_sc = RealEstate.deploy({'from':deployer})

    # get variables from config
    conf=load_config()
    seller=conf["escrow"]["seller"]
    inspector=conf["escrow"]["inspector"]
    lender=conf["escrow"]["lender"]

    # deploy escrow contract
    escrow_sc = Escrow.deploy(realstate_sc.address, seller, inspector, lender, {'from': deployer})

    return (realstate_sc, escrow_sc)

def main():
    deploy_realstate()
