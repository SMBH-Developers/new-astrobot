from aiogram import types


class Markups:
    welcome_mrkup = types.InlineKeyboardMarkup()
    welcome_mrkup.add(types.InlineKeyboardButton(text='🔮 Предназначение и реализация', callback_data='welcome:purpose'))
    welcome_mrkup.add(types.InlineKeyboardButton(text='🗺️ Личный гороскоп по дате рождения', callback_data='welcome:horoscope'))
    welcome_mrkup.add(types.InlineKeyboardButton(text='👫 Совместимость с человеком', callback_data='welcome:compatibility'))
    welcome_mrkup.add(types.InlineKeyboardButton(text='🏆 Предназначение и склонности к богатству', callback_data='welcome:wealth'))
 
    admin_mrkup = types.InlineKeyboardMarkup()
    admin_mrkup.add(types.InlineKeyboardButton(text='Пользователей всего', callback_data='Admin_Users_Total'))
    admin_mrkup.add(types.InlineKeyboardButton(text='Пользователей за сегодня', callback_data='Admin_Users_For_TODAY'))
    
    back_admin_mrkup = types.InlineKeyboardMarkup()
    back_admin_mrkup.add(types.InlineKeyboardButton(text='⬅️ В меню админа', callback_data='Admin_BACK'))

    main_menu_mrkup = types.InlineKeyboardMarkup()
    main_menu_mrkup.add(types.InlineKeyboardButton(text='🙄Что такое натальная карта рождения', callback_data='main:map'))
    main_menu_mrkup.add(types.InlineKeyboardButton(text='☀️Cовет дня', callback_data='main:day'))


    