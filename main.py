from test_exchange.exchange import TestExchange
from tests import test_data


def main():
    # Подгрузка данных

    # Создаем объект биржи
    exchange = TestExchange
    print(f'link: {exchange.chains[0].link}')
    print(f'contract_abi: {exchange.contract_abi}')

    # polygon_chain = TestExchange.chains[0]
    # Инициализируем пулы
    exchange.chains[0].set_pools()
    # polygon_chain.set_pools()
    # print(exchange.chains[0].get_pools)
    # print(polygon_chain.get_pools)
    while True:
        """
        Здесь нужно будет каждый цикл обновлять данные в пулах и
        выводить результат подсчётов после свапов (список) на основе списка test_data( tests.py ),
        где:
        1) количество token0, которое нужно будет свапнуть
        2) token0_symbol
        3) token1_symbol
        """
        # Обновляем данные в пулах
        pools = exchange.chains[0].pools
        print(type(pools))
        print(pools)
        exchange.chains[0].update(pools)
        # rpc = exchange.chains[0].links[0]
        # polygon_chain.update()
        print(f'Pools: {pools}')
        # Подсчитываем количество токенов на выходе после свапа
        for data in test_data:
            amount_in, token0_symbol, token1_symbol = data
            path_pool = exchange.chains[0].find_pool_by_tokens_names((token0_symbol, token1_symbol))
            # path_pool = polygon_chain.find_pool_by_tokens_names((token0_symbol, token1_symbol))
            if path_pool:
                output_tokens = exchange.calculate((amount_in,), path_pool)
                print(f"Amount in: {amount_in} {token0_symbol}, Amount out: {output_tokens[0]} {token1_symbol}")
        list_of_results = [235.10, 5352.35, 315235.65, 10]
        print(list_of_results)


if __name__ == '__main__':
    main()
