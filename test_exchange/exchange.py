import os
import json

from chains import TestChain
from classes.exchange import Exchange
from .contracts import get_pools_test_chain, update_pools
from .calculate import calculate

__name = 'test_exchange'
__chains = [TestChain]
__baseDir = os.path.dirname(os.path.abspath(__file__))
__contractAbi = json.load(open(__baseDir + '/data/uniswap_pair_abi.json'))
__token_abi = json.load(open(__baseDir + '/data/erc20_abi.json'))

TestExchange = Exchange(
    name=__name,
    chains=__chains,
    contract_abi=__contractAbi,
    token_abi=__token_abi,
    calculate_func=calculate
)

# Chains
PolygonChain = TestExchange.get_chain_by_name('Polygon')
PolygonChain.set_function_to_get_pools(
    function=get_pools_test_chain,
    args=(TestExchange.chains[0].link, __contractAbi, __token_abi)
)
PolygonChain.set_func_to_update(update_pools)
