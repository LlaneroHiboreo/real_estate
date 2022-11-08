from brownie import accounts, network
from web3 import Web3
from scripts.deploy import deploy_realstate
from helpers.helper import load_config
import pytest
import json


def test_mint():
    # deploy contracts
    contracts = deploy_realstate()
    realstate_sc = contracts[0]
    escrow_sc = contracts[1]
    # load config
    conf = load_config()
    seller=conf["escrow"]["seller"]
    inspector=conf["escrow"]["inspector"]
    lender=conf["escrow"]["lender"]
    buyer=conf["escrow"]["buyer"]
    # MINT property
    tx_mint = realstate_sc.mint(conf["metadata"]["property_1"], {'from':seller})
    tx_mint.wait(1)
    # check balance of listed items 1
    assert realstate_sc.totalSupply() == 1
    # APPROVE property
    realstate_sc.approve(escrow_sc.address, 1, {'from':seller})
    assert realstate_sc.getApproved(1) == escrow_sc.address
    # LIST property
    tx_list = escrow_sc.list(1, buyer, Web3.toWei(10, 'ether'), Web3.toWei(5, 'ether'), {'from':seller})
    tx_list.wait(1)
    # check is updated as listed
    assert escrow_sc.isListed(1) == True
    # check update of ownership
    assert realstate_sc.ownerOf(1) == escrow_sc.address
    # DEPOSIT
    tx_deposit = escrow_sc.depositEarnest(1, {'from':buyer, 'value':Web3.toWei(5, 'ether')})
    tx_deposit.wait(1)
    # check contract balance
    assert escrow_sc.getBalance() == Web3.toWei(5, 'ether')
    # INSPECTION
    escrow_sc.updateInspectionStatus(1, True, {'from':inspector})
    # check inspection passed
    assert escrow_sc.inspectionPassed(1) == True
    # APPROVE sale
    escrow_sc.approveSale(1, {"from":buyer})
    escrow_sc.approveSale(1, {"from":seller})
    escrow_sc.approveSale(1, {"from":lender})
    # check updated approval values
    assert escrow_sc.approval(1, buyer) == True
    assert escrow_sc.approval(1, seller) == True
    assert escrow_sc.approval(1, lender) == True
    # SALE
    #web3.eth.sendRawTransaction({'from':lender, 'to':escrow_sc.address, 'value':Web3.toWei(5, 'ether')})
    tx_sale = escrow_sc.finalizeSale(1, {'from':seller})
    # check ownerships
    assert realstate_sc.ownerOf(1) == buyer
    # check balance
    assert escrow_sc.getBalance() == 0
    