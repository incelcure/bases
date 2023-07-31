# from datetime import time
import time
from typing import List
from web3 import Web3
import os
import json
import requests

from classes.pool import Pool
from classes.token import Token
from classes.chain import Chain

__baseDir = os.path.dirname(os.path.abspath(__file__))
UNISWAP_FACTORY_ABI = json.load(open(__baseDir + '/data/factory_abi.json'))
UNISWAP_PAIR_ABI = json.load(open(__baseDir + '/data/uniswap_pair_abi.json'))
ERC20_ABI = json.load(open(__baseDir + '/data/erc20_abi.json'))

rpc_url = 'https://polygon-rpc.com'

web3 = Web3(Web3.HTTPProvider(rpc_url))

# UNISWAP_FACTORY_ADDRESS = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"  # Ether etc.
UNISWAP_FACTORY_ADDRESS = '0x5757371414417b8C6CAad45bAeF941aBc7d3Ab32'  # Polygon
uniswap_factory = web3.eth.contract(address=UNISWAP_FACTORY_ADDRESS, abi=UNISWAP_FACTORY_ABI)


def get_pools_test_chain() -> List[Pool]:
    swap_fee_percent = 0.3 / 1e6
    all_exchange_pools = uniswap_factory.functions.allPairsLength().call()
    pools = []

    pair_contract = web3.eth.contract(address='0x604229c960e5CACF2aaEAc8Be68Ac07BA9dF81c3', abi=UNISWAP_PAIR_ABI)
    token0_address = pair_contract.functions.token0().call()
    token1_address = pair_contract.functions.token1().call()
    token0_reserve, token1_reserve, _ = pair_contract.functions.getReserves().call()
    token0 = make_token(token0_address, ERC20_ABI, token0_reserve)
    token1 = make_token(token1_address, ERC20_ABI, token1_reserve)
    pools.append(
        Pool(tokens=(token0, token1), address='0x604229c960e5CACF2aaEAc8Be68Ac07BA9dF81c3', swap_fee=swap_fee_percent))

    pair_contract = web3.eth.contract(address='0x853Ee4b2A13f8a742d64C8F088bE7bA2131f670d', abi=UNISWAP_PAIR_ABI)
    token0_address = pair_contract.functions.token0().call()
    token1_address = pair_contract.functions.token1().call()
    token0_reserve, token1_reserve, _ = pair_contract.functions.getReserves().call()
    token0 = make_token(token0_address, ERC20_ABI, token0_reserve)
    token1 = make_token(token1_address, ERC20_ABI, token1_reserve)
    pools.append(
        Pool(tokens=(token0, token1), address='0x853Ee4b2A13f8a742d64C8F088bE7bA2131f670d', swap_fee=swap_fee_percent))

    print(pools)
    print(all_exchange_pools)
    for i in range(5):
        # for i in range(all_exchange_pools):
        exchange_pool_address = uniswap_factory.functions.allPairs(i).call()
        pair_contract = web3.eth.contract(address=exchange_pool_address, abi=UNISWAP_PAIR_ABI)

        token0_address = pair_contract.functions.token0().call()
        token1_address = pair_contract.functions.token1().call()

        token0_reserve, token1_reserve, _ = pair_contract.functions.getReserves().call()

        token0 = make_token(token0_address, ERC20_ABI, token0_reserve)
        token1 = make_token(token1_address, ERC20_ABI, token1_reserve)

        # token0_price = token1_reserve / (10 ** token1_decimals)
        # token1_price = token0_reserve / (10 ** token0_decimals)

        token0_price = token1_reserve / token0_reserve
        token1_price = 1 / token0_price

        tvl = (token0_reserve * token0_price) + (token1_reserve * token1_price)
        print(f'tvl: {tvl}')

        print(exchange_pool_address)
        if tvl > 200:
            pools.append(Pool(tokens=(token0, token1), address=exchange_pool_address, swap_fee=swap_fee_percent))
            print(pools[-1])
            print(len(pools))
        else:
            continue
    return pools


def update_pools(pools: List[Pool]):
    for pool in pools:
        # Создание объекта контракта UniswapV2Pair для каждого пула
        pool_contract = web3.eth.contract(address=pool.address, abi=UNISWAP_PAIR_ABI)

        # Получение резервов токенов в пуле
        reserve0, reserve1, _ = pool_contract.functions.getReserves().call()

        # Обновление данных о резервах токенов в пуле
        # pool.tokens[0].set_new_argument('amount', reserve0)
        # pool.tokens[1].set_new_argument('amount', reserve1)

        # print("Пул обновлен няняня")
        # Обновление времени последнего обновления данных
        pool.last_update = int(time.time())
        print(pool.last_update)


def make_token(token_address, abi, token_reserve) -> Token:
    token_contract = web3.eth.contract(address=token_address, abi=abi)
    token_symbol = token_contract.functions.symbol().call()
    token_decimals = token_contract.functions.decimals().call()
    token = Token(symbol=token_symbol, decimal=token_decimals, address=token_address)
    token.amount = token_reserve
    return token

# pools = get_pools_test_chain()
# while True:
#     update_pools(web3, pools)
# print(pools)