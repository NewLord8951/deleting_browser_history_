from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class BrowserCleaner:
    def __init__(self, browser_type='chrome'):
        self.browser_type = browser_type
        self.driver = None

    def setup_driver(self):
        """Настройка WebDriver"""
        if self.browser_type == 'chrome':
            from selenium.webdriver.chrome.options import Options
            options = Options()
            options.add_argument('--user-data-dir=/path/to/user/data')
            options.add_argument('--profile-directory=Default')
            self.driver = webdriver.Chrome(options=options)
        elif self.browser_type == 'firefox':
            # Аналогично для Firefox
            pass

    def clear_chrome_history(self):
        """Очистка истории в Chrome"""
        try:
            # Открываем страницу истории
            self.driver.get('chrome://history/')

            # Ждем загрузки страницы
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "history-app"))
            )

            # Очистка через меню
            self.driver.execute_script("""
                const menuButton = document.querySelector('cr-toolbar-menu-button');
                if (menuButton) {
                    menuButton.click();
                    setTimeout(() => {
                        const clearButton = document.querySelector('button#clear-browsing-data');
                        if (clearButton) clearButton.click();
                    }, 1000);
                }
            """)

            # Подтверждение очистки
            time.sleep(2)
            self.driver.execute_script("""
                const dialog = document.querySelector('clear-browsing-data-dialog');
                if (dialog) {
                    dialog.shadowRoot.querySelector('#clearBrowsingDataConfirm').click();
                }
            """)

        except Exception as e:
            print(f"Ошибка: {e}")

    def close(self):
        """Закрытие браузера"""
        if self.driver:
            self.driver.quit()
