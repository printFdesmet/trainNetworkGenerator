"""
TODO: Change the dataframe input from CSV to EXCEL, this prevents the step
      of manual converting the original document. (and worrying about formulas)
TODO: Change the Header values as those have changed with the latest version
      of the document.
TODO: Change the default Subnet Mask, this has been changed with the latest version
      of the document. has to be /13
TODO: Add the Multicast Column to the program and process it in the INI file.
TODO: Change the Function column values accessed within the program to the
      changed values.
TODO: Change the IP's of the devices in VLAN 12. has to be 172.x.x.x
"""

from stadler.flirt import Flirt
from stadler.stadler import Stadler


def main():
    # Add here your desired vehicles.
    # stadler_b3 = Stadler(total_amount_consists="7", vehicle_name="BMU-B3")
    # stadler_b4 = Stadler(total_amount_consists="17", vehicle_name="BMU-B4")
    # stadler_d4 = Stadler(total_amount_consists="11", vehicle_name="DMU4")
    #
    # train_list = [stadler_b3, stadler_b4, stadler_d4]
    #
    # # Returns list with all the switches in the chosen vehicle type.
    # switch_list_b3 = stadler_b3.chosen_train()
    # switch_list_b4 = stadler_b4.chosen_train()
    # switch_list_d4 = stadler_d4.chosen_train()
    #
    # switch_lists = [switch_list_b3, switch_list_b4, switch_list_d4]
    # # Goes over all the vehicle types, inside go over the amount of consists,
    # # then finally go over every switch inside that consist. Generating the
    # # .INI files.
    # # For the Flirt project.
    # for train in train_list:
    #     for consist in range(int(train.total_amount_consists)):
    #         for switch_list in switch_lists:
    #             for switch in switch_list:
    #                 if switch[0] == "A":
    #                     flirt = Flirt(config="data/stadler/switches_a.csv",
    #                                   total_amount_consists=consist,
    #                                   switch=switch,
    #                                   vehicle_name=train.vehicle_name)
    #                     flirt.generate_flirt_switch_config()
    #                 elif switch[0] == "B":
    #                     flirt = Flirt(config="data/stadler/switches_b.csv",
    #                                   total_amount_consists=consist,
    #                                   switch=switch,
    #                                   vehicle_name=train.vehicle_name)
    #                     flirt.generate_flirt_switch_config()
    #                 elif switch[0] == "C":
    #                     flirt = Flirt(config="data/stadler/switches_c.csv",
    #                                   total_amount_consists=consist,
    #                                   switch=switch,
    #                                   vehicle_name=train.vehicle_name)
    #                     flirt.generate_flirt_switch_config()
    #                 elif switch[0] == "D":
    #                     flirt = Flirt(config="data/stadler/switches_d.csv",
    #                                   total_amount_consists=consist,
    #                                   switch=switch,
    #                                   vehicle_name=train.vehicle_name)
    #                     flirt.generate_flirt_switch_config()
    #                 if switch[0] == "P":
    #                     flirt = Flirt(config="data/stadler/switches_p.csv",
    #                                   total_amount_consists=consist,
    #                                   switch=switch,
    #                                   vehicle_name=train.vehicle_name)
    #                     flirt.generate_flirt_switch_config()
    #                 else:
    #                     continue

    # For testing
    stadler_test = Stadler(total_amount_consists="1", vehicle_name="BMU-B3")
    test_list = stadler_test.chosen_train()
    for consist in range(int(stadler_test.total_amount_consists)):
        for test in test_list:
            if test[0] == "A":
                flirt = Flirt(config="data/stadler/switches_a.csv",
                              total_amount_consists=consist,
                              switch=test,
                              vehicle_name=stadler_test.vehicle_name)
                flirt.generate_flirt_switch_config()


if __name__ == '__main__':
    main()
