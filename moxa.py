import numpy


class Moxa:
    """
    This class handles the importing, manipulation and recreation of the moxa
    init file.
    """

    def __init__(self, coupling_mode, coupling_port, functions, ini_file,
                 management_vlan, netmask, poe, ports, port_based_ip_list,
                 vlan, redundancy_ports, redundant_protocol, ring_master,
                 switch_ip, switch_name, tagged_ports, untagged_ports):
        self.coupling_mode = coupling_mode
        self.coupling_port = coupling_port
        self.functions = functions
        self.ini_file = ini_file
        self.management_vlan = management_vlan
        self.netmask = netmask
        self.poe = poe
        self.ports = ports
        self.port_based_ip_list = port_based_ip_list
        self.vlan = vlan
        self.redundancy_ports = redundancy_ports
        self.redundant_protocol = redundant_protocol
        self.ring_master = ring_master
        self.switch_ip = switch_ip
        self.switch_name = switch_name
        self.tagged_ports = tagged_ports
        self.untagged_ports = untagged_ports

    def convert_ini_file_to_list(self):
        """
        This method opens a init file then returns them in to a list.

        :return: list
        """
        moxa_ini_file = open(self.ini_file, "r")
        moxa_ini_list = moxa_ini_file.readlines()
        moxa_ini_file.close()

        return moxa_ini_list

    def generate_ini_file(self):
        """
        This method generates a moxa config file by replacing the default
        values by the provided dataframe for the project.

        :return: file
        """
        def_ip_address = "192.168.127.253"
        def_netmask = "255.255.255.0"
        management_vlan = str(*self.management_vlan)

        template_file = self.convert_ini_file_to_list()
        counter = 0
        # Set the switch values.
        self.replace_line("SwitchName\t\t",
                          "\n", self.switch_name, template_file)
        self.replace_line("IPAddress\t\t",
                          def_ip_address, str(*self.switch_ip), template_file)
        self.replace_line("Netmask\t\t\t",
                          def_netmask, self.netmask, template_file)
        self.replace_line("SysVID\t\t\t",
                          "1", management_vlan[:-1], template_file)

        # Set Turbo Ring values.
        self.replace_line("RedundantProtol\t\t", "0",
                          self.redundant_protocol, template_file)
        self.replace_line("Ring1_Master\t\t", "0",
                          self.ring_master, template_file)
        self.replace_line("CouplingMode\t\t", "0",
                          self.coupling_mode, template_file)
        if self.coupling_port == "14":
            self.replace_line("Coupling_1st\t\t", "14",
                              self.coupling_port, template_file)
        else:
            self.replace_line("Coupling_1st\t\t", "14",
                              str(*self.coupling_port), template_file)

        # Set port specific values.
        for port in self.ports:
            def_current_port = f"DeviceIP_{port}\t"
            current_port = def_current_port + self.port_based_ip_list[counter]
            self.replace_line(def_current_port, def_current_port,
                              current_port, template_file)

            def_current_netmask = f"Netmask_{port}\t"
            current_netmask = def_current_netmask + self.netmask
            self.replace_line(def_current_netmask, def_current_netmask,
                              current_netmask, template_file)

            def_current_port_name = f"Port_{port}_NAME\t\t"
            current_port_name = def_current_port_name + \
                str(self.functions[counter])
            self.replace_line(def_current_port_name, def_current_port_name,
                              current_port_name, template_file)

            # Set VLAN values based on type.
            def_current_vlan_id = f"VLANPvid_{port}\t\t1"
            untagged = def_current_vlan_id[:-1] + self.untagged_ports[counter]
            self.replace_line(def_current_vlan_id, def_current_vlan_id,
                              untagged, template_file)

            def_current_tagged = f"FixVid_{port}\t\t"
            tagged = def_current_tagged + self.tagged_ports[counter]
            self.replace_line(def_current_tagged, def_current_tagged,
                              tagged, template_file)

            # Set PoE values.
            def_power_allocation = f"POE_PORT{port}_POWERALLOCATION\t\t0"
            power_allocation = \
                def_power_allocation[:-1] + str(self.poe[counter])

            def_power_output_mode = f"POE_PORT{port}_OUTPUTMODE\t\t0"
            power_output_mode = f"POE_PORT{port}_OUTPUTMODE\t\t2"

            def_port_check = f"POE_PORT{port}_PDCHECK\t\t0"
            port_check = f"POE_PORT{port}_PDCHECK\t\t1"

            def_pd_ipaddr = f"POE_PORT{port}_PDIPADDR\t\t"
            pd_ipaddr = def_pd_ipaddr + self.port_based_ip_list[counter]

            if not numpy.isnan(self.poe[counter]):
                self.replace_line(def_power_allocation, def_power_allocation,
                                  power_allocation[:-2], template_file)
                # set power mode to force if power allocation value isn't 0.
                if power_allocation[-2] != 0:
                    self.replace_line(def_power_output_mode,
                                      def_power_output_mode,
                                      power_output_mode,
                                      template_file)
                    self.replace_line(def_port_check, def_port_check,
                                      port_check,
                                      template_file)
                    self.replace_line(def_pd_ipaddr, def_pd_ipaddr,
                                      pd_ipaddr,
                                      template_file)

            counter += 1

        return template_file

    @staticmethod
    def get_line_number_in_list(phrase, array_name):
        """This function returns a line number if
           the corresponding string is found

        Args:
            phrase (string): Text to be found in the row
            array_name (list): List of rows from the csv file

        Returns:
            integer: returns the line number where the phrase is found
                     otherwise returns a 0
        """
        line_num = 0
        found = 0
        for line in array_name:
            line_num += 1

            if phrase in line:
                return line_num

        if found == 0:  # not found
            return 0

    def replace_line(self, search_txt, replace_txt, new_txt, lines_array):
        """This function gets the line to be replaced, and replaces the content
           With a combination of an IP address and Subnet mask.

        Args:
            search_txt (file): configuration file
            replace_txt (string): text to be replaced
            new_txt (string): text that replaces the original
            lines_array (list): list of the configuration

        Returns:
            list: returns list with the replaced line.
        """
        line_to_replace = self.get_line_number_in_list(search_txt, lines_array)

        if line_to_replace != 0:
            line2 = str.replace(
                lines_array[line_to_replace - 1], replace_txt, new_txt)

            lines_array[line_to_replace - 1] = line2

        return lines_array

    @staticmethod
    def write_ini_file(new_ini_file, ini_list):
        moxa_file = open(new_ini_file, "w")
        moxa_file.writelines(ini_list)

        return moxa_file
