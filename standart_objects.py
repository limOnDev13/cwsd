from cwsd import CWSD
from fish import ListFish, create_list_fish
from optimization import Optimization
from datetime import date


numbers_and_mass: list[list[float | int]] = [[590, 200.0], [600, 150.0], [760, 100.0], [1200, 50.0]]


def get_cwsd() -> CWSD:
    """
    Метод для получения стандартного объекта CWSD
    :return: объект CWSD
    """
    cwsd: CWSD = CWSD(
        number_pools=len(numbers_and_mass),
        pool_area=6.0,
        max_planting_density=40.0,
        commercial_fish_mass=450.0,
        min_package=1000,
        start_date=date.today()
    )
    for i in range(len(numbers_and_mass)):
        list_fish: ListFish = create_list_fish(numbers_and_mass[i][0], numbers_and_mass[i][1])
        cwsd.add_fish(list_fish)

    return cwsd


def get_optimization() -> Optimization:
    """
    Метод для получения стандартного объекта Optimization
    :return: объект Optimization
    """
    return Optimization(
        number_pools=4,
        pool_area=6.0,
        max_planting_density=40.0,
        commercial_fish_mass=450.0,
        min_package=1000
        )
