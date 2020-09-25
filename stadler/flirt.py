"""
TODO: Loop over de config file.
TODO: Extract the rows for the current switch configuration.
TODO: From those rows extract the IP, VLAN ID and port.
TODO: Generate the correct IP from the formula.
TODO: Loop over the IP column, replacing the values with the generated ones.
TODO: Convert the Multicast address(es) to their MAC.
TODO: loop over the Multicast column replacing the IP value to the MAC variant.
"""
from moxa import Moxa
from stadler.generate_ip_for_stadler import GenerateIPForStadler
from stadler.stadler import Stadler


class Flirt(Stadler):
    """
    This class creates Flirt network configs.
    """

    def __init__(self, config, total_amount_consists, switch, vehicle_name):
        super().__init__(config, total_amount_consists, vehicle_name)

        self.config = config
        self.total_amount_consists = total_amount_consists
        self.switch = switch
        self.vehicle_name = vehicle_name

    def generate_flirt_switch_config(self):
        """
        This method reads in the current switch information alters the template
        values and returns them back in a csv format.
        :return: file
        """
        switch_information = self.read_network_config()
        if switch_information.empty:
            return f"No information available for switch {self.switch}"

        ip_list = switch_information["ip"].tolist()
        port_list = switch_information["Port"].tolist()
        vlan_list = switch_information["VLAN ID"].tolist()

        gis = GenerateIPForStadler(
            consist_number=self.total_amount_consists,
            ip=ip_list,
            vehicle_name=self.vehicle_name,
            vlan_id=vlan_list)
        converted_ip_list = gis.generate_unique_ip()

        data_with_updated_values = self.replace_faulty_values(
            ip_list=converted_ip_list,
            port_list=port_list)

        # moxa = Moxa("data/moxa/moxa_4500a_16.ini")
        # moxa_list = moxa.convert_ini_file_to_list()
        # print(moxa.generate_ini_file())
        # new_config_list = []
        # counter = 0
        # for line in moxa_list:
        #     if f"Port_{1}_EN" in line:
        #         replaced_line = line.replace('1\n', '0\n')
        #         new_config_list.append(replaced_line)
        #         print(new_config_list)
        #     if (f"Device_IP_{data_with_updated_values["Port]}") in line:
        #         replaced_line = line.replace('\n', '')

        # # print(data_with_updated_values)
        # return data_with_updated_values.to_csv(
        #     f"data/stadler/flirt{self.vehicle_name}"
        #     f"_consist{self.total_amount_consists + 1}_switch_{self.switch}.csv")

    def replace_lines(self):
        pass

