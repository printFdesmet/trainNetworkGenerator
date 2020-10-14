import csv

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
        self.read_network_config_excel()

        # Dataframe containing the current switch data.
        switch_information = self.read_network_config()
        if switch_information.empty:
            return f"No information available for switch {self.switch}"

        # Extracting values from the dataframe.
        ip_list = switch_information["ip"].tolist()
        port_list = switch_information["Port"].tolist()
        vlan_list = switch_information["VLAN ID"].tolist()

        # Instantiate IP class and return list of adjusted IPs.
        gis = GenerateIPForStadler(
            consist_number=self.total_amount_consists,
            ip=ip_list,
            vehicle_name=self.vehicle_name,
            vlan_id=vlan_list)
        converted_ip_list = gis.generate_unique_ip()

        # Replaces the Uplink port values from G1, to numeric values 25.
        df = self.replace_faulty_values(
            ip_list=converted_ip_list,
            port_list=port_list)

        # Extracting values.
        switch_row = df.loc[df["Function"] == "switch"]
        switch_ip = switch_row["ip"].values

        # Extracting values.
        port_based_ip_row_list = df.loc[df["Port"] != ""]
        port_based_ip_list = port_based_ip_row_list["ip"].values

        # Extracting values.
        ports_row = df.loc[df["Port"] != ""]
        ports = ports_row["Port"].values

        # Extracting values.
        vlan_row = df.loc[df["VLAN ID"] != ""]
        vlan = vlan_row["VLAN ID"].values

        # Extracting values.
        poe = df["PoE power demand"].values

        # Check to evaluate if the switch has a coupler or not and is
        # Primary or backup depending on the topology.
        if self.switch == "A1" or self.switch == "D1":
            coupling_port_row = df[df["Function"].str.contains("coupling", na=False)]
            coupling_port = coupling_port_row["Port"].values
            coupling_mode = "3"  # Primary coupling
        elif self.switch == "A3" or self.switch == "D3":
            coupling_port_row = df[df["Function"].str.contains("coupling", na=False)]
            coupling_port = coupling_port_row["Port"].values
            coupling_mode = "2"  # Backup coupling
        else:  # Default in file
            coupling_port = "14"
            coupling_mode = "0"

        # Extracting values.
        functions = df["Function"].values

        # Extracting values.
        switch_name = df["Position"].values[0]

        netmask = "255.128.0.0"  # CIDR /9

        # Extracting values.
        management_vlan_row = df.loc[df["Function"] == "switch"]
        management_vlan = management_vlan_row["VLAN ID"].values

        # Extracting values.
        redundancy_ports_row = df.loc[df["Function"] == "Ring PIS/VSS/PAN"]
        redundancy_ports = redundancy_ports_row["Port"].values
        redundant_protocol = "2"  # Turbo Ring V2.

        # Set the Ring Master on the C2 switch, to prevent auto propagation
        # and have the Master on a coupler switch.
        ring_master = "0"
        if self.switch == "C2":
            ring_master = "1"

        # Extract the multiple VLANs on a port in its respective target.
        tagged_ports = []
        untagged_ports = []
        untagged = ""
        for vlans in vlan:
            if "U" in str(vlans):
                untagged = vlans.find("U")
                untagged -= 1
                untagged_ports.append(vlans[untagged])
            else:
                untagged_ports.append("")
            if "T" in str(vlans) and "U" in str(vlans):
                tagged = vlans.replace(f"{vlans[untagged]}U,", "")
                tagged = tagged.replace(f"T", "")
                tagged_ports.append(tagged)
            elif "T" in str(vlans):
                tagged = vlans.replace(f"T", "")
                tagged_ports.append(tagged)
            else:
                tagged_ports.append("")

        # Instantiate the Moxa class
        moxa = Moxa(
            coupling_mode=coupling_mode,
            coupling_port=coupling_port,
            functions=functions,
            ini_file="data/moxa/moxa_4500a_16.ini",
            management_vlan=management_vlan,
            netmask=netmask,
            poe=poe,
            ports=ports,
            port_based_ip_list=port_based_ip_list,
            vlan=vlan,
            redundancy_ports=redundancy_ports,
            redundant_protocol=redundant_protocol,
            ring_master=ring_master,
            switch_ip=switch_ip,
            switch_name=f"Consist{self.total_amount_consists + 1}"
                        f"_Switch{switch_name[-2:]}",
            tagged_ports=tagged_ports,
            untagged_ports=untagged_ports
        )

        # Test return output in CSV format.
        # return df.to_csv(
        #     f"data/stadler/flirt{self.vehicle_name}"
        #     f"_consist{self.total_amount_consists + 1}_switch_{self.switch}.csv")

        # Return a list with the values replaced by the passed ones.
        # moxa_config_list = moxa.generate_ini_file()

        # Create an IP-Table for the Network Documentation.
        # # self.create_ip_table(ip_list=port_based_ip_list,
        # #                      name_list=functions,
        # #                      vlan_list=vlan_list)
        # Take the Moxa list and write them to an .INI file.
        # self.make_ini_file(config_list=moxa_config_list,
        #                    moxa=moxa)

    # Make a .INI file for the current switch, type and consist.
    def make_ini_file(self, config_list, moxa):
        if self.vehicle_name == "DMU4":
            dmu4_config = f"data/stadler/DMU4/flirtV2{self.vehicle_name}" \
                          f"_consist{self.total_amount_consists + 1}" \
                          f"_switch_{self.switch}.ini"
            moxa.write_ini_file(dmu4_config, config_list)
        elif self.vehicle_name == "BMU-B3":
            bmub3_config = f"data/stadler/BMU-B3/flirtV2{self.vehicle_name}" \
                           f"_consist{self.total_amount_consists + 1}" \
                           f"_switch_{self.switch}.ini"
            moxa.write_ini_file(bmub3_config, config_list)
        elif self.vehicle_name == "BMU-B4":
            bmub4_config = f"data/stadler/BMU-B4/flirtV2{self.vehicle_name}" \
                           f"_consist{self.total_amount_consists + 1}" \
                           f"_switch_{self.switch}.ini"
            moxa.write_ini_file(bmub4_config, config_list)

    # Write values necessary for the IP-table to a CSV file.
    @staticmethod
    def create_ip_table(ip_list, name_list, vlan_list):
        with open("IP_TABLE.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerows(zip(name_list, ip_list, vlan_list))
