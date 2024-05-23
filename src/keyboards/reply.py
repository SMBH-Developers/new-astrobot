from aiogram import types


class MenuButton:
    main_menu_mrkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu_mrkup.add(types.KeyboardButton(text='📝 Записаться к астрологу'))
    main_menu_mrkup.add(types.KeyboardButton(text='✨ Все об астрологии'))
