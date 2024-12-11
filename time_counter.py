from loguru import logger


class TimeCounter:
    def __init__(self, card_records: list[tuple]) -> None:
        self.card_records = card_records
        self.estimations: list[str] | None = None
        self.summ_of_estimation: int | None = None
        self.full_estimation: str | None = None

    def final_estimation(self):
        self.extract_estimations()
        self.full_hours_counter()

        if self.summ_of_estimation < 8:
            self.hours_counter()
            return self.full_estimation
        elif 8 <= self.summ_of_estimation < 40:
            self.days_counter()
            return self.full_estimation
        elif 40 <= self.summ_of_estimation < 160:
            self.weeks_counter()
            return self.full_estimation
        elif self.summ_of_estimation >= 160:
            self.months_counter()
            return self.full_estimation

    def extract_estimations(self) -> None:
        estimations = []

        for record in self.card_records:
            if len(record) > 0:
                estimations.append(record[0])
            else:
                logger.warning("Запись не имеет элементов...")

        self.estimations = estimations

    def full_hours_counter(self) -> None:
        list_of_estimation = self.estimations
        summ_of_estimation = 0

        for element in list_of_estimation:
            counter = 0
            hours_in_element = 0
            place_of_alpha = 0
            for i in range(len(element)):
                if element[i].isalpha():
                    if counter == 0:
                        value_of_time = int(element[:i])
                        if element[i] == 'm':
                            hours_in_element = value_of_time * 160
                        elif element[i] == 'w':
                            hours_in_element = value_of_time * 40
                        elif element[i] == 'd':
                            hours_in_element = value_of_time * 8
                        elif element[i] == 'h':
                            hours_in_element = value_of_time
                        counter += 1
                        place_of_alpha = i
                    else:
                        value_of_time = int(element[place_of_alpha + 1:i])
                        if element[i] == 'w':
                            hours_in_element += value_of_time * 40
                        elif element[i] == 'd':
                            hours_in_element += value_of_time * 8
                        elif element[i] == 'h':
                            hours_in_element += value_of_time
                        place_of_alpha = i
            summ_of_estimation += hours_in_element
            self.summ_of_estimation = summ_of_estimation

    def hours_counter(self):

        # summ_of_estimation = self.summ_of_estimation
        # if summ_of_estimation < 8:
        # estimation = str(self.summ_of_estimation) + 'h'
        self.full_estimation = str(self.summ_of_estimation) + 'h'

    def days_counter(self):

        time_list = []

        days = self.summ_of_estimation // 8
        time_list.extend([str(days), 'd'])

        hours = self.summ_of_estimation % 8
        if hours != 0:
            time_list.extend([str(hours), 'h'])

        estimation = ''.join(time_list)
        self.full_estimation = estimation

    def weeks_counter(self):

        time_list = []

        weeks = self.summ_of_estimation // 40
        time_list.extend([str(weeks), 'w'])

        days = (self.summ_of_estimation - weeks * 40) // 8
        if days != 0:
            time_list.extend([str(days), 'd'])

        hours = (self.summ_of_estimation - weeks * 40) % 8
        if hours != 0:
            time_list.extend([str(hours), 'h'])

        estimation = ''.join(time_list)
        self.full_estimation = estimation

    def months_counter(self):

        time_list = []

        months = self.summ_of_estimation // 160
        time_list.extend([str(months), 'm'])

        weeks = (self.summ_of_estimation - months * 160) // 40
        if weeks != 0:
            time_list.extend([str(weeks), 'w'])

        days = (self.summ_of_estimation - months * 160 - weeks * 40) // 8
        if days != 0:
            time_list.extend([str(days), 'd'])

        hours = (self.summ_of_estimation - months * 160 - weeks * 40) % 8
        if hours != 0:
            time_list.extend([str(hours), 'h'])

        estimation = ''.join(time_list)
        self.full_estimation = estimation
