from stadler.flirt import Flirt
from stadler.stadler import Stadler


def main():
    # Change here the desired amount of consists and the design.
    stadler_b3 = Stadler(total_amount_consists="7", vehicle_name="BMU-B3")
    stadler_b4 = Stadler(total_amount_consists="17", vehicle_name="BMU-B4")
    stadler_d4 = Stadler(total_amount_consists="11", vehicle_name="DMU4")

    train_list = [stadler_b3, stadler_b4, stadler_d4]

    switch_list_b3 = stadler_b3.chosen_train()
    switch_list_b4 = stadler_b4.chosen_train()
    switch_list_d4 = stadler_d4.chosen_train()

    switch_lists = [switch_list_b3, switch_list_b4, switch_list_d4]

    for train in train_list:
        for consist in range(int(train.total_amount_consists)):
            for switch_list in switch_lists:
                for switch in switch_list:
                    if switch[0] == "A":
                        flirt = Flirt(config="data/stadler/switches_a.csv",
                                      total_amount_consists=consist,
                                      switch=switch,
                                      vehicle_name=train.vehicle_name)
                        flirt.generate_flirt_switch_config()
                    elif switch[0] == "B":
                        flirt = Flirt(config="data/stadler/switches_b.csv",
                                      total_amount_consists=consist,
                                      switch=switch,
                                      vehicle_name=train.vehicle_name)
                        flirt.generate_flirt_switch_config()
                    elif switch[0] == "C":
                        flirt = Flirt(config="data/stadler/switches_c.csv",
                                      total_amount_consists=consist,
                                      switch=switch,
                                      vehicle_name=train.vehicle_name)
                        flirt.generate_flirt_switch_config()
                    elif switch[0] == "D":
                        flirt = Flirt(config="data/stadler/switches_d.csv",
                                      total_amount_consists=consist,
                                      switch=switch,
                                      vehicle_name=train.vehicle_name)
                        flirt.generate_flirt_switch_config()
                    if switch[0] == "P":
                        flirt = Flirt(config="data/stadler/switches_p.csv",
                                      total_amount_consists=consist,
                                      switch=switch,
                                      vehicle_name=train.vehicle_name)
                        flirt.generate_flirt_switch_config()
                    else:
                        continue


if __name__ == '__main__':
    main()
