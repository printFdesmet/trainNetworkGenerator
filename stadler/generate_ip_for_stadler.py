"""
TODO: Extract the untagged vlan port if there is a list. if no untagged,
      keep the original way to chose the subnet. see from line 54.
      HOWTO: Loop over the list, selecting the element containing the 'U'
      character then choose the first char of that element.
IMPORTANT: For the second octet only 7 bits are being used, from which the
           the first 3 are for the vehicle type and the following 4 for
           the VLAN ID.
VLAN ID     |Vehicle type
X.64.32.16.8|.4.2.1
------------------
8.7 .6 .5 .4|.3.2.1

VLANs in use: 2, 7, 9, 10, 12
Vehicle types: 1, 6, 7
"""
counter = 0


class GenerateIPForStadler:
    """
    A Class to generate the second and third octet of an IP using
    a combination of the VLAN ID and vehicle type for the second and the car
    number for the third one.
    """

    def __init__(self, consist_number, ip, vehicle_name, vlan_id):
        self.consist_number = consist_number
        self.ip = ip
        self.vehicle_name = vehicle_name
        self.vlan_id = vlan_id

    def generate_second_octet(self):
        """
        This method takes the VLAN ID and the vehicle type to generate the
        correct byte.

        :returns: string
        """
        global counter

        vlan_to_ip = {
            "2": "16",
            "7": "56",
            "9": "72",
            "10": "80",
            "12": "96",
        }

        vehicle_type_to_ip = {
            "DMU4": "1",  # Vehicle name: lot 1b
            "BMU-B3": "6",  # Vehicle name: lot 4a
            "BMU-B4": "7",  # Vehicle name: lot 4b
        }

        vehicle_ip = vehicle_type_to_ip.get(self.vehicle_name)
        if len(self.vlan_id[counter]) > 3:
            vlan_ip = vlan_to_ip.get(self.vlan_id[counter][0])
        else:
            vlan_ip = vlan_to_ip.get(self.vlan_id[counter][:-1])

        second_octet = int(vehicle_ip) + int(vlan_ip)

        counter += 1

        return str(second_octet)

    def generate_third_octet(self):
        """
        This method takes the car number and creates the third octet.

        :returns: string
        """
        return str(self.consist_number + 1)

    def generate_unique_ip(self):
        """
        This method takes the original IP template (without the second and
        third octet) and fills those empty values with the generated octets.

        :returns: list
        """
        global counter
        counter = 0
        ip_list = []

        for an_ip in self.ip:
            if type(an_ip) == float:
                ip_list.append("")
                counter += 1
                continue
            if not an_ip:
                ip_list.append("")
                counter += 1
            else:
                second_octet = self.generate_second_octet()
                third_octet = self.generate_third_octet()

                altered_ip_with_octets = \
                    an_ip.replace("x", second_octet).replace("y", third_octet)
                ip_list.append(altered_ip_with_octets)

        return ip_list
