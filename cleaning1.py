from selenium import webdriver
import time


class JavaScriptCleaner:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def clear_via_javascript(self):
        """Очистка через выполнение JavaScript"""
        try:
            # Открываем любой сайт для выполнения JS
            self.driver.get('https://google.com')

            # Очистка localStorage
            self.driver.execute_script("localStorage.clear();")

            # Очистка sessionStorage
            self.driver.execute_script("sessionStorage.clear();")

            # Очистка cookies
            self.driver.delete_all_cookies()

            # Для indexedDB и других хранилищ
            self.driver.execute_script("""
                try {
                    indexedDB.databases().then(function(databases) {
                        databases.forEach(function(database) {
                            indexedDB.deleteDatabase(database.name);
                        });
                    });
                } catch(e) {}

                // Очистка service workers
                if ('serviceWorker' in navigator) {
                    navigator.serviceWorker.getRegistrations().then(function(registrations) {
                        registrations.forEach(function(registration) {
                            registration.unregister();
                        });
                    });
                }
            """)

        except Exception as e:
            print(f"Ошибка: {e}")
