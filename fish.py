import random


class Fish:
    """
    Класс для хранения информации о каждой рыбке
    """

    @staticmethod
    def _calculate_random_mac() -> float:
        """
        Расчет случайного значения коэффициента массонакопления
        по нормальному распределению.
        :return: Коэффициент массонакопления (mass accumulation coefficient)
        """
        min_mass_accumulation: float = 0.07
        max_mass_accumulation: float = 0.087

        medium: float = (max_mass_accumulation + min_mass_accumulation) / 2
        # Стандартное отклонение возьмем из расчета, что 68% выпадает
        # на вторую треть промежутка между min_mass_accumulation
        # и max_mass_accumulation
        standard_deviation: float = \
            ((max_mass_accumulation - min_mass_accumulation) / 3) / 2

        mass_accumulation_coefficient: float = random.gauss(medium,
                                                            standard_deviation)
        return mass_accumulation_coefficient

    def __init__(self, start_mass: float, feed_ratio: float = 1.5):
        self.mass: float = start_mass  # текущая масса
        self.feed_ratio: float = feed_ratio  # кормовой коэффициент
        self._mac: float = self._calculate_random_mac()  # коэффициент массонакопления

    def daily_growth(self) -> dict[str, float]:
        """
        Метод для расчета суточного выращивания данной рыбы.
        :return: Возвращает словарь с информацией об абсолютном значении прироста
        и затраченного корма.
        Словарь имеет вид {'mass_increase': ...,
        'required_feed': ...}
        """
        # Масса в начале суток
        previous_mass: float = self.mass
        # Масса в конце суток
        next_mass: float = \
            (previous_mass ** (1 / 3) + self._mac / 3) ** 3
        # Относительный суточный прирост
        relative_daily_increase: float =\
            (next_mass - previous_mass) * 100 / previous_mass
        # Абсолютный суточный прирост
        mass_increase: float = next_mass - previous_mass
        # Норма кормления
        feeding_rate: float = relative_daily_increase * self.feed_ratio
        # масса затраченного корма
        required_feed: float = previous_mass * feeding_rate / 100

        self.mass = next_mass

        return {'mass_increase': mass_increase,
                'required_feed': required_feed}

    def print(self):
        """
        Метод для печати массы рыбки.
        :return: Ничего
        """
        print(f'Масса рыбки: {self.mass}')


"""
fish: Fish = Fish(100.0, 1.5)
days: int = 100

for _ in range(days):
    fish.daily_growth()
    fish.print()
"""
