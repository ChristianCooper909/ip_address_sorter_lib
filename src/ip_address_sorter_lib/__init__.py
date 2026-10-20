# ip_address_sorter_lib
"""
Sort mixed IPv4 and IPv6 addresses and ranges in proper numeric order.

Only the public name ``sort_ip_addresses`` is re-exported. Importing the
package root keeps the namespace small and makes the supported API explicit.
"""

from .core import sort_ip_addresses

__all__ = ["sort_ip_addresses"]
