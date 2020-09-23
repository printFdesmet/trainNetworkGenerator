from pandas import DataFrame


class Moxa:
    """
    This class handles the importing, manipulation and recreation of the moxa
    init file.
    """

    def __init__(self, ini_file):
        self.ini_file = ini_file

    def convert_ini_file_to_list(self):
        """
        This method opens a init file then returns them in to a dataframe.

        :return: dataframe
        """
        moxa_ini_file = open(self.ini_file, "r")
        moxa_ini_list = moxa_ini_file.readlines()
        moxa_str = str(moxa_ini_list)
        moxa_list = moxa_str.split(r"\n")

        return moxa_list

    def generate_ini_file(self):
        pass
