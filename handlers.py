from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

def getbot():
    from main import getbot
    return getbot()

router = Router()

# Класс состояния
class registr(StatesGroup):
    summa = State()
    wallet = State()
    selected_business = State()
    business_cost = State()

class givepay(StatesGroup):
    userid = State()
    summa = State()
    

# База балансов и бизнесов
user_balances = {}
user_business = {}

# Обработчик /Start
@router.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    if user_id not in user_balances:
        user_balances[user_id] = 0
    await message.answer_photo(photo='https://ibb.co/Kw7HCPq')
    await message.answer("Добро пожаловать, покупай бизнес и получай доход", reply_markup=kb.menu)

# Обработчик покупки
@router.callback_query(F.data == "buy")
async def buybiznes(callbackquery: CallbackQuery):
    await callbackquery.message.edit_text("Вот бизнесы которые можете купить", reply_markup=kb.buybusiness)
    await callbackquery.answer()
    
# Обработчики товаров
@router.callback_query(F.data == "buy1")
async def buy1(callbackquery: CallbackQuery, state: FSMContext):
    await state.update_data(selected_business="ларёк", business_cost=0.3)
    await callbackquery.message.edit_text("Вы выбрали ларёк(0.3 -> 0.45), ларёк стоит 0.3 тон и приносит +0.15 тон нажимайте на кнопку оплатить чтобы купить бизнес", reply_markup=kb.payment)
    await callbackquery.answer()
   
@router.callback_query(F.data == "buy2")
async def buy2(callbackquery: CallbackQuery, state: FSMContext):
    await state.update_data(selected_business="магазин", business_cost=0.5)
    await callbackquery.message.edit_text("Вы выбрали магазин(0.5 -> 0.75), магазин стоит 0.5 тон и приносит +0.25 тон дохода, нажимайте на кнопку оплатить чтобы купить бизнес", reply_markup=kb.payment)
    await callbackquery.answer() 
    
@router.callback_query(F.data == "buy3")
async def buy3(callbackquery: CallbackQuery, state: FSMContext):
    await state.update_data(selected_business="заправка", business_cost=0.7)
    await callbackquery.message.edit_text("Вы выбрали заправка(0.7 -> 1), заправка стоит 0.7 тон и приносит +0.3 тон, нажимайте на кнопку оплатить чтобы купить бизнес", reply_markup=kb.payment)
    await callbackquery.answer()

@router.callback_query(F.data == "buy4")
async def buy4(callbackquery: CallbackQuery, state: FSMContext):
    await state.update_data(selected_business="отель", business_cost=1.0)
    await callbackquery.message.edit_text("Вы выбрали отель(1 -> 1.5), отель стоит 1 тон и приносит +0.5 тон нажимайте на кнопку оплатить чтобы купить бизнес", reply_markup=kb.payment)
    await callbackquery.answer()
    
# Обработчик кнопки оплатить
@router.callback_query(F.data == "pay")
async def pay(callbackquery: CallbackQuery, state: FSMContext):
    user_id = callbackquery.from_user.id
    data = await state.get_data()
    business_cost = data.get('business_cost')
    selected_business = data.get('selected_business')

    if user_balances.get(user_id, 0) < business_cost:
        await callbackquery.message.edit_text("Недостаточно средств для покупки бизнеса.", reply_markup=kb.cancel)
        await callbackquery.answer()
        return

    user_balances[user_id] -= business_cost

    if user_id not in user_business:
        user_business[user_id] = []
    user_business[user_id].append(selected_business)
    
    await callbackquery.message.edit_text(f"Вы успешно купили {selected_business}. Ваш текущий баланс: {user_balances[user_id]} TON", reply_markup=kb.menu)
    await callbackquery.answer()
    
# Обработчик мои бизнесы
@router.callback_query(F.data == "mybuy")
async def mybuy(callbackquery: CallbackQuery):
    user_id = callbackquery.from_user.id
    if user_id not in user_business or not user_business[user_id]:
        user_business_list = "У вас нет бизнеса"
    else:
        user_business_list = "\n".join(user_business[user_id])
    await callbackquery.message.edit_text(f"Ваши бизнесы:\n\n{user_business_list}", reply_markup=kb.cancel)
    await callbackquery.answer()
    
# Обработчик кнопки баланс
@router.callback_query(F.data == "balance")
async def balance(callbackquery: CallbackQuery):
    user_id = callbackquery.from_user.id
    user_balance = user_balances.get(user_id, 0)
    await callbackquery.message.edit_text(f"Ваш баланс: {user_balance} TON", reply_markup=kb.withdrawal)
    await callbackquery.answer()

