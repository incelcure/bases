from web3.contract import Contract
from web3 import Web3
from eth_typing import ChecksumAddress
from web3.types import ABI

from .types import (
    Symbol,
    Decimal,
    Amount,
    AmountWithoutDecimals,
    Optional
)
from .base import EtherBaseClass


class Token(EtherBaseClass):
    symbol: Symbol
    decimal: Optional[Decimal]
    address: Optional[ChecksumAddress]

    __amount: Optional[Amount]
    __reserves: Optional[AmountWithoutDecimals]
    __contract: Optional[Contract]

    def __init__(
            self,
            symbol: Symbol,
            decimal: Optional[Decimal] = None,
            address: Optional[ChecksumAddress] = None,
            pool=None
    ):
        super().__init__(name=symbol)

        self.symbol = symbol.lower()
        self.decimal = int(decimal) if isinstance(decimal, str) else decimal
        self.address = address

        self.__amount = None
        self.__reserves = None
        self.contract = None

        self.amount = 0

        if pool:
            self.pool = pool

    @property
    def pool(self):
        return self.__pool

    @pool.setter
    def pool(self, pool):
        self.__pool = pool
        _web3: Web3 = self.__pool.chain.web3
        _token_abi: ABI = self.__pool.chain.exchange.token_abi
        self.contract = _web3.eth.contract(_web3.to_checksum_address(self.address), abi=_token_abi)

    @property
    def amount(self) -> Optional[Amount]:
        try:
            if self.__amount is None:
                self.__amount = self.__reserves / 10 ** self.decimal
            return self.__amount
        except TypeError:
            return None

    @amount.setter
    def amount(self, reserves: AmountWithoutDecimals):
        self.__reserves = reserves
        self.__amount = None
