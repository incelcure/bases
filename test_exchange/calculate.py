from typing import List, Union

from classes.pool import PathPool


def calculate(values: List[Union[float, int]], path_pool: PathPool) -> List[Union[float, int]]:
    token1, token2 = path_pool.tokens[0], path_pool.tokens[1]
    reserve1, reserve2 = token1.amount, token2.amount
    swap_fee = path_pool.swap_fee

    amount_in = values[0]
    if token1.symbol == path_pool.tokens[0].symbol:
        amount_out = (amount_in * reserve2) / (reserve1 + amount_in * (1 - swap_fee))
    else:
        amount_out = (amount_in * reserve1) / (reserve2 + amount_in * (1 - swap_fee))

    return [amount_out]
