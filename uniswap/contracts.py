import time
from typing import List
from web3 import Web3
import os
import json

from classes.pool import Pool
from classes.token import Token
from classes.chain import Chain

__baseDir = os.path.dirname(os.path.abspath(__file__))
UNISWAP_FACTORY_ABI = json.load(open(__baseDir + '/data/factory_abi.json'))


def get_pools_test_chain(rpc_url, contract_abi, token_abi) -> List[Pool]:
    web3 = Web3(Web3.HTTPProvider(rpc_url))

    # UNISWAP_FACTORY_ADDRESS = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"  # Ether etc.
    UNISWAP_FACTORY_ADDRESS = '0x5757371414417b8C6CAad45bAeF941aBc7d3Ab32'  # Polygon
    uniswap_factory = web3.eth.contract(address=UNISWAP_FACTORY_ADDRESS, abi=UNISWAP_FACTORY_ABI)

    # swap_fee_percent = 0.3 / 1e6
    swap_fee_percent = 0.3 / 100

    all_exchange_pools = uniswap_factory.functions.allPairsLength().call()
    print(f'total number of pools: {all_exchange_pools}')
    pools = []

    for i in range(10):
    # for i in range(all_exchange_pools):
        exchange_pool_address = uniswap_factory.functions.allPairs(i).call()
        pair_contract = web3.eth.contract(address=exchange_pool_address, abi=contract_abi)

        token0_address = pair_contract.functions.token0().call()
        token1_address = pair_contract.functions.token1().call()

        token0_reserve, token1_reserve, _ = pair_contract.functions.getReserves().call()

        token0 = make_token(web3, token0_address, token_abi, token0_reserve)
        token1 = make_token(web3, token1_address, token_abi, token1_reserve)

        token0_price = token1_reserve / token0_reserve
        token1_price = 1 / token0_price

        tvl = (token0_reserve * token0_price) + (token1_reserve * token1_price)

        if tvl > 200:
            pools.append(Pool(tokens=(token0, token1), address=exchange_pool_address, swap_fee=swap_fee_percent))
            print(len(pools))
            print(f'added {pools[-1]}')
            print(f'pool address: {exchange_pool_address}')
            print(f'tvl: {tvl}')
        else:
            continue
    return pools


def update_pools(pools: List[Pool], rpc_url, contract_abi):
    web3 = Web3(Web3.HTTPProvider(rpc_url))

    for pool in pools:
        pool_contract = web3.eth.contract(address=pool.address, abi=contract_abi)

        reserve0, reserve1, _ = pool_contract.functions.getReserves().call()
        pool.tokens[0].amount = reserve0
        pool.tokens[1].amount = reserve1

        pool.last_update = int(time.time())
        print(f'{pool} was updated\nlast update: {pool.last_update} ')


def make_token(web3: Web3, token_address, token_abi, token_reserve) -> Token:
    token_contract = web3.eth.contract(address=token_address, abi=token_abi)
    token_symbol = token_contract.functions.symbol().call()
    token_decimals = token_contract.functions.decimals().call()
    token = Token(symbol=token_symbol, decimal=token_decimals, address=token_address)
    token.amount = token_reserve
    return token
