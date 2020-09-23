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
        switch_information = self.read_network_config()

        if switch_information.empty:
            return f"No information available for switch {self.switch}"

        ip_list = switch_information["ip"].tolist()
        port_list = switch_information["port"].tolist()
        vlan_list = switch_information["vlan id"].tolist()

        # moxa = Moxa(ini_file="data/moxa/moxa_4500a_16.ini")
        # moxa_information = moxa.convert_ini_file_to_list()
        # for line in moxa_information:
        #     if "#" not in line:
        #         print(line)

        gis = GenerateIPForStadler(
            consist_number=self.total_amount_consists,
            ip=ip_list,
            vehicle_name=self.vehicle_name,
            vlan_id=vlan_list)
        converted_ip_list = gis.generate_unique_ip()

        data_with_updated_ip_columns = self.replace_faulty_values(
            ip_list=converted_ip_list,
            port_list=port_list)

        return data_with_updated_ip_columns
