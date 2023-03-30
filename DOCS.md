# Documentation

The header of each message is the command name, followed by padding of bytes in little-endian format. All data is in little-endian format, unless specified otherwise.

### version

The version message is the first packet sent by a client that wants to sync with a full or semi-full node.

| Field Size  | Description | Data Type     | Comments |
| :---        |    :----:   |   :----:      | ---: |
| 4 bytes     | Version (magic)| int32_t    | Protocol version used by node |
| 8 bytes     | Services    | uint64_t      | bitfield of enabled connection features |
| 8 bytes     | Timestamp   | int64_t       | UNIX time in seconds |
| 22 bytes    | addr_recv   | net_addr      | address of the node receiving the message |
| 8 bytes     | Command     | char[12]      | ASCII string that identifies the packet content |
| 4 bytes     | Length      | uint32_t      | Length of payload in number of bytes |
| 8 bytes     | Nonce       | uint64_t      | Node random nonce helps detect self-connections |
| 4 bytes     | Checksum    | uint32_t      | First 4 bytes of dhash(payload) |

### verack

The verack message is the first packet sent by a node that agrees to connect with a client.

| Field Size  | Description | Data Type     | Comments |
| :---        |    :----:   |   :----:      | ---: |
| 4 bytes     | Version (magic)| int32_t    | Protocol version used by node |
| 8 bytes     | Command     | char[12]      | ASCII string that identifies the packet content |
| 4 bytes     | Checksum    | uint32_t      | First 4 bytes of dhash(version + command) |

## General Packing Functions

### addr_recv

The address recv packing function is 22 bytes, with the IPv6 function arranged in big-endian byte order. Timestamp is NOT included in version message.

| Field Size  | Description | Data Type     | Comments |
| :---        |    :----:   |   :----:      | ---: |
| 8 bytes     | Timestamp   | int64_t       | Protocol version used by node |
| 8 bytes     | Services    | uint64_t      | bitfield of enabled connection features |
| 12 bytes    | IPv6        | char[]        | IPv6 address of the emitting node |
| 2 bytes     | Port        | uint16_t      | Port of the outgoing connection |


