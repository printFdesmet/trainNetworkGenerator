import unittest

from stadler.generate_ip_for_stadler import GenerateIPForStadler


class TestGenerateIPForStadler(unittest.TestCase):
    stadler_ip = GenerateIPForStadler(consist_number=0,
                                      ip=["10.x.y.40"],
                                      vehicle_name="BMU-B3",
                                      vlan_id=["2U"])

    def test_generate_unique_ip(self):
        result = self.stadler_ip.generate_unique_ip()
        self.assertEqual(result, ["10.22.1.40"])

    def test_generate_second_octet(self):
        result = self.stadler_ip.generate_second_octet()
        self.assertEqual(result, "22")

    def test_generate_third_octet(self):
        result = self.stadler_ip.generate_third_octet()
        self.assertEqual(result, "1")


if __name__ == '__main__':
    unittest.main()
