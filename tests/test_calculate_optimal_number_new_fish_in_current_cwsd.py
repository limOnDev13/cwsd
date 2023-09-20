from optimization import Optimization

from cwsd import CWSD
from fish import ListFish
from datetime import date
from standart_objects import get_cwsd, get_optimization, numbers_and_mass


cwsd: CWSD = get_cwsd()
optimization: Optimization = get_optimization()

first_days: int = 80

cwsd.print()
for _ in range(first_days):
    cwsd.daily_growth(False)
cwsd.print()
cwsd.daily_growth(False)
cwsd.print()
print()

optimization.calculate_optimal_number_new_fish_in_current_cwsd(
    cwsd=cwsd,
    average_mass=180.0,
    start_number=100,
    step=10,
    end_number=5000
)
