# magic
MAINNET = 0xAB44AB55
TESTNET = 0xBCABCB04

# can serve txs
NODE_NETWORK = 1

# can serve bloomed txs
NODE_BLOOM = 1 << 7

# supports SegWit data
NODE_WITNESS = 1 << 30

# compact block filter support
NODE_COMPACT_FILTERS = 1 << 6

# node is running in limited mode and will
# only connect to full nodes that have
# NODE_NETWORK set
NODE_NETWORK_LIMITED = 1 << 10

# THIS NODE

# version
version = hex(51652)[2:][::-1]

# node's current services
services = NODE_NETWORK | NODE_BLOOM

KNOWN_NODES = []
