from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Інформація')],
                                     [KeyboardButton(text='Нові авто')],
                                     [KeyboardButton(text='Останні 5 авто')],
                                     [KeyboardButton(text='Завантажити фото')]
                                     ],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')