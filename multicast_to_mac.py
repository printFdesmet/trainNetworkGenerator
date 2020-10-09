"""
        This class converts given IP-addresses to their corresponding
        MAC-addresses.
"""


class MulticastIPToMAC:
    def __init__(self, multicast_list):
        self.multicast = multicast_list

    def verify_ip(self, multicast_ip):
        """

        This method takes a multicast IP(string) as an argument

        and returns True if IP address is correct

        """

        if len(multicast_ip) < 9 or len(multicast_ip) > 15:
            print("Multicast IP address length is incorrect !")

            return False

        octets = multicast_ip.split('.')

        if len(octets) < 4:
            print("Incorrect number of octets in multicast IP address !")

            return False

        for idx in range(0, 4):

            if not (self.verify_octet(octets[idx])):
                print("One of the octets is incorrect !")

                return False

        # Check if first octet is from multicast range

        if int(octets[0]) < 224 or int(octets[0]) > 239:
            print(f"First octet isn’t from multicast range !"
                  f"Should be 224 … 239 !")

            return False

        return True

    @staticmethod
    def verify_octet(octet):

        """

        This method returns True if string parameter ‘octet’
        is a number in the range 0…255

        """

        if octet.isdigit:

            octet_num = int(octet)

            if 0 <= octet_num <= 255:
                return True

        return False

    def ip2mac(self):

        """

        Method ip2mac takes multicast IP address as an argument
        and returns multicast MAC address

        """

        if not (self.verify_ip(self.multicast)):
            print(f"Parameter provided is not a valid multicast IP !"
                  f"Should be 224.0.0.1 … 239.255.255.255")

        multicast_to_mac = '01-00-5e-'
        octets = self.multicast.split('.')
        second_oct = int(octets[1]) & 127
        third_oct = int(octets[2])
        fourth_oct = int(octets[3])

        multicast_to_mac = (f"{multicast_to_mac}"
                            f"{format(second_oct, '02x')}-"
                            f"{format(third_oct, '02x')}-"
                            f"{format(fourth_oct, '02x')}")

        return multicast_to_mac
