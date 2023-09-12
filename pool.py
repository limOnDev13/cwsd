from fish import Fish, ListFish


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

    def add_new_fishes(self, new_fish: ListFish):
        """
        Метод для добавления новых рыбок в бассейн.
        :param new_fish: Список новых рыбок.
        :return: Ничего.
        """
        for fish in new_fish.list_fish:
            self.fishes.append(fish)

        # Обновим информацию о рыбе в бассейне
        self.biomass += new_fish.get_biomass()
        self.number_fish += new_fish.get_number_fish()

        # Отсортируем рыбу по массе
        self.fishes.sort(key=lambda item: item.mass)

        # Обновим информацию о рыбе в бассейне
        self._update_info()

    def remove_fish(self, number_fish: int, biggest_fish: bool = True) -> ListFish:
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

            return ListFish(removed_fish)

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
