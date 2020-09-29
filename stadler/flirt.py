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

        df = self.replace_faulty_values(
            ip_list=converted_ip_list,
            port_list=port_list)

        switch_row = df.loc[df["Function"] == "switch"]
        switch_ip = switch_row["ip"].values

        port_based_ip_row_list = df.loc[df["Port"] != ""]
        port_based_ip_list = port_based_ip_row_list["ip"].values

        ports_row = df.loc[df["Port"] != ""]
        ports = ports_row["Port"].values

        vlan_row = df.loc[df["VLAN ID"] != ""]
        vlan = vlan_row["VLAN ID"].values

        poe = df["PoE power demand"].values

        coupling_port_row = df[df["Function"].str.contains("coupling", na=False)]
        coupling_port = coupling_port_row["Port"].values

        functions = df["Function"].values

        switch_name = df["Position"].values[0]

        netmask = "255.128.0.0"  # CIDR /9

        moxa = Moxa(
            coupling_port=coupling_port,
            functions=functions,
            ini_file="data/moxa/moxa_4500a_16.ini",
            netmask=netmask,
            poe=poe,
            ports=ports,
            port_based_ip_list=port_based_ip_list,
            vlan=vlan,
            switch_ip=switch_ip,
            switch_name=switch_name
                    )
        # moxa.generate_ini_file()

        print(df)

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
        #
        # if self.vehicle_name == "DMU4":
        #     return df.to_csv(
        #         f"data/stadler/DMU4/flirt{self.vehicle_name}"
        #         f"_consist{self.total_amount_consists + 1}"
        #         f"_switch_{self.switch}.csv")
        # elif self.vehicle_name == "BMU-B3":
        #     return df.to_csv(
        #         f"data/stadler/BMU-B3/flirt{self.vehicle_name}"
        #         f"_consist{self.total_amount_consists + 1}"
        #         f"_switch_{self.switch}.csv")
        # elif self.vehicle_name == "BMU-B4":
        #     return df.to_csv(
        #         f"data/stadler/BMU-B4/flirt{self.vehicle_name}"
        #         f"_consist{self.total_amount_consists + 1}"
        #         f"_switch_{self.switch}.csv")
