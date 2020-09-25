from moxa import Moxa
from stadler.flirt import Flirt
from stadler.stadler import Stadler

from pandas import DataFrame


def main():
    # Change here the desired amount of consists and the design.
    # stadler = Stadler(total_amount_consists="11", vehicle_name="DMU4")
    # switch_list = stadler.chosen_train()
    #
    # for consist in range(int(stadler.total_amount_consists)):
    #     for switch in switch_list:
    #         if switch[0] == "A":
    #             flirt = Flirt(config="data/stadler/switches_a.csv",
    #                           total_amount_consists=consist,
    #                           switch=switch,
    #                           vehicle_name=stadler.vehicle_name)
    #             flirt.generate_flirt_switch_config()
    #         elif switch[0] == "B":
    #             flirt = Flirt(config="data/stadler/switches_b.csv",
    #                           total_amount_consists=consist,
    #                           switch=switch,
    #                           vehicle_name=stadler.vehicle_name)
    #             flirt.generate_flirt_switch_config()
    #         elif switch[0] == "C":
    #             flirt = Flirt(config="data/stadler/switches_c.csv",
    #                           total_amount_consists=consist,
    #                           switch=switch,
    #                           vehicle_name=stadler.vehicle_name)
    #             flirt.generate_flirt_switch_config()
    #         elif switch[0] == "D":
    #             flirt = Flirt(config="data/stadler/switches_d.csv",
    #                           total_amount_consists=consist,
    #                           switch=switch,
    #                           vehicle_name=stadler.vehicle_name)
    #             flirt.generate_flirt_switch_config()
    #         elif switch[0] == "P":
    #             flirt = Flirt(config="data/stadler/switches_p.csv",
    #                           total_amount_consists=consist,
    #                           switch=switch,
    #                           vehicle_name=stadler.vehicle_name)
    #             flirt.generate_flirt_switch_config()
    #         else:
    #             continue
    # moxa = Moxa("data/moxa/moxa_4500a_16.ini")
    # moxa_list = moxa.convert_ini_file_to_list()
    # print(moxa.generate_ini_file())
    # new_config_list = []
    # for line in moxa_list:
    #     if f"Port_{1}_EN" in line:
    #         replaced_line = line.replace('1\n', '0\n')
    #         new_config_list.append(replaced_line)
    #         print(new_config_list)
    pass


if __name__ == '__main__':
    main()
