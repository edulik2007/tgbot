from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, 
                           ReplyKeyboardMarkup, KeyboardButton)


# Для менью
menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Купить бизнес", callback_data = "buy")],
    [InlineKeyboardButton(text="Мои бизнесы", callback_data = "mybuy")],
    [InlineKeyboardButton(text="Баланс", callback_data = "balance"), InlineKeyboardButton(text="Канал", url="https://t.me/busintoness")],
    [InlineKeyboardButton(text="Поддержка", url ='https://t.me/busstonsupport')],
])

# Покупка бизнесов
buybusiness = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Ларёк(0.3 -> 0.45)", callback_data="buy1")],
    [InlineKeyboardButton(text="Магазин(0.5 -> 0.75)", callback_data="buy2")],
    [InlineKeyboardButton(text="Заправка(0.7 -> 1)", callback_data="buy3")],
    [InlineKeyboardButton(text="Отель(1 -> 1.5)", callback_data="buy4")],
    [InlineKeyboardButton(text="Назад", callback_data="nazadmain")]
])

# Покупка бизнеса
payment = InlineKeyboardMarkup(inline_keyboard=[
    
    [InlineKeyboardButton(text="Оплатить", callback_data="pay"), InlineKeyboardButton(text="Назад", callback_data="nazadbuy")]
    
])


# Для кнопки Баланс
withdrawal = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Вывод", callback_data='withdrawal'), InlineKeyboardButton(text="Пополнить", callback_data="popolnit")
        ],
        [InlineKeyboardButton(text="Назад", callback_data="nazad")]
    ]
)

pay = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Оплата", url="https://t.me/send?start=IV18zUgjAdfHn"), InlineKeyboardButton(text="Назад", callback_data="nazadbalance")],
    [InlineKeyboardButton(text="Я оплатил", callback_data='paid')]
])

# Назад кнопка
cancel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data="nazadmain")]
])