import re

from db.structured_data.card import DBCardEstimationResponse


class EstimationCounter:
    def __init__(self, records: list[DBCardEstimationResponse]) -> None:
        self.card_records = records
        self.estimations: list[str] = []
        self.summ_of_estimation: int = 0
        self.full_estimation: str = ""

    def final_estimation(self) -> str:
        self.extract_estimations()
        self.summ_of_estimation = self.calculate_total_hours()
        self.full_estimation = self.format_time(self.summ_of_estimation)
        return self.full_estimation

    def extract_estimations(self) -> None:
        self.estimations = [record.estimation for record in self.card_records]

    def calculate_total_hours(self) -> int:
        total = 0
        for element in self.estimations:
            total += self.parse_time_element(element)
        return total

    @staticmethod
    def parse_time_element(element: str) -> int:
        total_hours = 0
        pattern = re.compile(r"(\d+)([mwedh])")
        matches = pattern.findall(element)
        for value, unit in matches:
            value = int(value)
            if unit == "m":
                total_hours += value * 160
            elif unit == "w":
                total_hours += value * 40
            elif unit == "d":
                total_hours += value * 8
            elif unit == "h":
                total_hours += value
        return total_hours

    @staticmethod
    def format_time(total_hours: int) -> str:
        units = [(160, "m"), (40, "w"), (8, "d"), (1, "h")]
        time_list = []
        remaining = total_hours
        for divisor, unit in units:
            if divisor == 1:
                if remaining > 0:
                    time_list.append(f"{remaining}{unit}")
                break
            count, remaining = divmod(remaining, divisor)
            if count > 0:
                time_list.append(f"{count}{unit}")
            if remaining == 0:
                break
        return "".join(time_list)
