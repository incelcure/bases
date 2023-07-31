from typing import List, Union

from classes.pool import PathPool


def calculate(
        values: List[Union[float | int]],
        path_pool: PathPool,
        *args, **kwargs
) -> List[Union[float, int]]:
    x, y = path_pool.pool.get_decimals()

    # Объем токена, который хотим обменять
    amount = values[0]

    # Рассчитываем новые значения x' и y' после обмена
    x_prime = x + amount
    y_prime = x * y / x_prime

    # Возвращаем список с количеством токенов на выходе после свапа
    return [x_prime, y_prime]


def calculate(values: List[Union[float, int]], path_pool: PathPool) -> List[Union[float, int]]:
    # Получение токенов и резервов пула
    token1, token2 = path_pool.token1, path_pool.token2
    reserve1, reserve2 = token1.amount, token2.amount
    swap_fee = path_pool.pool.swap_fee

    # Подсчет количества токенов на выходе после свапа
    amount_in = values[0]
    if token1.symbol == path_pool.token1Symbol:
        amount_out = (amount_in * reserve2) / (reserve1 + amount_in * (1 - swap_fee))
    else:
        amount_out = (amount_in * reserve1) / (reserve2 + amount_in * (1 - swap_fee))

    # Возвращаем результат в виде списка
    return [amount_out]