# Обработчики пополнения баланса
@router.callback_query(F.data == "popolnit")
async def popolnit(callbackquery: CallbackQuery):
    await callbackquery.message.edit_text("Указывайте сумму в счёте которую хотите получить, оставляйте ваш никнейм в комментарий к платежу, оплачивайте и нажмите на кнопку 'я оплатил'", reply_markup=kb.pay)
    await callbackquery.answer()
    
@router.callback_query(F.data == "paid")
async def paid(callbackquery: CallbackQuery):
    bot = getbot()
    user_name = callbackquery.from_user.username
    await callbackquery.message.answer("Хорошо, сейчас админ проверит оплату и начислит деньги на ваш баланс")
    await bot.send_message(1098185428, f"Пользователь @{user_name} нажал на кнопку я оплатил, проверьте оплату, его id: <code>{callbackquery.from_user.id}</code>", parse_mode="HTML")
    
# Обработчики кнопки назад
@router.callback_query(F.data == "nazadmain")
async def nazadmain(callbackquery: CallbackQuery):
    await callbackquery.message.edit_text("Добро пожаловать, покупай бизнес и получай доход", reply_markup=kb.menu)
    await callbackquery.answer()

@router.callback_query(F.data == "nazadbuy")
async def nazadbuy(callbackquery: CallbackQuery):
    await callbackquery.message.edit_text("Вот бизнесы которые можете купить", reply_markup=kb.buybusiness)
    await callbackquery.answer()
    
@router.callback_query(F.data == "nazad")
async def cancel(callbackquery: CallbackQuery):
    await callbackquery.message.edit_text("Добро пожаловать, покупай бизнес и получай доход", reply_markup=kb.menu)
    await callbackquery.answer()
    
@router.callback_query(F.data == "nazadbalance")
async def cancel(callbackquery: CallbackQuery):
    user_id = callbackquery.from_user.id
    user_balance = user_balances.get(user_id, 0)
    await callbackquery.message.edit_text(f"Ваш баланс: {user_balance} TON", reply_markup=kb.withdrawal)
    await callbackquery.answer()
    
# Состояние Вывода
@router.callback_query(F.data == "withdrawal")
async def summa(callbackquery: CallbackQuery, state: FSMContext):
    user_id = callbackquery.from_user.id
    balance = user_balances.get(user_id, 0)
    await state.set_state(registr.summa)
    await callbackquery.message.answer(f"Баланс: {balance} Ton\nВведите сумму для вывода")

@router.message(registr.summa)
async def wallet(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите правильное числовое значение.")
        return

    user_id = message.from_user.id
    balance = user_balances.get(user_id, 0)

    if amount > balance:
        await message.answer("Недостаточно средств на балансе.")
        return

    await state.update_data(summa=amount)
    await state.set_state(registr.wallet)
    await message.answer("Введите ваш кошелёк")

@router.message(registr.wallet)
async def endstate(message: Message, state: FSMContext):
    bot = getbot()
    user_id = message.from_user.id
    
    if user_id not in user_balances:
        user_balances[user_id] = 0
    data = await state.get_data()
    amount = data.get('summa')

    user_balances[user_id] -= amount

    await state.update_data(wallet=message.text)
    data = await state.get_data()

    await message.answer(
        f"Сумма вывода: {data['summa']} TON\nКошелёк для вывода: {data['wallet']}\n\nЗаявка на вывод создана!", reply_markup=kb.cancel
    )
    
    await bot.send_message(1098185428, f"Пользователь @{message.from_user.username} Заказал(а) выплату\n\nСумма вывода: {data['summa']} TON\nКошелёк для вывода: <code>{data['wallet']}</code>", parse_mode="HTML")
    await state.clear()

# Состояния пополнения баланса
@router.message(Command("popolnit"))
async def vivod(message: Message, state: FSMContext):
    bot = getbot()
    await state.set_state(givepay.userid)
    await bot.send_message(1098185428, "Введите юзер ид пользователья")
    
@router.message(givepay.userid)
async def vivod(message: Message, state: FSMContext):
    bot = getbot()
    await state.update_data(userid = message.text)
    await state.set_state(givepay.summa)
    await bot.send_message(1098185428, "Введите сумму пополнения")
    
@router.message(givepay.summa)
async def vivod(message: Message, state: FSMContext):
    bot = getbot()
    await state.update_data(summa = message.text)
    data = await state.get_data()
        
    user_id = int(data['userid'])  
    amount = float(data['summa'])
    
    if user_id not in user_balances:
        user_balances[user_id] = 0
        
    user_balances[user_id] += amount
    await bot.send_message(1098185428, "Вы успешно пополнили баланс пользователья")
    await bot.send_message(user_id, f"Ваша пополнение суммой {amount} тон успешно пришло на ваш баланс")
    await state.clear
    