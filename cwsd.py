from datetime import date
from fish import Fish
from pool import Pool


class CWSD:
    def __init__(self, number_pools: int, pool_area: float,
                 max_planting_density: float, commercial_fish_mass: float,
                 min_package: int, start_date: date):
        """
        Метод __init__.
        :param number_pools: Количество бассейнов.
        :param pool_area: Площадь бассейна в м^2.
        :param max_planting_density: Максимальная плотность посадки рыбы в кг/м^2.
        :param commercial_fish_mass: Масса товарной рыбы в г.
        :param min_package: Минимальный размер пакета на продажу.
        """
        self.number_pools: int = number_pools
        self.start_date: date = start_date

        self.commercial_fish_mass: float = commercial_fish_mass
        self.min_package: int = min_package

        self.max_planting_density: float = max_planting_density

        self.pools: list[Pool] = list()
        for number in range(number_pools):
            pool: Pool = Pool(pool_area, number)
            self.pools.append(pool)

        self.biomass: float = 0.0
        self.days: int = 0
        self.spent_feed: float = 0.0
        self.sold_biomass: float = 0.0

    def _update_mass_indexes(self):
        """
        Метод для обновления массовых индексов бассейнов. Они выставляются по
         возрастанию средней массы рыбы.
        :return: Ничего
        """
        average_masses: list[float] = [pool.average_mass for pool in self.pools]
        average_masses.sort()

        # Присвоим бассейнам в зависимости от средней массы массовый индекс
        for pool in self.pools:
            for number in range(len(average_masses)):
                if pool.average_mass == average_masses[number]:
                    pool.mass_index = number
                    break

    def add_fish(self, fishes: list[Fish]):
        """
        Метод для добавления новой рыбы в какой-нибудь пустой бассейн.
        :param fishes: Список новой рыбы.
        :return: Ничего.
        """
        empty_pool: Pool | None = None

        for pool in self.pools:
            if pool.number_fish == 0:
                empty_pool = pool
                break

        if empty_pool is not None:
            empty_pool.add_new_fishes(fishes)
            self.biomass += empty_pool.biomass
            self._update_mass_indexes()
        else:
            print('Пока нет ни одного пустого бассейна.')

    def sell_fish(self) -> list[Fish] | None:
        """
        Если есть достаточно много товарной рыбы, этот метод ее продает.
        :return: Список проданной рыбы.
        """
        # Найдем товарный бассейн
        commercial_pool: Pool = self.pools[0]

        for pool in self.pools:
            if pool.mass_index == self.number_pools - 1:
                commercial_pool = pool
                break

        # Посчитаем количество товарной рыбы
        number_commercial_fish: int = 0

        for fish in commercial_pool.fishes:
            if fish.mass >= self.commercial_fish_mass:
                number_commercial_fish += 1

        # Если количество товарной рыбы превысил минимальный размер пакета или
        # выросла вся рыба
        if (number_commercial_fish >= self.min_package) or\
                (number_commercial_fish == commercial_pool.number_fish):
            # Удалим рыбу из бассейна
            sold_fish: list[Fish] = commercial_pool.remove_fish(number_commercial_fish)

            # Обновим информацию о проданной рыбе
            for fish in sold_fish:
                self.sold_biomass += fish.mass / 1000

            # вернем список проданной рыбы
            return sold_fish
        # Если выросло недостаточно, то вернем None
        else:
            return None