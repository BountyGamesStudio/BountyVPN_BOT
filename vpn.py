import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import aiohttp

# --- НАСТРОЙКИ ---
BOT_TOKEN = "8461545776:AAHDGzyf7sQFA9L3-pHiCjh-GONneOsLsvI"
ADMIN_ID = 7728468302  # ТВОЙ ID
URL_SUB = "https://raw.githubusercontent.com/BountyGamesStudio/BountyVPN/refs/heads/main/sub.txt"

# --- РЕКВИЗИТЫ ДЛЯ ОПЛАТЫ (СБП) ---
PAYMENT_DETAILS = {
    "phone": "+7 951 843-60-20",
    "bank": "ВТБ"
}

# --- ИНИЦИАЛИЗАЦИЯ ---
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
async def get_subscription_links() -> list:
    """Загружает список ссылок из файла."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(URL_SUB) as response:
                if response.status == 200:
                    text = await response.text()
                    links = [line.strip() for line in text.split('\n') if line.strip()]
                    return links
                else:
                    logging.error(f"Ошибка загрузки: статус {response.status}")
                    return []
    except Exception as e:
        logging.error(f"Ошибка при запросе к URL: {e}")
        return []

def split_links_by_type(links: list) -> tuple:
    """Разделяет ссылки на бесплатные и донорские."""
    free_links = []
    donor_links = []
    
    donor_keywords = ['премиум', 'premium', 'донат', 'donate', 'vip', 'pro', 
                     'улучш', 'повыш', 'бонус', 'платн', 'paid']
    free_keywords = ['бесплатн', 'free', 'базов', 'basic', 'обычн']
    
    for link in links:
        link_lower = link.lower()
        is_donor = any(keyword in link_lower for keyword in donor_keywords)
        is_free = any(keyword in link_lower for keyword in free_keywords)
        
        if is_donor and not is_free:
            donor_links.append(link)
        elif is_free or (not is_donor and not is_free):
            free_links.append(link)
        else:
            free_links.append(link)
    
    if not donor_links and links:
        split_idx = max(1, int(len(links) * 0.3))
        donor_links = links[:split_idx]
        free_links = links[split_idx:]
    
    return free_links, donor_links

def format_links_text(links: list, max_display: int = 5) -> str:
    """Форматирует ссылки для вывода."""
    if not links:
        return "❌ Ссылки временно недоступны"
    
    text = ""
    for i, link in enumerate(links[:max_display], 1):
        display_link = link if len(link) < 65 else link[:65] + "..."
        text += f"{i}. `{display_link}`\n"
    
    if len(links) > max_display:
        text += f"\n... и ещё {len(links) - max_display} ссылок"
    
    return text

# --- ОБРАБОТЧИКИ КОМАНД ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Приветственное сообщение."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🆓 Получить подписку", callback_data="get_free")],
        [InlineKeyboardButton(text="❤️ Поддержать разработчика", callback_data="donate")],
        [InlineKeyboardButton(text="ℹ️ О боте", callback_data="info")]
    ])
    
    welcome_text = (
        "🌍 *BountyVPN Bot*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🔑 *Подписка бесплатная для всех!*\n"
        "Просто нажми кнопку ниже и получи доступ.\n\n"
        "❤️ Если хочешь поддержать проект — \n"
        "переведи 100 ₽ через СБП и получи \n"
        "улучшенные серверы в подарок! 🎁\n\n"
        "👇 *Выбери действие:*"
    )
    
    await message.answer(
        welcome_text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# --- ОБРАБОТЧИКИ КНОПОК ---
@dp.callback_query(lambda c: c.data == "get_free")
async def process_get_free(callback_query: types.CallbackQuery):
    """Выдает бесплатную подписку."""
    await bot.answer_callback_query(callback_query.id)
    
    loading_msg = await bot.send_message(
        callback_query.from_user.id,
        "⏳ Загружаю серверы..."
    )
    
    all_links = await get_subscription_links()
    free_links, _ = split_links_by_type(all_links)
    
    if not free_links:
        await loading_msg.edit_text(
            "❌ Серверы временно недоступны. Попробуй позже."
        )
        return
    
    text = (
        "🆓 *Бесплатная подписка*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "📡 *Доступные серверы:*\n"
        f"{format_links_text(free_links)}\n\n"
        "🌍 *Страны:* Россия, Германия, США\n"
        "⚡ *Скорость:* до 50 Мбит/с\n"
        "🛡 *Защита:* базовое шифрование\n\n"
        "📲 *Как подключиться:*\n"
        "1. Скопируй ссылку\n"
        "2. Открой приложение *Happ*\n"
        "3. Вставь и подключись\n\n"
        "✅ *Действует бессрочно*"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Скопировать первую ссылку", callback_data="copy_first_free")],
        [InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu")]
    ])
    
    await loading_msg.edit_text(text, parse_mode="Markdown", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == "donate")
async def process_donate(callback_query: types.CallbackQuery):
    """Информация о поддержке разработчика."""
    await bot.answer_callback_query(callback_query.id)
    
    donate_text = (
        "❤️ *Поддержка разработчика*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "💰 *Сумма:* 100 ₽ (разово)\n\n"
        "📱 *Как перевести через СБП:*\n\n"
        "🔹 *По номеру телефона:*\n"
        f"   `{PAYMENT_DETAILS['phone']}`\n\n"
        f"🏦 *Банк:* {PAYMENT_DETAILS['bank']}\n\n"
        "📌 *Инструкция:*\n"
        "1. Открой приложение своего банка\n"
        "2. Выбери «Перевод по номеру телефона» (СБП)\n"
        "3. Введи номер выше и сумму 100 ₽\n"
        "4. В назначении платежа укажи: «Поддержка BountyVPN»\n"
        "5. После перевода нажми кнопку ниже\n"
        "   и отправь скриншот чека\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🎁 *Бонус за поддержку:*\n\n"
        "• 15+ стран вместо 3\n"
        "• Скорость до 500 Мбит/с\n"
        "• Обход всех глушилок\n"
        "• Усиленное шифрование\n"
        "• Приоритетная поддержка\n\n"
        "✅ *После подтверждения платежа*\n"
        "ты получишь улучшенные ссылки!"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Скопировать номер телефона", callback_data="copy_phone")],
        [InlineKeyboardButton(text="📤 Отправить скриншот чека", callback_data="send_receipt")],
        [InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu")]
    ])
    
    await bot.send_message(
        callback_query.from_user.id,
        donate_text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "send_receipt")
async def process_send_receipt(callback_query: types.CallbackQuery):
    """Просит пользователя отправить скриншот."""
    await bot.answer_callback_query(callback_query.id)
    
    text = (
        "📤 *Отправка чека*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "1. Сделай скриншот подтверждения перевода\n"
        "2. Отправь его в этот чат\n"
        "3. После проверки (до 5 минут) ты получишь\n"
        "   улучшенные ссылки!\n\n"
        "🔐 *Проверка:* администратор подтвердит вручную\n\n"
        "📌 *Отправь скриншот прямо сюда:*"
    )
    
    await bot.send_message(
        callback_query.from_user.id,
        text,
        parse_mode="Markdown"
    )

@dp.message(lambda message: message.photo and not message.text)
async def handle_receipt_photo(message: types.Message):
    """Обработка скриншота чека."""
    user_id = message.from_user.id
    username = message.from_user.username or f"ID: {user_id}"
    full_name = message.from_user.full_name or "Не указан"
    
    # Получаем файл
    photo = message.photo[-1]
    file_id = photo.file_id
    
    # Отправляем админу на проверку
    admin_text = (
        f"📩 *Новый платеж на проверку!*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 *Пользователь:* {full_name}\n"
        f"🆔 *Username:* @{username}\n"
        f"🆔 *ID:* `{user_id}`\n"
        f"💰 *Сумма:* 100 ₽\n"
        f"📱 *Способ:* СБП (ВТБ)\n"
        f"📅 *Время:* {message.date.strftime('%d.%m.%Y %H:%M')}\n\n"
        f"✅ *Подтвердить платеж:* /confirm_{user_id}\n"
        f"❌ *Отклонить:* /reject_{user_id}"
    )
    
    # Отправляем админу фото + текст
    await bot.send_photo(
        ADMIN_ID,
        photo=file_id,
        caption=admin_text,
        parse_mode="Markdown"
    )
    
    # Подтверждаем пользователю
    await message.reply(
        "✅ *Скриншот получен!*\n\n"
        "Я отправил его на проверку администратору.\n"
        "Обычно это занимает 1-5 минут.\n"
        "Как только платеж подтвердят — ты получишь бонусные ссылки! 🙌",
        parse_mode="Markdown"
    )

# --- АДМИН-КОМАНДЫ ДЛЯ ПОДТВЕРЖДЕНИЯ ---
@dp.message(lambda message: message.from_user.id == ADMIN_ID and message.text and message.text.startswith("/confirm_"))
async def confirm_payment(message: types.Message):
    """Подтверждение платежа админом."""
    try:
        user_id = int(message.text.split("_")[1])
    except:
        await message.reply("❌ Неверный формат. Используй: /confirm_123456789")
        return
    
    # Загружаем ссылки
    all_links = await get_subscription_links()
    _, donor_links = split_links_by_type(all_links)
    
    if not donor_links:
        await message.reply("❌ Бонусные ссылки временно недоступны.")
        return
    
    # Отправляем пользователю бонусные ссылки
    bonus_text = (
        "🎁 *Поздравляем! Платеж подтвержден!*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Спасибо за поддержку проекта! ❤️\n\n"
        "📡 *Твои улучшенные серверы:*\n"
        f"{format_links_text(donor_links)}\n\n"
        "🌍 *15+ стран мира*\n"
        "⚡ *Скорость до 500 Мбит/с*\n"
        "🚀 *Обход всех глушилок*\n"
        "🛡 *Усиленное шифрование*\n\n"
        "📲 *Инструкция:*\n"
        "1. Скопируй любую ссылку\n"
        "2. Открой приложение *Happ*\n"
        "3. Вставь и наслаждайся!\n\n"
        "🔗 *Доступ навсегда!*"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Скопировать первую ссылку", callback_data="copy_first_donor")],
        [InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu")]
    ])
    
    try:
        await bot.send_message(
            user_id,
            bonus_text,
            parse_mode="Markdown",
            reply_markup=keyboard
        )
        await message.reply(f"✅ Платеж для пользователя ID {user_id} подтвержден. Бонусные ссылки отправлены!")
    except Exception as e:
        await message.reply(f"❌ Ошибка при отправке пользователю: {e}")

@dp.message(lambda message: message.from_user.id == ADMIN_ID and message.text and message.text.startswith("/reject_"))
async def reject_payment(message: types.Message):
    """Отклонение платежа админом."""
    try:
        user_id = int(message.text.split("_")[1])
    except:
        await message.reply("❌ Неверный формат. Используй: /reject_123456789")
        return
    
    try:
        await bot.send_message(
            user_id,
            "❌ *Платеж не подтвержден*\n\n"
            "К сожалению, мы не смогли верифицировать твой перевод.\n"
            "Пожалуйста, проверь правильность суммы и номера,\n"
            "а затем отправь скриншот повторно.\n\n"
            "Если у тебя есть вопросы — напиши @BountyVPN_Admin",
            parse_mode="Markdown"
        )
        await message.reply(f"❌ Платеж для пользователя ID {user_id} отклонен.")
    except Exception as e:
        await message.reply(f"❌ Ошибка при отправке пользователю: {e}")

# --- ОСТАЛЬНЫЕ ОБРАБОТЧИКИ ---
@dp.callback_query(lambda c: c.data == "copy_phone")
async def copy_phone(callback_query: types.CallbackQuery):
    """Копирует номер телефона."""
    await bot.answer_callback_query(callback_query.id, text="Номер скопирован!", show_alert=False)
    await bot.send_message(
        callback_query.from_user.id,
        f"📱 *Номер для СБП:*\n`{PAYMENT_DETAILS['phone']}`",
        parse_mode="Markdown"
    )

@dp.callback_query(lambda c: c.data == "copy_first_free")
async def copy_first_free(callback_query: types.CallbackQuery):
    """Копирует первую бесплатную ссылку."""
    all_links = await get_subscription_links()
    free_links, _ = split_links_by_type(all_links)
    if free_links:
        await bot.answer_callback_query(callback_query.id, text="Ссылка скопирована!", show_alert=False)
        await bot.send_message(
            callback_query.from_user.id,
            f"📋 *Ссылка:*\n`{free_links[0]}`",
            parse_mode="Markdown"
        )
    else:
        await bot.answer_callback_query(callback_query.id, text="Ссылки недоступны", show_alert=True)

@dp.callback_query(lambda c: c.data == "copy_first_donor")
async def copy_first_donor(callback_query: types.CallbackQuery):
    """Копирует первую донатскую ссылку."""
    all_links = await get_subscription_links()
    _, donor_links = split_links_by_type(all_links)
    if donor_links:
        await bot.answer_callback_query(callback_query.id, text="Ссылка скопирована!", show_alert=False)
        await bot.send_message(
            callback_query.from_user.id,
            f"📋 *Бонусная ссылка:*\n`{donor_links[0]}`",
            parse_mode="Markdown"
        )
    else:
        await bot.answer_callback_query(callback_query.id, text="Ссылки недоступны", show_alert=True)

@dp.callback_query(lambda c: c.data == "info")
async def process_info(callback_query: types.CallbackQuery):
    """Информация о боте."""
    await bot.answer_callback_query(callback_query.id)
    text = (
        "🤖 *BountyVPN Bot v2.0*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "📦 *Разработчик:* BountyGamesStudio\n"
        "📅 *Версия:* 2.0 (2026)\n\n"
        "🆓 *Подписка бесплатная*\n"
        "Доступ к VPN получают все пользователи.\n\n"
        "❤️ *Донат (100 ₽ через СБП)*\n"
        "Поддержка разработчика → бонусные серверы\n\n"
        "🎁 *Бонусы за донат:*\n"
        "• 15+ стран\n"
        "• Скорость до 500 Мбит/с\n"
        "• Обход глушилок\n"
        "• Усиленное шифрование\n\n"
        "📡 *Источник ссылок:*\n"
        f"`{URL_SUB}`\n\n"
        "🔒 *Безопасность:* бот не хранит данные"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu")]
    ])
    
    await bot.send_message(
        callback_query.from_user.id,
        text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "back_to_menu")
async def process_back_to_menu(callback_query: types.CallbackQuery):
    """Возвращает в главное меню."""
    await bot.answer_callback_query(callback_query.id)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🆓 Получить подписку", callback_data="get_free")],
        [InlineKeyboardButton(text="❤️ Поддержать разработчика", callback_data="donate")],
        [InlineKeyboardButton(text="ℹ️ О боте", callback_data="info")]
    ])
    
    await bot.send_message(
        callback_query.from_user.id,
        "🌍 *Главное меню*\n\nВыбери действие:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# --- ЗАПУСК БОТА ---
async def main():
    logging.basicConfig(level=logging.INFO)
    print("🤖 BountyVPN Bot v2.0 запущен!")
    print(f"👤 Админ ID: {ADMIN_ID}")
    print("🆓 Бесплатная подписка для всех")
    print(f"❤️ Донат через СБП: {PAYMENT_DETAILS['phone']} (ВТБ)")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
