import schedule
import time
from datetime import datetime


class ScheduledCleaner:
    def __init__(self):
        self.cleaner = PlaywrightCleaner()

    def daily_clean(self):
        """Ежедневная очистка в 3:00"""
        print(f"{datetime.now()}: Запуск ежедневной очистки")
        self.cleaner.clear_browser_data()

    def weekly_clean(self):
        """Еженедельная очистка"""
        print(f"{datetime.now()}: Запуск еженедельной очистки")
        self.cleaner.clear_browser_data()

    def run_scheduler(self):
        """Запуск планировщика"""
        schedule.every().day.at("03:00").do(self.daily_clean)
        schedule.every().sunday.at("04:00").do(self.weekly_clean)

        while True:
            schedule.run_pending()
            time.sleep(60)


# Использование
if __name__ == "__main__":
    cleaner = ScheduledCleaner()
    cleaner.run_scheduler()
