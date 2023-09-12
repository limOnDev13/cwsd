from fish import Fish


class Pool:
    """
    Класс отвечающий за работу бассейна
    """
    def __init__(self, area: float, mass_index: int):
        self._area: float = area
        self.mass_index: int = mass_index

        self.biomass: float = 0.0
        self.number_fish: int = 0

        self.average_mass: float = 0.0
        self.planting_density: float = 0.0

        self.fishes: list[Fish] = list()

    def _update_info(self):
        """
        Метод для обновления информации о рыбе в бассейне.
        :return: Ничего
        """
        if len(self.fishes) == 0:
            self.biomass = 0.0
            self.number_fish = 0
            self.average_mass = 0.0
            self.planting_density = 0.0
        else:
            self.average_mass = self.biomass / self.number_fish * 1000  # в граммах
            self.planting_density = self.biomass / self._area

    def add_new_fishes(self, new_fishes: list[Fish]):
        """
        Метод для добавления новых рыбок в бассейн.
        :param new_fishes: Список новых рыбок.
        :return: Ничего
        """
        for fish in new_fishes:
            self.fishes.append(fish)
            self.biomass += fish.mass / 1000
            self.number_fish += 1

        # Отсортируем рыбу по массе
        self.fishes.sort(key=lambda item: item.mass)

        # Обновим информацию о рыбе в бассейне
        self._update_info()

    def remove_fish(self, number_fish: int, biggest_fish: bool = True) -> list[Fish]:
        """
        Метод для удаления рыбы из бассейна.
        :param number_fish: Количество удаляемых рыб.
        :param biggest_fish: Если True, то удаляет самые большие рыбы,
         иначе - самые маленькие.
        :return: Список удаленных рыб
        """
        if number_fish > self.number_fish:
            print('Попытка удалить рыбы больше чем есть в бассейне!')
        else:
            removed_fish: list[Fish] = list()

            for _ in range(number_fish):
                fish: Fish
                if biggest_fish:
                    fish = self.fishes.pop(-1)
                else:
                    fish = self.fishes.pop(0)

                self.biomass -= fish.mass / 1000
                self.number_fish -= 1
                removed_fish.append(fish)

            # Обновим информацию о рыбе в бассейне
            self._update_info()

            return removed_fish

    def daily_growth(self) -> dict[str, float]:
        """
        Метод для расчета ежедневного выращивания всей рыбы в этом бассейне.
        :return: Возвращает словарь с информацией об суточном приросте биомассы
         и затраченном корме на бассейн.
        Словарь имеет вид:
        {'biomass_increase': ..., 'spent_feed': ...}
        """
        biomass_increase: float = 0.0
        spent_feed: float = 0.0

        for fish in self.fishes:
            daily_result: dict[str, float] = fish.daily_growth()
            biomass_increase += daily_result['mass_increase'] / 1000
            spent_feed += daily_result['required_feed'] / 1000

        # Обновим информацию о рыбе в бассейне
        self.biomass += biomass_increase
        self._update_info()

        return {'biomass_increase': biomass_increase, 'spent_feed': spent_feed}

    def print(self):
        """
        Метод для печати информации о рыбе в бассейне.
        :return: Ничего
        """
        print(f'Биомасса в бассейне: {self.biomass} кг.\n'
              f'Количество рыбы в бассейне: {self.number_fish} шт.\n'
              f'Средняя масса рыбы: {self.average_mass} г.\n'
              f'Плотность посадки: {self.planting_density} кг/м^2.')


"""
number_fish: int = 100
start_mass: float = 100.0
feed_ratio: float = 1.5

fishes: list[Fish] = list()
for _ in range(number_fish):
    fishes.append(Fish(start_mass, feed_ratio))

pool: Pool = Pool(6.0)

pool.print()
pool.add_new_fishes(fishes)
pool.print()
print()

days: int = 100
increase_biomass: float = 0.0
spent_feed: float = 0.0

for _ in range(days):
    result: dict[str, float] = pool.daily_growth()
    increase_biomass += result['biomass_increase']
    spent_feed += result['spent_feed']

pool.print()
print(f'increase_biomass = {increase_biomass} kg\n'
      f'spent_feed = {spent_feed} kg')
print()

removed_fish1: list[Fish] = pool.remove_fish(10)
pool.print()
print()

removed_fish2: list[Fish] = pool.remove_fish(10, biggest_fish=False)
pool.print()
print()
"""
