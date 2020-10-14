import unittest

from multicast_to_mac import MulticastIPToMAC


class TestMulticastToMac(unittest.TestCase):
    ip_to_mac = MulticastIPToMAC("224.0.0.251")

    def test_verify_ip(self):
        # Verify if this is a valid Multicast address.
        result = self.ip_to_mac.verify_ip(self.ip_to_mac.multicast)
        self.assertTrue(result)

    def test_verify_octet(self):
        # Inspect each octet in an IP, validates True if not lower then 0
        # or higher then 255.
        octets = self.ip_to_mac.multicast.split(".")
        for octet in octets:
            self.assertTrue(octet)

    def test_ip2mac(self):
        # Test if the conversion process succeeded.
        result = self.ip_to_mac.ip2mac()
        self.assertEqual(result, "01-00-5e-00-00-fb")


if __name__ == '__main__':
    unittest.main()
