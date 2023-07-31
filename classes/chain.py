from typing import Tuple, Optional, Union, Callable, List
from web3 import Web3, AsyncWeb3, AsyncHTTPProvider
from eth_typing import URI

from .pool import Pool
from .base import EtherBaseClass


class ChainBase(EtherBaseClass):
    name: str
    links: Tuple[URI]

    web3: Web3
    web3Async: AsyncWeb3
    __link: URI

    def __init__(self, name: str, links: Tuple[URI], scan_uri: URI):
        super().__init__(name=name)
        self.name = name
        self.links = links
        self.scan_uri = scan_uri

        self.link = None

        self.web3 = Web3(Web3.HTTPProvider(self.link))
        self.web3Async = AsyncWeb3(AsyncHTTPProvider(self.link))

    @property
    def link(self) -> URI:
        return self.__link

    @link.setter
    def link(self, link_address: Optional[URI] = None):
        self.__link = link_address if link_address is not None else self.links[0]


class Chain(EtherBaseClass):
    name: str
    link: str
    web3: Web3
    web3Async: AsyncWeb3

    get_pools: Optional[Callable]
    calculate: Callable

    __pools: List[Pool]
    __update: Callable

    def __init__(
            self,
            chain_base: ChainBase,
            exchange=None
    ):
        super().__init__(name=chain_base.name)

        self.name, self.link, self.web3, self.web3Async = (
            chain_base.name,
            chain_base.link,
            chain_base.web3,
            chain_base.web3Async
        )
        self.get_pools = None
        self.__get_pools = None
        self.__paths = ()
        self.__update = lambda *args, **kwargs: None
        self.calculate = lambda *args, **kwargs: None
        if exchange:
            self.exchange = exchange

    @property
    def exchange(self):
        return self.__exchange

    @exchange.setter
    def exchange(self, exchange):
        self.__exchange = exchange

    def set_pools(self, *args, **kwargs):
        self.pools = self.__get_pools['function'](
            *self.__get_pools['args'],
            **self.__get_pools['kwargs']
        )

    def set_function_to_get_pools(self, function: Callable, args=None, kwargs=None):
        args = () if not args else args
        kwargs = {} if not kwargs else kwargs

        self.__get_pools = {
            'function': function,
            'args': args,
            'kwargs': kwargs
        }

    @property
    def pools(self) -> Union[List[Pool], Tuple]:
        try:
            return self.__pools
        except AttributeError:
            return ()

    @pools.setter
    def pools(self, pools_list: List[Pool]):
        self.__pools = pools_list
        for pool in self.__pools:
            pool.chain = self

    def set_func_to_update(self, function: Callable):
        self.__update = function

    def update(self, *args, **kwargs):
        self.__update(*args, **kwargs)

    @property
    def paths(self):
        return self.__paths

    @paths.setter
    def paths(self, paths):
        self.__paths = paths

    def find_pool_by_tokens_names(self, tokens_names: Tuple[str]) -> Optional[Pool]:
        for pool in self.pools:
            tokens_names_from_pool = [token.symbol for token in pool.tokens]
            if all([tk in tokens_names for tk in tokens_names_from_pool]):
                return pool
