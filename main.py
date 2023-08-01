from uniswap.exchange import TestExchange
from tests import test_data


def main():
    exchange = TestExchange
    rpc_url = exchange.chains[0].link
    contract_abi = exchange.contract_abi
    token_abi = exchange.token_abi

    exchange.chains[0].set_pools(rpc_url, contract_abi, token_abi)
    pools = exchange.chains[0].pools

    while True:
        exchange.chains[0].update(pools, rpc_url, contract_abi)
        for data in test_data:
            amount_in, token0_symbol, token1_symbol = data
            path_pool = exchange.chains[0].find_pool_by_tokens_names((token0_symbol, token1_symbol))
            if path_pool:
                output_tokens = exchange.calculate((amount_in,), path_pool)
                print(f"Amount in: {amount_in} {token0_symbol}, Amount out: {output_tokens[0]} {token1_symbol}")

        # list_of_results = [235.10, 5352.35, 315235.65, 10]
        # print(list_of_results)


if __name__ == '__main__':
    main()
