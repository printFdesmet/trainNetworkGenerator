import unittest

from stadler.flirt import Flirt


class TestFlirt(unittest.TestCase):
    flirt = Flirt(config="data/stadler/switches_a.csv",
                  total_amount_consists=0,
                  switch="A1",
                  vehicle_name="BMU-B3")


if __name__ == '__main__':
    unittest.main()
