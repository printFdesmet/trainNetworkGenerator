import os
import unittest

from train_network import TrainNetwork


class MyTestCase(unittest.TestCase):
    # Take full path to prevent issues regarding path.
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, "switches_a.csv")

    network = TrainNetwork(config=file,
                           total_amount_consists=0,
                           switch="A1")

    # Validates if the returned dataframe is empty.
    def test_read_network_config(self):
        result = self.network.read_network_config()
        self.assertFalse(result.empty)


if __name__ == '__main__':
    unittest.main()
