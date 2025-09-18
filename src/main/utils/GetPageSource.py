from selenium import webdriver

class GetPageSource:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # remove if you want to see browser
        self.driver = webdriver.Chrome(options=options)

    def store_dom(self, url, filepath):
        try:
            self.driver.get(url)
            # Wait for JS to load (you can make this smarter with WebDriverWait)
            self.driver.implicitly_wait(5)
            
            page_source = self.driver.page_source

            with open(filepath, 'rb') as f:
                f.write(page_source)

        finally:
            self.driver.quit()