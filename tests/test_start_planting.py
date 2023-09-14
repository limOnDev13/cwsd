from fish import Fish, ListFish, create_list_fish
from cwsd import CWSD
from optimization import Optimization

from datetime import date


number_and_mass: list[list[int]] = [[590, 200], [600, 150], [760, 100], [1200, 50]]
attempts: int = 100
success_attempts: int = 0
failed_attempts: int = 0

for attempt in range(attempts):
    print(f'попытка номер {attempt}')

    cwsd: CWSD = CWSD(
        number_pools=len(number_and_mass),
        pool_area=6.0,
        max_planting_density=40.0,
        commercial_fish_mass=450.0,
        min_package=1000,
        start_date=date.today()
    )

    for i in range(len(number_and_mass)):
        cwsd.add_fish(create_list_fish(number_and_mass[i][0], number_and_mass[i][1]))

    it_works: bool = True
    for _ in range(200):
        result = cwsd.daily_growth(print_info=False)
        if result is None:
            it_works = False
            break

    if it_works:
        print(f'Все работает!  {number_and_mass}')
        success_attempts += 1
    else:
        failed_attempts += 1

print(f'Из {attempts} попыток {success_attempts} удачных.')
