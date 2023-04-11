# Documentation

The header of each message is the command name, followed by padding of bytes in little-endian format. All data is in little-endian format, unless specified otherwise.

### message_struct

| Field Size  | Description | Data Type     | Comments |
| :---        |    :----:   |   :----:      | ---: |
| 4 bytes     | Magic       | uint32_t      | Message origin network value |
| 12 bytes    | Command     | char[12]      | ASCII string identifying packet content, NULL padded |
| 4 bytes     | Length      | uint32_t      | Length of payload in bytes |
| 4 bytes     | Checksum    | uint32_t      | dhash(payload)[:4] |
| ? bytes     | Payload     | uchar[]       | The payload's data (e.g. packed version message) |

### version

The version message is the first packet sent by a client that wants to sync with a full or semi-full node.

| Field Size  | Description | Data Type     | Comments |
| :---        |    :----:   |   :----:      | ---: |
| 4 bytes     | Version     | int32_t       | Protocol version used by node |
| 8 bytes     | Services    | uint64_t      | bitfield of enabled connection features |
| 8 bytes     | Timestamp   | int64_t       | UNIX time in seconds |
| 26 bytes    | addr_recv   | net_addr      | address of the node receiving the message |
| 8 bytes     | Nonce       | uint64_t      | Node random nonce helps detect self-connections |

### verack

The verack message is the first packet sent by a node that agrees to connect with a client. It doesn't follow the message_struct. It is in and of itself a unique message structure called verack.

| Field Size  | Description | Data Type | Comments |
| :---        |    :----:   |   :----:  | ---: |
| 4 bytes     | Magic       | uint32_t  | Message origin network value |
| 12 bytes    | Command     | char[12]  | ASCII string identifying packet content, NULL padded; it should state verack |
| 4 bytes     | Payload     | uchar[4]  | Unsigned payload field |
| 4 bytes     | Checksum    | uint32_t  | dhash(Magic + Command + Payload)[:4] |

## General Packing Functions

### addr_recv

The address recv packing function is 34 bytes, with the IPv6 function arranged in big-endian byte order. Timestamp is NOT included in version message.

| Field Size  | Description | Data Type     | Comments |
| :---        |    :----:   |   :----:      | ---: |
| 8 bytes     | Timestamp   | int64_t       | Protocol version used by node |
| 8 bytes     | Services    | uint64_t      | bitfield of enabled connection features |
| 16 bytes    | IPv6        | char[16]        | IPv4-mapped IPv6 address of the emitting node |
| 2 bytes     | Port        | uint16_t      | Port of the outgoing connection |


