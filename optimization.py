from cwsd import CWSD
from pool import Pool
from fish import Fish, ListFish
from datetime import date


class Optimization:
    def __init__(self, number_pools: int, pool_area: float, max_planting_density: float, commercial_fish_mass: float,
                 min_package: int):
        self.number_pools: int = number_pools
        self.pool_area: float = pool_area
        self.max_planting_density: float = max_planting_density
        self.commercial_fish_mass: float = commercial_fish_mass
        self.min_package: int = min_package
        self.start_date: date = date.today()

    def create_cwsd(self) -> CWSD:
        return CWSD(
            number_pools=self.number_pools,
            pool_area=self.pool_area,
            max_planting_density=self.max_planting_density,
            commercial_fish_mass=self.commercial_fish_mass,
            min_package=self.min_package,
            start_date=self.start_date
        )

    @staticmethod
    def create_list_fish(number_fish: int, mass: float) -> ListFish:
        fishes: list[Fish] = [Fish(mass) for _ in range(number_fish)]
        return ListFish(fishes)

    def calculate_growing_time(self, mass: float, number_fish: int) -> int:
        """
        Метод для расчета длительности выращивания с такой средней массой.
        :param mass: Средняя масса рыбки.
        :param number_fish: Количество рыбок, по которому нужно усреднять.
        :return: Количество дней
        """
        list_fish: ListFish = self.create_list_fish(mass=mass, number_fish=number_fish)
        days: int = 0

        amount_growth_fish: int = 0

        while amount_growth_fish < self.min_package:
            amount_growth_fish = 0
            for fish in list_fish.list_fish:
                fish.daily_growth()
                if fish.mass > self.commercial_fish_mass:
                    amount_growth_fish += 1
            days += 1

        return days

    def calculate_number_fish_for_max_density(self, days: int, start_mass: float, start_number: int, step: int,
                                              end_number: int) -> int:
        """
        Метод для расчета количества рыбы в бассейне, которое будет соответствовать максимальной плотности
         прошествии определенного количества дней.
        :param days: Количество дней, по истечению которых будет достигнута максимальная плотность.
        :param start_mass: Начальная масса рыбок.
        :param start_number: Начальное количество рыбы для вариации.
        :param step: Шаг для вариации.
        :param end_number: Конечное количество рыбы для вариации.
        :return: Оптимальное количество дней
        """
        number_fish: int = start_number

        while number_fish <= end_number:
            pool: Pool = Pool(self.pool_area, 0)
            list_fish: ListFish = self.create_list_fish(number_fish, start_mass)
            pool.add_new_fishes(list_fish)

            for _ in range(days):
                pool.daily_growth()

            if pool.planting_density >= self.max_planting_density:
                break
            else:
                number_fish += step

        return number_fish
