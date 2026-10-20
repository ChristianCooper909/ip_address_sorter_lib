import unittest

import ip_address_sorter_lib
from ip_address_sorter_lib import sort_ip_addresses
from ip_address_sorter_lib.core import _normalize


class TestSortIPAddresses(unittest.TestCase):
    def test_module_exports_sort_ip_addresses(self):
        self.assertTrue(hasattr(ip_address_sorter_lib, "sort_ip_addresses"))
        self.assertIs(
            ip_address_sorter_lib.sort_ip_addresses, sort_ip_addresses
        )

    def test_empty_input_returns_empty_list(self):
        self.assertEqual(sort_ip_addresses([]), [])

    def test_ipv4_addresses_sorted_numerically(self):
        result = sort_ip_addresses(["192.0.2.10", "192.0.2.2", "192.0.2.1"])
        self.assertEqual(result, ["192.0.2.1", "192.0.2.2", "192.0.2.10"])

    def test_ipv4_hosts_and_ranges_sorted_together(self):
        result = sort_ip_addresses(
            ["192.0.2.5", "192.0.2.0/24", "192.0.2.129"]
        )
        self.assertEqual(
            result, ["192.0.2.0/24", "192.0.2.5", "192.0.2.129"]
        )

    def test_ipv6_addresses_sorted_numerically(self):
        result = sort_ip_addresses(
            ["2001:db8::ff", "2001:db8::1", "2001:db8::10"]
        )
        self.assertEqual(
            result, ["2001:db8::1", "2001:db8::10", "2001:db8::ff"]
        )

    def test_ipv6_hosts_and_ranges_sorted_together(self):
        result = sort_ip_addresses(
            ["2001:db8:1::5", "2001:db8::/32", "2001:db8:1::2"]
        )
        self.assertEqual(
            result, ["2001:db8::/32", "2001:db8:1::2", "2001:db8:1::5"]
        )

    def test_ipv4_sorts_before_ipv6(self):
        result = sort_ip_addresses(["::1", "255.255.255.255", "0.0.0.0"])
        self.assertEqual(result, ["0.0.0.0", "255.255.255.255", "::1"])

    def test_mixed_families_with_ranges(self):
        result = sort_ip_addresses(
            ["2001:db8::/32", "192.0.2.0/24", "2001:db8::1", "192.0.2.1"]
        )
        self.assertEqual(
            result,
            ["192.0.2.0/24", "192.0.2.1", "2001:db8::/32", "2001:db8::1"],
        )

    def test_ranges_with_same_network_address_more_specific_last(self):
        result = sort_ip_addresses(["10.0.0.0/24", "10.0.0.0/8", "10.0.0.0/30"])
        self.assertEqual(
            result, ["10.0.0.0/8", "10.0.0.0/24", "10.0.0.0/30"]
        )

    def test_input_list_is_not_mutated(self):
        original = ["10.0.0.2", "10.0.0.1", "10.0.0.3"]
        sort_ip_addresses(original)
        self.assertEqual(original, ["10.0.0.2", "10.0.0.1", "10.0.0.3"])

    def test_tuple_input_accepted(self):
        result = sort_ip_addresses(("192.0.2.2", "192.0.2.1"))
        self.assertEqual(result, ["192.0.2.1", "192.0.2.2"])

    def test_invalid_string_raises_value_error(self):
        with self.assertRaises(ValueError):
            sort_ip_addresses(["not-an-ip"])

    def test_host_bits_in_strict_network_form_rejected(self):
        with self.assertRaises(ValueError):
            _normalize("10.0.0.1/8")


if __name__ == "__main__":
    unittest.main()
