from fish import Fish, ListFish, create_list_fish
from cwsd import CWSD
from optimization import Optimization

from datetime import date


number_pools: int = 4
optimization: Optimization = Optimization(
    number_pools=number_pools,
    pool_area=6.0,
    max_planting_density=40.0,
    commercial_fish_mass=450.0,
    min_package=1000
)

start_mass: float = 200.0

number_fish: int = 1000
attempts: int = 100

min_days: int = 100000
max_days: int = 0
average_days: int = 0

for _ in range(attempts):
    days: int = optimization.calculate_growing_time(start_mass, number_fish)
    if min_days > days:
        min_days = days
    if max_days < days:
        max_days = days
    average_days += days
    print(days)
print()

average_days /= attempts
print(f'Минимум дней: {min_days}\n'
      f'Максимум дней: {max_days}\n'
      f'Среднее количество дней: {average_days}')

print(optimization.calculate_number_fish_for_max_density(
    days=83,
    start_mass=50,
    start_number=10,
    step=10,
    end_number=5000
))

cwsd: CWSD = CWSD(
    number_pools=number_pools,
    pool_area=6.0,
    max_planting_density=40.0,
    commercial_fish_mass=450.0,
    min_package=1000,
    start_date=date.today()
)

cwsd.add_fish(create_list_fish(470, 200))
cwsd.add_fish(create_list_fish(580, 150))
cwsd.add_fish(create_list_fish(760, 100))
cwsd.add_fish(create_list_fish(1300, 50))

cwsd.print()

for _ in range(1000):
    result = cwsd.daily_growth()
    if result is None:
        break

cwsd.print()
