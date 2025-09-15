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
