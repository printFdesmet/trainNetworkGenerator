import unittest

from stadler.stadler import Stadler


class TestStadler(unittest.TestCase):
    stadler = Stadler(total_amount_consists=0,
                      vehicle_name="BMU-B3",
                      )

    def test_chosen_train(self):
        result = self.stadler.chosen_train()

        self.assertEqual(result, ["A1", "A2", "A3",
                                  "C1", "C2",
                                  "D1", "D2", "D3",
                                  "P1"])


if __name__ == '__main__':
    unittest.main()
