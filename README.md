# ip_address_sorter_lib

Sort a mixed list of IPv4 and IPv6 addresses and ranges in proper numeric
order. Pure standard library, no dependencies.

```python
from ip_address_sorter_lib import sort_ip_addresses

result = sort_ip_addresses(["2001:db8::1", "10.0.0.0/8", "192.0.2.1"])
# ['10.0.0.0/8', '192.0.2.1', '2001:db8::1']
```

The exported name is `sort_ip_addresses`. It takes a list or tuple of strings
and returns a list of strings.

## Why this exists

`ipaddress` exposes `ip_address` and `ip_network` as separate functions, so a
mixed list of bare addresses and CIDR ranges needs a branch on every element.
This library normalizes everything to `ip_network` (treating a bare address as
a `/32` for IPv4 or `/128` for IPv6) and sorts on a single key shape across
both families.

## Sort order and one deliberate decision

The sort key is `(version, network_address-as-int, prefixlen)`. The leading
`version` field groups all IPv4 before all IPv6. That is a choice: interleaving
`::1` between `0.0.0.0` and `0.0.0.8` by raw integer value is technically
defensible but surprises people in practice. If you want interleaved numeric
order across families, this library does not do that.

Within a family, bare hosts and CIDR ranges sort together by network address.
Where two ranges share a network address, the shorter prefix (broader range)
comes first; the longer prefix (more specific) comes after.

## Edge you will hit

Host bits in a strict CIDR form are rejected. `10.0.0.1/8` raises
`ValueError`; the canonical network form `10.0.0.0/8` is expected. Any string
that is neither a valid address nor a valid network raises `ValueError`.
