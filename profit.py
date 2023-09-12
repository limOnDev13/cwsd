from cwsd import CWSD
from datetime import date


class Profit:
    def __init__(self, cwsd: CWSD, feed_cost: float, fish_cost: float, start_date: date, start_up_capital: float):
        self.cwsd: CWSD = cwsd
        self.start_date: date = start_date

        self.feed_cost: float = feed_cost
        self.fish_cost: float = fish_cost

        self.days: int = 0
        self.sold_biomass: float = 0.0
        self.spent_feed: float = 0.0

        self.start_up_capital: float = start_up_capital
        self.current_budget: float = start_up_capital
        self.daily_budget: dict[int, float] = {}
        self.income: float = 0.0  # Суммарный доход за все время
        self.expenses: float = 0.0  # Суммарные траты
        self.profit: float = 0.0
