import easyocr
# Визначення функції для розпізнавання тексту на зображенні
def recognize_text(image_path):
    # Використання EasyOCR для розпізнавання тексту на зображенні
    reader = easyocr.Reader(['uk'])  # ініціалізуємо модель для англійської мови
    result = reader.readtext(image_path)
    # Обробка результатів розпізнавання
    plate_text = ""
    for detection in result:
        plate_text += detection[1] + " "  # текст розпізнання з кожної області
    return plate_text
# Зображення з номером машини

image_path = 'example1.jpeg'
# Розпізнавання тексту на зображенні
plate_text = recognize_text(image_path)[:10]
print("Розпізнаний текст:", plate_text)