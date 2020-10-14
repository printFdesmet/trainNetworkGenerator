import pandas as pd


class TrainNetwork:
    """
    This class generates network configuration files for the specified project.
    """

    def __init__(self, config, total_amount_consists, switch):
        self.config = config
        self.total_amount_consist = total_amount_consists
        self.switch = switch

    def read_network_config(self):
        """
        This method reads in the csv config file of the project and returns the
        chosen switch its specifications.

        :return: dataframe
        """

        try:
            all_switches = pd.read_csv(self.config,
                                       encoding="ISO-8859-1",
                                       header=0)

            # Filter on the current switch only.
            switch_information = all_switches[
                all_switches["Position"].str.contains(self.switch, na=False)
            ]
            return switch_information
        except FileNotFoundError:
            print(f"The selected file {self.config} could not be found.")
        except ValueError:
            print(f"There is an empty value that can't be processed.")

    def read_network_config_excel(self):
        """
        This method reads in the excel config file of the project and returns the
        chosen switch its specifications.

        :return: dataframe
        """
        # Testing in progress, should replace the CSV Method.
        try:
            all_switches = pd.read_excel(r"data/stadler/BU_3794636.xlsx", sheet_name="BMU-A")
            switch_information = all_switches[
                all_switches["Position"].str.contains(self.switch, na=False)
            ]
            with pd.option_context('display.max_rows', None, 'display.max_columns',
                                   None):  # more options can be specified also
                print(switch_information)
        except FileNotFoundError:
            print(f"The selected file {self.config} could not be found.")
        except ValueError:
            print(f"There is an empty value that can't be processed.")
