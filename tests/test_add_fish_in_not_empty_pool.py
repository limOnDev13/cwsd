from cwsd import CWSD
from fish import create_list_fish, ListFish
from datetime import date


number_and_mass: list[list[int | float]] = [[590, 200], [600, 150], [760, 100], [1200, 50]]

cwsd: CWSD = CWSD(
    number_pools=len(number_and_mass),
    pool_area=6.0,
    max_planting_density=40.0,
    commercial_fish_mass=450.0,
    min_package=1000,
    start_date=date.today()
)

cwsd.print()
for i in range(len(number_and_mass)):
    cwsd.add_fish(create_list_fish(number_and_mass[i][0], number_and_mass[i][1]))
cwsd.print()

new_fish: ListFish = create_list_fish(100, 210)

cwsd.add_fish_in_not_empty_pool(210, new_fish, print_info=True)
cwsd.print()
