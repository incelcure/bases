from test_exchange.exchange import TestExchange
from tests import test_data
import time


def main():
    exchange = TestExchange
    print(f'link: {exchange.chains[0].link}')
    print(f'contract_abi: {exchange.contract_abi}')

    rpc_url = exchange.chains[0].link
    contract_abi = exchange.contract_abi
    token_abi = exchange.token_abi

    exchange.chains[0].set_pools(rpc_url, contract_abi, token_abi)

    pools = exchange.chains[0].pools
    print(f'pools: {pools}')

    while True:
        """
        Здесь нужно будет каждый цикл обновлять данные в пулах и
        выводить результат подсчётов после свапов (список) на основе списка test_data( tests.py ),
        где:
        1) количество token0, которое нужно будет свапнуть
        2) token0_symbol
        3) token1_symbol
        """
        print('Loop')
        exchange.chains[0].update(pools, rpc_url, contract_abi)
        for data in test_data:
            amount_in, token0_symbol, token1_symbol = data
            path_pool = exchange.chains[0].find_pool_by_tokens_names((token0_symbol, token1_symbol))
            if path_pool:
                output_tokens = exchange.calculate((amount_in,), path_pool)
                print(f"Amount in: {amount_in} {token0_symbol}, Amount out: {output_tokens[0]} {token1_symbol}")
                time.sleep(5)
        # list_of_results = [235.10, 5352.35, 315235.65, 10]
        # print(list_of_results)


if __name__ == '__main__':
    main()
