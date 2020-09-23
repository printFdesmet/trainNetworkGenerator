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
            data = pd.read_csv(self.config, encoding="ISO-8859-1", header=0)
            switch_information = \
                data[data["position"].str.contains(self.switch)]
            return switch_information
        except FileNotFoundError:
            print(f"The selected file {self.config} could not be found.")
