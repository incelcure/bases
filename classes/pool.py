from typing import (
    Tuple,
    Any,
    Union,
    List,
    Optional
)
import time
from web3.contract import Contract
from web3 import Web3
from eth_typing import ChecksumAddress
from web3.types import ABI
from eth_typing import URI

from .token import Token
from .types import SwapFee, Symbol, T
from .base import EtherBaseClass


class Pool(EtherBaseClass):
    tokens: Tuple[Token]
    address: ChecksumAddress
    swap_fee: SwapFee

    contract: Optional[Contract]

    last_update: int

    def __init__(
            self,
            tokens: Tuple[Token],
            address: ChecksumAddress,
            swap_fee: SwapFee,
            chain=None
    ):
        super().__init__(name='-'.join([token.name for token in tokens]))

        self.tokens = tokens
        self.swap_fee = swap_fee
        self.address = address

        self.contract = None
        if chain:
            self.chain = chain

        self.last_update = int(time.time())

    @property
    def scan_uri(self) -> URI:
        return self.chain.scan_uri + '/address/' + self.address

    @property
    def chain(self):
        return self.__chain

    @chain.setter
    def chain(self, chain):
        self.__chain = chain
        _web3: Web3 = self.__chain.web3
        _contract_abi: ABI = self.__chain.exchange.contract_abi
        self.contract = _web3.eth.contract(_web3.to_checksum_address(self.address), abi=_contract_abi)
        for token in self.tokens:
            token.pool = self

    def get_token_by_symbol(self, symbol: Symbol) -> Union[Token, None]:
        for token in self.tokens:
            if token.symbol == symbol:
                return token

    def get_decimals(self) -> List[int]:
        return [token.decimal for token in self.tokens]

    def set_new_argument(self, arg_name: str, arg_value: Any) -> None:
        self.__setattr__(arg_name, arg_value)

    @property
    def reserved(self) -> List[float]:
        return [token.amount for token in self.tokens]

    def update(self, *args: Any, **kwargs: Any):
        self.last_update = int(time.time())
        # Some function to update data in this pool


class PathPool(EtherBaseClass):
    pool: Pool
    token1Symbol: Symbol
    token2Symbol: Symbol
    token1: Token
    token2: Token

    __slots__ = 'pool', 'token1Symbol', 'token2Symbol', 'token1', 'token2'

    def __init__(self, pool: Pool, token1_symbol: Symbol, token2_symbol: Symbol):
        super().__init__(name=f'{token1_symbol}-{token2_symbol} ({pool.address})')
        self.pool = pool

        self.token1Symbol = token1_symbol
        self.token2Symbol = token2_symbol

        self.token1 = pool.get_token_by_symbol(token1_symbol)
        self.token2 = pool.get_token_by_symbol(token2_symbol)

    def create_reversed(self: T) -> T:
        return PathPool(
            pool=self.pool,
            token1_symbol=self.token2Symbol,
            token2_symbol=self.token1Symbol
        )
