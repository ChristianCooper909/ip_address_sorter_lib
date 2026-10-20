from __future__ import annotations

import ipaddress
from typing import List, Union

__all__ = ["sort_ip_addresses"]


def _normalize(value: str) -> ipaddress._BaseNetwork:
    """
    Convert a textual address or range into an ``_BaseNetwork`` instance.

    ``ipaddress`` exposes ``ip_address`` and ``ip_network`` as separate
    functions, which forces a branch on every input otherwise. A bare address
    like ``192.0.2.1`` is not a valid network with a prefix, so we tell
    ``ip_network`` to treat it as a single-host network. This collapses the
    type space: everything downstream works on one concrete type and one sort
    key shape, IPv4 and IPv6 alike.

    Raises ``ValueError`` if the string is not a valid IPv4 or IPv6 address
    or network.
    """
    return ipaddress.ip_network(value, strict=True)


def _format(net: ipaddress._BaseNetwork) -> str:
    """
    Return the canonical string for a network.

    A single-host network (``/32`` for IPv4, ``/128`` for IPv6) is printed
    as a bare address so that inputs like ``192.0.2.1`` round-trip back to
    ``192.0.2.1`` rather than ``192.0.2.1/32``.
    """
    if net.prefixlen == net.max_prefixlen:
        return str(net.network_address)
    return str(net)


def sort_ip_addresses(
    items: Union[List[str], tuple],
) -> List[str]:
    """
    Sort a mixed list of IPv4 and IPv6 addresses and ranges in numeric order.

    Each element must be a textual address (``192.0.2.1``, ``2001:db8::1``) or
    a range in CIDR notation (``192.0.2.0/24``, ``2001:db8::/32``). Invalid
    strings raise ``ValueError``.

    The sort key is a tuple of
    ``(version, network_address-as-int, prefixlen)``.

    The ``version`` field comes first so all IPv4 sorts before all IPv6.
    The decision to group by family rather than interleaving is deliberate:
    when a caller hands you a mixed list, mixing a ``::1`` at numeric value 1
    between ``0.0.0.0`` and ``0.0.0.8`` surprises people more than it helps.

    The prefix length is the tiebreaker so that, within an overlapping set
    of ranges, the more specific (longer prefix) range sorts after the less
    specific one.

    The input is copied before use. Sorting a caller's list in place would be
    a surprising side effect for a function whose name promises a return
    value.
    """
    normalized = [_normalize(str(item)) for item in list(items)]
    normalized.sort(
        key=lambda net: (net.version, int(net.network_address), net.prefixlen)
    )
    return [_format(net) for net in normalized]
