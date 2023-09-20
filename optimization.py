from cwsd import CWSD
from pool import Pool
from fish import Fish, ListFish, create_list_fish
from datetime import date
from copy import deepcopy


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

    def calculate_growing_time(self, mass: float, number_fish: int) -> int:
        """
        Метод для расчета длительности выращивания с такой средней массой.
        :param mass: Средняя масса рыбки.
        :param number_fish: Количество рыбок, по которому нужно усреднять.
        :return: Количество дней
        """
        list_fish: ListFish = create_list_fish(mass=mass, number_fish=number_fish)
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
            list_fish: ListFish = create_list_fish(number_fish, start_mass)
            pool.add_new_fishes(list_fish)

            for _ in range(days):
                pool.daily_growth()

            if pool.planting_density >= self.max_planting_density:
                break
            else:
                number_fish += step

        return number_fish

    @staticmethod
    def calculate_optimal_number_new_fish_in_current_cwsd(cwsd: CWSD, average_mass: float,
                                                          start_number: int, step: int, end_number: int,
                                                          attempts: int = 100) -> int:
        """
        Метод для определения оптимального количества рыбы в уже работающее узв.
        :param cwsd: Работающее УЗВ.
        :param average_mass: Средняя масса новой рыбы.
        :param start_number: Начальное значение варьируемого количества.
        :param step: Шаг вариации.
        :param end_number: Конечный предел вариации количества.
        :param attempts: Количество проверок.
        :return: Оптимальное количество новой рыбы.
        """
        number_fish: int = start_number
        optimal_quantity: int = start_number
        risk_quantity: int = start_number

        # Сделаем вариацию параметра number_fish
        while number_fish <= end_number:
            print(f'Тестируем с {number_fish} рыб массой {average_mass}')
            success_attempts: int = 0

            for _ in range(attempts):
                test_cwsd: CWSD = deepcopy(cwsd)
                list_fish: ListFish = create_list_fish(number_fish, average_mass)

                # Если есть пустой бассейн, добавим в него рыбу
                if not test_cwsd.add_fish(list_fish):
                    # Если пустых бассейнов нет, добавим в близкий по средней массе
                    test_cwsd.add_fish_in_not_empty_pool(average_mass, list_fish)

                # Начнем ежедневную работу, пока биомасса не опуститься ниже 1 кг, или пока не произойдет переполнение
                success: bool = True
                while test_cwsd.biomass > 1.0:
                    result: dict[str, float] | None = test_cwsd.daily_growth(print_info=False)

                    if result is None:
                        success = False
                        break
                if success:
                    success_attempts += 1
            print(f'Было {success_attempts} попыток из {attempts}')

            if success_attempts == attempts:
                optimal_quantity = number_fish
            if float(success_attempts) / float(attempts) >= 0.9:
                risk_quantity = number_fish
                number_fish += step
            else:
                print(f'Оптимальное значение количества новой рыбы, при котором не происходит переполнение в {attempts}'
                      f' из {attempts} случаев, равно {optimal_quantity}.\n'
                      f'Рискованное значение количества новой рыбы, при котором не происходит переполнение в 90% и выше'
                      f' (в {success_attempts} случаях из {attempts}), равно {risk_quantity}.')
                break
        return optimal_quantity
