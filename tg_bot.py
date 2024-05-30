import asyncio
import json
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold
from config import token, user_id
from main import check_new_golf
import keybord as kb
import easyocr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import re
from nomeroff_net import pipeline
from nomeroff_net.tools import unzip
import warnings
import time


bot = Bot(token=token)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привіт!", reply_markup=kb.main)
    await message.reply("Що вас цікавить?")

@dp.message(F.text == "Нові авто")
async def get_fresh_car(message: Message):
    fresh_golf = check_new_golf()
    if len(fresh_golf) >= 1:
        for k, v in sorted(fresh_golf.items()):
            car = f"{(v['Title'])}\n"\
                  f"{v['Price']}\n" \
                  f"{v['Location']}\n" \
                  f"{v['Url']}"
            await message.answer(car)
    else:
        await message.answer("Нових авто поки що немає...")

@dp.message(F.text == "Останні 5 авто")
async def get_latest_cars(message: Message):
    with open("all_golf_dict.json") as file:
        car_dict = json.load(file)
    for k, v in sorted(car_dict.items())[-5:]:
        car = f"{(v['Title'])}\n"\
              f"{v['Price']}\n" \
              f"{v['Location']}\n" \
              f"{v['Url']}"
        await message.answer(car)

@dp.message(F.text == "Інформація")
async def get_information(message: Message):
    await message.answer(
        f"{('💬 Інформація 💬')}\n\n"
        f"Цей бот вміє розпізнавати номера автомобіля та надавати інформацію про нього з відкритих джерел.\n\n"
        f"❗️Це лише початковий прототип, деякі функції бота показують лише приклад роботи.\n\n"
        f"🆕Нові авто: відстежує появу нових оголошеннь(на прикладі марки BMW)\n\n"
        f"5️⃣Останні 5 авто: показує останні 5 актуальних оголошень(на прикладі марки BMW)\n\n"
        f"🤖Розпізнати фото: розпізнає номера автомобіля на фото, та надає інформацію про нього з відкритих джерел\n\n"
        # f"💾 Код бота на GitHub: https://github.com/bartos92\n"
    )

@dp.message(F.text == "Завантажити фото")
async def download_photo(message: Message):
    await message.answer("Будь ласка, надішліть фото, яке ви хочете розпізнати.")

# Оновлений декоратор для обробки повідомлень з фото
@dp.message(F.content_type == ContentType.PHOTO)
async def handle_photo(message: Message):
    await message.answer(f"Розпізнавання...")
    photo = message.photo[-1]  # Останнє фото найвищої якості
    file_info = await bot.get_file(photo.file_id)
    file_path = file_info.file_path
    file = await bot.download_file(file_path)

    # Збереження фото
    image_path = "downloaded_photo.jpg"
    with open(image_path, "wb") as f:
        f.write(file.getvalue())

    plate_text = read_plate(image_path)[0][0]

    # # Виконання розпізнавання тексту
    # plate_text = recognize_text(image_path)[:10]
    # plate_text = re.sub(r"\s+", "", plate_text)
    print(plate_text)
    await message.answer(f"Розпізнаний номер: {plate_text}")
    await message.answer(f"Шукаю інформацію про автомобіль...")
    # Отримання інформації про автомобіль
    car_info = get_car_info(plate_text)

    print(car_info)

    # Виведення отриманих даних
    await message.answer(f"Інформація про автомобіль:\n{car_info}")

    time.sleep(5)

# Функція для розпізнавання тексту на зображенні
def recognize_text(image_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path)
    plate_text = ""
    for detection in result:
        plate_text += detection[1] + " "
    return plate_text

# Функція для отримання інформації про автомобіль
def get_car_info(number):
    
    # Налаштування браузера
    options = Options()
    options.headless = True  # Використовувати безголовий режим, щоб не відкривати браузер

    # Ініціалізація веб-драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


    try:
    # Відкриття сторінки
        plate_info_path = driver.get(f'https://ua.carplates.app/number/{number}')

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
        car_info = (
                f'Назва: {brand}\n'
                f'Модель: {model}\n'
                f'Рік: {make_year}\n'
                f'Середня ціна на ринку: {avg_price}\n'
                f'Колір: {color}\n'
                f'Тип: {car_type}\n'
                f'Паливо: {fuel_type}\n'
                f"Об'єм двигуна: {engine}\n"
                f"Маса/Макс. маса: {weight}\n"
                f"Кузов: {body}"
            )

        print(plate_info_path)

    except Exception as e:
        car_info = "Виникла помилка, спробуйте ще раз через декілька хвилин.."
    finally:
    # Закриття веб-драйвера
        driver.quit()

    return car_info

def read_plate(img_path):
    number_plate_detection_and_reading = pipeline("number_plate_detection_and_reading", 
                                                  image_loader="opencv")

    (images, images_bboxs, 
     images_points, images_zones, region_ids, 
     region_names, count_lines, 
     confidences, texts) = unzip(number_plate_detection_and_reading([img_path]))
    
    return texts

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
# Suppress warnings from torchvision
    warnings.filterwarnings("ignore", module="torchvision")
    warnings.filterwarnings("ignore", module="nomeroff_net")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Вимкнено!")
