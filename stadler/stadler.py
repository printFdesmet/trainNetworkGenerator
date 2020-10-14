import sys

from train_network import TrainNetwork


class Stadler(TrainNetwork):
    """
    This class represents the base template for all the Stadler projects.
    """

    def __init__(self, total_amount_consists, vehicle_name, config=None):
        super().__init__(config, total_amount_consists, switch=None)
        self.total_amount_consists = total_amount_consists
        self.vehicle_name = vehicle_name

    def chosen_train(self):
        """
        This method validates which vehicle has been chosen, selects the
        corresponding list (list of switches) and returns it.

        :return: list
        """
        # Different amount of switches per vehicle type.
        dmu_4 = ["A1", "A2", "A3",
                 "B1", "B2",
                 "C1", "C2",
                 "D1", "D2", "D3",
                 "P1"]

        bmu_b3 = ["A1", "A2", "A3",
                  "C1", "C2",
                  "D1", "D2", "D3",
                  "P1"]

        bmu_b4 = ["A1", "A2", "A3",
                  "B1", "B2",
                  "C1", "C2",
                  "D1", "D2", "D3",
                  "P1"]

        # Return list depending from the chosen vehicle type.
        if self.vehicle_name == "DMU4":
            return dmu_4
        elif self.vehicle_name == "BMU-B3":
            return bmu_b3
        elif self.vehicle_name == "BMU-B4":
            return bmu_b4
        else:
            print(f"The vehicle {self.vehicle_name} does not exist.")
            return sys.exit()

    def replace_faulty_values(self, ip_list, port_list):
        """
        This method replaces the template values in the column
        with the generated ones.

        :param ip_list: list
        :param port_list: list
        :return: dataframe
        """
        dataframe = self.read_network_config()
        ip_dict = {}
        row = dataframe.first_valid_index()

        # Replaces the IPs in the dataframe.
        for ip in range(len(ip_list)):
            ip_dict.update({dataframe["ip"][row]: ip_list[ip]})
            row += 1

        dataframe.replace({"ip": ip_dict}, inplace=True)

        uplink_ports = {
            'G1': ['13', '25'],
            'G2': ['14', '26'],
            'G3': ['15', '27'],
            'G4': ['16', '28'],
        }

        dataframe["Port"] = dataframe["Port"].str.upper()

        # Replaces the uplink ports in the dataframe.
        if len(port_list) <= 16:
            for port in dataframe["Port"]:
                if uplink_ports.get(port) is not None:
                    dataframe.replace({"Port": port}, uplink_ports[port][0],
                                      inplace=True)
        else:
            for port in dataframe["Port"]:
                if uplink_ports.get(port) is not None:
                    dataframe.replace({"Port": port}, uplink_ports[port][1],
                                      inplace=True)

        return dataframe
