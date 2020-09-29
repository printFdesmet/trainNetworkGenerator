class Moxa:
    """
    This class handles the importing, manipulation and recreation of the moxa
    init file.
    """

    def __init__(self, coupling_port, functions, ini_file, netmask, switch_ip,
                 poe, ports, port_based_ip_list, vlan, switch_name):
        self.coupling_port = coupling_port
        self.functions = functions
        self.ini_file = ini_file
        self.netmask = netmask
        self.poe = poe
        self.ports = ports
        self.port_based_ip_list = port_based_ip_list
        self.vlan = vlan
        self.switch_ip = switch_ip
        self.switch_name = switch_name

    def convert_ini_file_to_list(self):
        """
        This method opens a init file then returns them in to a list.

        :return: list
        """
        moxa_ini_file = open(self.ini_file, "r")
        moxa_ini_list = moxa_ini_file.readlines()

        return moxa_ini_list

    def generate_ini_file(self):
        """
        This method generates a moxa config file by replacing the default
        values by the provided dataframe for the project.

        :return: file
        """
        print(f"Coupling port:\n{self.coupling_port}\n")
        print(f"Port names:\n{self.functions}\n")
        print(f"Netmask:\n{self.netmask}\n")
        print(f"PoE list:\n{self.poe}\n")
        print(f"Port list:\n{self.ports[:-1]}\n")
        print(f"IP list:\n{self.port_based_ip_list[:-1]}\n")
        print(f"Vlan list:\n{self.vlan}\n")
        print(f"Switch IP:\n{self.switch_ip}\n")
        print(f"Switch name:\n{self.switch_name}\n")

    @staticmethod
    def get_line_number_in_list(phrase, array_name):
        """This function returns a line number if the corresponding string is found

        Args:
            phrase (string): Text to be found in the row
            array_name (list): List of rows from the csv file

        Returns:
            integer: returns the line number where the phrase is found otherwise
                     returns a 0
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
