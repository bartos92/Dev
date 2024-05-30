from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import random


def get_car_info(number):

    user_agent = UserAgent()
    proxy_list = [f"http://dqN3W92Z:QM2PX9h9@45.147.149.43:64674", "http://dqN3W92Z:QM2PX9h9@192.177.161.62:63532", "http://dqN3W92Z:QM2PX9h9@192.177.144.218:64108"]

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent.random}")
    proxy = random.choice(proxy_list)
    options.add_argument(f'--proxy-server={proxy}')
    # Налаштування браузера
    # options = Options()
    options.headless = True  # Використовувати безголовий режим, щоб не відкривати браузер

    # Ініціалізація веб-драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Відкриття сторінки
    driver.get(f'https://ua.carplates.app/number/{number}')

    # Затримка для завантаження контенту (може знадобитися налаштувати)
    driver.implicitly_wait(10)

    # Збір інформації про назву, модель та рік машини
    brand = driver.find_element(By.CLASS_NAME, 'brand').text.strip()
    model = driver.find_element(By.CLASS_NAME, 'model').text.strip()
    make_year = driver.find_element(By.CLASS_NAME, 'make_year').text.strip()
    avg_price = driver.find_element(By.CLASS_NAME, 'price').text.strip()

    color_element = driver.find_element(By.XPATH, "//div[@class='horizontal-property is-selected' and .//span[text()='Колір']]//span[@class='primary-text']")
    color = color_element.text.strip()

    type_element = driver.find_element(By.XPATH, "//div[@class='horizontal-property' and .//span[text()='Тип']]//span[@class='primary-text']")
    car_type = type_element.text.strip()
    
    fuel_element = driver.find_element(By.XPATH, "//div[@class='horizontal-property' and .//span[text()='Паливо']]//span[@class='primary-text']")
    fuel_type = fuel_element.text.strip()
    
    engine_element = driver.find_element(By.XPATH, "//div[@class='horizontal-property' and .//span[text()=\"Об'єм двигуна\"]]//span[@class='primary-text']")
    engine = engine_element.text.strip()
    
    weight_element = driver.find_element(By.XPATH, "//div[@class='horizontal-property' and .//span[text()='Маса/Макс. маса']]//span[@class='primary-text']")
    weight = weight_element.text.strip()
    
    body_element = driver.find_element(By.XPATH, "//div[@class='horizontal-property' and .//span[text()='Категорія/Кузов']]//span[@class='primary-text']")
    body = body_element.text.strip()
    
    # Виведення отриманих даних
    print(f'Назва: {brand}')
    print(f'Модель: {model}')
    print(f'Рік: {make_year}')
    print(f'Середня ціна на ринку: {avg_price}')
    print(f'Колір: {color}')
    print(f'Тип: {car_type}')
    print(f'Паливо: {fuel_type}')
    print(f"Об'єм двигуна: {engine}")
    print(f"Маса/Макс. маса: {weight}")
    print(f"Кузов: {body}")

    # Закриття веб-драйвера
    driver.quit()

def main():
    get_car_info("ВC1905TE")
    
if __name__ == "__main__":
    main()