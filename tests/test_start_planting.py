from fish import Fish, ListFish, create_list_fish
from cwsd import CWSD
from optimization import Optimization

from datetime import date


number_pools: int = 4
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
