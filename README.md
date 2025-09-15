# deleting_browser_history_

Отличная идея! Использование автоматизации браузера через Selenium или Playwright - это правильный подход. Вот несколько алгоритмов и реализаций для очистки истории браузера.

## Архитектура решения

### Алгоритм 1: Очистка через UI браузера
```python
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
```

### Алгоритм 2: Очистка через JavaScript (более надежный)
```python
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
```

### Алгоритм 3: Использование Playwright (рекомендуется)
```python
from playwright.sync_api import sync_playwright
import asyncio

class PlaywrightCleaner:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = None
        
    def clear_browser_data(self, user_data_dir=None):
        """Очистка данных браузера через Playwright"""
        try:
            self.browser = self.playwright.chromium.launch_persistent_context(
                user_data_dir=user_data_dir if user_data_dir else "/tmp/chrome-profile",
                headless=False
            )
            
            # Получаем все страницы
            pages = self.browser.pages()
            if pages:
                page = pages[0]
            else:
                page = self.browser.new_page()
            
            # Очистка через devtools protocol
            cdp_session = page.context.new_cdp_session(page)
            cdp_session.send('Storage.clearDataForOrigin', {
                'origin': '*',
                'storageTypes': 'all'
            })
            
            # Альтернативно: очистка через навигацию
            page.goto('chrome://settings/clearBrowserData')
            
            # Ждем и кликаем кнопку очистки
            page.wait_for_selector('//*[@id="clearBrowsingDataConfirm"]')
            page.click('//*[@id="clearBrowsingDataConfirm"]')
            
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            if self.browser:
                self.browser.close()
```

## Алгоритм 4: Полная автоматизация с расписанием
```python
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
```

## Рекомендации по реализации:

1. **Используйте Playwright** - он более стабилен для автоматизации
2. **Работайте с персистентными контекстами** для доступа к данным пользователя
3. **Добавьте обработку ошибок** и логирование
4. **Тестируйте на разных браузерах** (Chrome, Firefox, Edge)
5. **Учитывайте синхронизацию** - очистка на одном устройстве может не сразу синхронизироваться

## Установка и запуск:

1. Установите зависимости:
```bash
pip install playwright selenium schedule
playwright install
```

2. Настройте путь к профилю браузера
3. Запустите скрипт как фоновый процесс

Это решение будет эффективно очищать историю и cookies через автоматизацию реального браузера.
