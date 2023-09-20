from datetime import date
from fish import Fish, ListFish
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
        self.pool_area: float = pool_area
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

    def add_fish(self, fishes: ListFish) -> bool:
        """
        Метод для добавления новой рыбы в какой-нибудь пустой бассейн.
        :param fishes: Список новой рыбы.
        :return: True, если был пустой бассейн и в него добавилась новая рыба. Иначе - False.
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
            return True
        else:
            return False

    def add_fish_in_not_empty_pool(self, average_mass: float, list_fish: ListFish, print_info: bool = False):
        """
        Метод для добавления рыбы в НЕ пустой бассейн. Рыба будет добавляться в бассейн, в котором находится рыба
         с наиболее близкой средней массой к массе новой рыбы.
        :param average_mass: Средняя масса добавляемой рыбы.
        :param list_fish: Список новой рыбы.
        :param print_info: Показывает, нужно ли печатать в какой бассейн добавили рыбу.
        :return: Ничего.
        """
        # Найдем бассейн со средней массой рыбы наиболее близкой к средней массе новой рыбы
        min_delta_mass: float = abs(self.pools[0].average_mass - average_mass)
        chosen_pool: Pool = self.pools[0]

        for pool in self.pools:
            delta_mass: float = abs(pool.average_mass - average_mass)
            if delta_mass < min_delta_mass:
                min_delta_mass = delta_mass
                chosen_pool = pool

        # Если нужно, напечатаем в какой бассейн добавили рыбу
        if print_info:
            print(f'Рыбу добавили в бассейн с массовым индексом {chosen_pool.mass_index}')

        # Добавим в найденный бассейн новую рыбу
        chosen_pool.add_new_fishes(list_fish)
        # Обновим информацию о рыбе в бассейне
        self.biomass += list_fish.get_biomass()
        self._update_mass_indexes()

    def sell_fish(self) -> ListFish | None:
        """
        Если есть достаточно много товарной рыбы, этот метод ее продает.
        :return: Список проданной рыбы. Если таковой нет, то None.
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
            sold_fish: ListFish = commercial_pool.remove_fish(number_commercial_fish)

            # Обновим информацию о проданной рыбе
            self.sold_biomass += sold_fish.get_biomass()
            # Обновим массовые индексы в бассейнах
            self._update_mass_indexes()

            # вернем список проданной рыбы
            return sold_fish
        # Если выросло недостаточно, то вернем None
        else:
            return None

    def _find_pool_with_mass_index(self, mass_index: int) -> Pool | None:
        """
        Метод для поиска бассейна с указанным массовым индексом.
        :param mass_index: Массовый индекс искомого бассейна.
        :return: искомый бассейн.
        """
        for pool in self.pools:
            if pool.mass_index == mass_index:
                return pool
        # Если бассейна с таким массовым индексом нет, то вернем None
        return None

    @staticmethod
    def _pool_is_empty(pool: Pool) -> bool:
        """
        Метод, который определяет, является ли переданный бассейн пустым.
        :param pool: Бассейн, который нужно определить, пустой он или нет.
        :return: True, если бассейн пустой. Иначе - False.
        """
        if pool.number_fish == 0:
            return True
        else:
            return False

    def separate_fish(self, overflowed_pool: Pool, percent: float = 30.0, print_info: bool = True):
        """
        Метод для распределения рыбы из переполненного бассейна по соседним
         (по средней массе). Также рыба НЕ будет распределяться в пустые бассейны.
        :param overflowed_pool: Переполненный бассейн.
        :param percent: Процент удаляемой рыбы. Половина от этого процента придется
         на медленнорастущих, вторая половина - на быстрорастущих. Если бассейн
          оказался крайним (т.е. с самой большой или самой маленькой рыбой),
           то удалится только половина процента.
        :param print_info: Показывает, нужно ли печатать информацию о перемещении рыбы.
        :return: Ничего
        """
        index_overflowed_pool: int = overflowed_pool.mass_index
        previous_pool: Pool | None = self._find_pool_with_mass_index(
            index_overflowed_pool - 1)
        next_pool: Pool | None = self._find_pool_with_mass_index(
            index_overflowed_pool + 1)

        # распределим рыбу
        number_fish_to_be_removed: int = int(
            overflowed_pool.number_fish * percent / 100 / 2)

        if (previous_pool is not None) and (self._pool_is_empty(previous_pool)):
            slow_growing_fish: ListFish = overflowed_pool.remove_fish(
                number_fish_to_be_removed, biggest_fish=False)
            if print_info:
                print(f'Переместим {number_fish_to_be_removed} медленно растущих рыб из'
                      f' {index_overflowed_pool} бассейна в {previous_pool.mass_index}.')
            previous_pool.add_new_fishes(slow_growing_fish)
        if (next_pool is not None) and (self._pool_is_empty(next_pool)):
            fast_growing_fish: ListFish = overflowed_pool.remove_fish(
                number_fish_to_be_removed)
            if print_info:
                print(f'Переместим {number_fish_to_be_removed} быстро растущих рыб из'
                      f' {index_overflowed_pool} бассейна в {next_pool.mass_index}.')
            next_pool.add_new_fishes(fast_growing_fish)

        # Обновим информацию о массовых индексах
        self._update_mass_indexes()

    def daily_growth(self, print_info: bool = True) -> dict[str, float] | None:
        """
        Метод для проведения ежедневного выращивания.
        :param print_info: Показывает, нужно ли печатать информацию о перемещении рыбы.
        :return: Словарь с информацией об изменении биомассы,
         затраченном корме и проданной биомассе. Словарь имеет вид
          {'biomass_increase': biomass_increase, 'spent_feed': spent_feed,
           'sold_biomass': sold_biomass}
        """
        biomass_increase: float = 0.0
        spent_feed: float = 0.0
        for pool in self.pools:
            pool_result: dict[str, float] = pool.daily_growth()
            biomass_increase += pool_result['biomass_increase']
            spent_feed += pool_result['spent_feed']

        # Если есть, продадим товарную рыбу
        sold_fish: ListFish | None = self.sell_fish()
        sold_biomass: float = 0.0
        if sold_fish is not None:
            sold_biomass = sold_fish.get_biomass()

        # Обновим информацию о рыбе в УЗВ
        self.biomass += biomass_increase - sold_biomass
        self.days += 1
        self.spent_feed += spent_feed

        # Соберем словарь в качестве результата
        result: dict[str, float] = {'biomass_increase': biomass_increase,
                                    'spent_feed': spent_feed,
                                    'sold_biomass': sold_biomass}

        # Если переполнено все УЗВ, то сообщим об ошибке и завершим работу
        if self.biomass / (self.pool_area * self.number_pools) >=\
                self.max_planting_density:
            print('Переполнение!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            return None

        # Если есть переполненные бассейны - распределим рыбу
        for pool in self.pools:
            if pool.planting_density >= self.max_planting_density:
                self.separate_fish(pool, print_info=print_info)

        # Вернем ежедневный результат
        return result

    def print(self):
        print(f'Прошло {self.days} дней.\n'
              f'В УЗВ находится {self.biomass} кг биомассы.\n'
              f'За это время продано {self.sold_biomass} кг биомассы.\n'
              f'При этом было потрачено {self.spent_feed} кг корма.')
        for pool in self.pools:
            pool.print()
            print()
