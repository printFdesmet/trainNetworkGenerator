"""
TODO: Replace the read_csv approach with the read_excel one. see read_excel.py
"""

import pandas as pd


class TrainNetwork:
    """
    This class generates network configuration files for the specified project.
    """

    def __init__(self, config, total_amount_consists, *switch):
        self.config = config
        self.total_amount_consist = total_amount_consists
        self.switch = switch

    def read_network_config(self):
        """
        This method reads in the config file of the project and returns the
        chosen switch its specifications.

        :return: dataframe
        """

        try:
            all_switches = pd.read_csv(self.config,
                                       encoding="ISO-8859-1",
                                       header=0)

            switch_information = all_switches[
                all_switches["Position"].str.contains(self.switch, na=False)
            ]
            return switch_information
        except FileNotFoundError:
            print(f"The selected file {self.config} could not be found.")
        except ValueError:
            print(f"There is an empty value that can't be processed.")
