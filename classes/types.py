from typing import TypeVar, Optional

Symbol = str
Amount = TypeVar('Amount', int, float)
AmountWithoutDecimals = int
Decimal = int
SwapFee = Optional[float]
SignalWithIndexesAndResult = TypeVar('SignalWithIndexesAndResult')
T = TypeVar('T')

