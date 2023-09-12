from fish import Fish, ListFish
from cwsd import CWSD

from datetime import date


number_pools: int = 4
cwsd: CWSD = CWSD(
    number_pools=number_pools,
    pool_area=6.0,
    max_planting_density=40.0,
    commercial_fish_mass=450.0,
    min_package=100,
    start_date=date.today()
)

numbers: list[int] = [800 for _ in range(number_pools - 1)]
numbers.append(600)

masses: list[float] = [50, 100, 150, 200]

lists_fishes: list[ListFish] = list()

cwsd.print()
for index in range(number_pools):
    fishes: ListFish = ListFish([Fish(masses[index]) for _ in range(numbers[index])])
    cwsd.add_fish(fishes)
cwsd.print()

days: int = 1000

for _ in range(days):
    result = cwsd.daily_growth()
    if result is None:
        break

cwsd.print()
