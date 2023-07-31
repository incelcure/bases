from typing import Optional, Callable, List, Dict
from web3.types import ABI

from .chain import Chain, ChainBase
from .base import EtherBaseClass


class Exchange(EtherBaseClass):
    name: str
    chains: List[Chain]

    calculate: Optional[Callable]

    def __init__(
            self,
            name: str,
            chains: List[ChainBase],
            contract_abi: ABI = None,
            token_abi: ABI = None,
            calculate_func: Optional[Callable] = None,
            configs: Optional = None,
            contract_abis: Dict[int, ABI] = None,
            token_abis: Dict[int, ABI] = None
    ):
        super().__init__(name=name)

        self.name = name
        self.calculate = (lambda *args, **kwargs: 0) if calculate_func is None else calculate_func
        self.contract_abi = contract_abi
        self.token_abi = token_abi
        self.chains = [Chain(chain_base=chainBase, exchange=self) for chainBase in chains]
        self.configs = configs

        contract_abis = contract_abis if contract_abis is not None else {}
        token_abis = token_abis if token_abis is not None else {}

        base_version = 3

        if base_version not in contract_abis:
            contract_abis[base_version] = contract_abi
        if base_version not in token_abis:
            token_abis[base_version] = token_abi

        self.contract_abis = contract_abis
        self.token_abis = token_abis

    def get_chain_by_name(self, name: str) -> Optional[Chain]:
        for chain in self.chains:
            if chain.name == name:
                return chain

    def del_chain_by_name(self, chain_name: str) -> None:
        chain = self.get_chain_by_name(chain_name)
        del self.chains[self.chains.index(chain)]

    def update(self):
        for chain in self.chains:
            chain.update()

    def set_func_to_calculate(self, calculate_func: Callable):
        self.calculate = calculate_func
