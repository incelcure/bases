from typing import Any


class EtherBaseClass:
    __slots__ = 'name'

    def __init__(self, name: Any, *args, **kwargs):
        self.name = str(name)

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.name}'
