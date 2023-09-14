from fish import Fish, ListFish, create_list_fish
from cwsd import CWSD
from optimization import Optimization

from datetime import date


optimization: Optimization = Optimization(
    number_pools=4,
    pool_area=6.0,
    max_planting_density=40.0,
    commercial_fish_mass=450.0,
    min_package=1000
)

print(optimization.calculate_number_fish_for_max_density(
    days=83,
    start_mass=50,
    start_number=10,
    step=10,
    end_number=5000
))
