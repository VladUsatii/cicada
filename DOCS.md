# Documentation

The header of each message is the command name, followed by padding of bytes in little-endian format. All data is in little-endian format, unless specified otherwise.

### version

The version message is the first packet sent by a client that wants to sync with a full or semi-full node.

| Field Size  | Description | Data Type     | Comments |
| :---        |    :----:   |   :----:      | ---: |
| 4 bytes     | Version (magic)| int32_t    | Protocol version used by node |
| 8 bytes     | Command     | char[12]      | ASCII string that identifies the packet content |
| 4 bytes     | Length      | uint32_t      | Length of payload in number of bytes |
| 4 bytes     | Checksum    | uint32_t      | First 4 bytes of dhash(payload) |
| 0 bytes     | Payload     | uchar[]       | Empty data |


### verack

The verack message is the first packet sent by a node that agrees to connect with a client.

| Field Size  | Description | Data Type     | Comments |
| :---        |    :----:   |   :----:      | ---: |
| 4 bytes     | Version (magic)| int32_t    | Protocol version used by node |
| 8 bytes     | Command     | char[12]      | ASCII string that identifies the packet content |
| 4 bytes     | Checksum    | uint32_t      | First 4 bytes of dhash(version + command) |


