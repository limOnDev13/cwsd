from cwsd import CWSD
from datetime import date
from optimization import Optimization
from fish import create_list_fish


class Profit:
    def __init__(self, cwsd: CWSD, feed_cost: float, prices_for_fry: list[list[float, int]], fish_cost: float,
                 start_date: date, start_up_capital: float):
        """
        __init__
        :param cwsd: Объект УЗВ.
        :param feed_cost: Стоимость килограмма корма.
        :param prices_for_fry: Список цен для каждой массы. Список составлен по убыванию массы.
         Имеет вид [[mass1, price1], ...].
        :param fish_cost: Стоимость килограмма рыбы.
        :param start_date: Дата зарыбления.
        :param start_up_capital: Начальный капитал.
        """
        self.cwsd: CWSD = cwsd
        self.start_date: date = start_date

        self.feed_cost: float = feed_cost
        self.fish_cost: float = fish_cost

        self.prices_for_fry: list[list[float, int]] = prices_for_fry

        self.start_up_capital: float = start_up_capital
        self.current_budget: float = start_up_capital
        self.daily_budget: dict[int, float] = {}
        self.income: float = 0.0  # Суммарный доход за все время
        self.expenses: float = 0.0  # Суммарные траты
        self.profit: float = 0.0
        self.optimization: Optimization = Optimization(
            number_pools=cwsd.number_pools,
            pool_area=cwsd.pool_area,
            max_planting_density=cwsd.max_planting_density,
            commercial_fish_mass=cwsd.commercial_fish_mass,
            min_package=cwsd.min_package
        )

    def work_cwsd(self, days: int, print_info: bool = False):
        """
        Метод, который ведет подсчет расходов и доходов за указанное количество дней.
        :param days: Количество дней работы УЗВ.
        :param print_info: Если нужно писать подробную информацию, то True, иначе - False.
        :return: Пока не знаю, наверное это будет словарь с необходимыми результатами.
        """
        for day in range(days):
            # Проанализируем дневной результат
            daily_result: dict[str, float] | None = self.cwsd.daily_growth(print_info=False)
            if print_info:
                self.cwsd.print()
                print()
                print(f"За сегодня биомасса увеличилась на {daily_result['biomass_increase']} кг.\n"
                      f"Сегодня было потрачено {daily_result['spent_feed']} кг корма.\n"
                      f"Сегодня было продано {daily_result['sold_biomass']} кг рыбы.")

            # Сохраним изменение бюджета
            daily_income: float = daily_result['sold_biomass'] * self.fish_cost
            daily_expenses: float = daily_result['spent_feed'] * self.feed_cost

            # Добавим новую рыбу, если есть пустые бассейны
            number_empty_pools: int = self.cwsd.have_empty_pool()

            for number_empty_pool in range(number_empty_pools):
                mass: float = self.prices_for_fry[number_empty_pool][0]
                number_new_fish: int = self.optimization.calculate_optimal_number_new_fish_in_current_cwsd(
                    cwsd=self.cwsd,
                    average_mass=mass,
                    start_number=10,
                    step=10,
                    end_number=5000
                )

                self.cwsd.add_fish(create_list_fish(number_fish=number_new_fish, mass=mass))
                daily_expenses += mass * number_new_fish * self.prices_for_fry[number_empty_pool][1]
                if print_info:
                    print(f'В УЗВ (в пустой бассейн) добавлено {number_new_fish} рыб массой {mass}.')

            # Сохраним информацию о расходах и доходах
            self.current_budget += daily_income - daily_expenses
            self.income += daily_income
            self.expenses += daily_expenses
            self.profit = self.income - self.expenses - self.start_up_capital
