from typing import Tuple
from eth_typing import URI

from classes.chain import ChainBase

__links: Tuple[URI] = (
    URI('https://polygon-rpc.com'),
    URI('https://polygon.meowrpc.com'),
)

TestChain = ChainBase(
    name='Polygon',
    links=__links,
    scan_uri=URI('https://polygonscan.com')
)

# TestChain2 = ChainBase(
#     name='Polygon',
#     links=__links,
#     scan_uri=URI('https://polygonscan.com')
# )

