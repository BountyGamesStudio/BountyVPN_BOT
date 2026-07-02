import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode

# ---------- КОНФИГ ----------
BOT_TOKEN = "8461545776:AAHDGzyf7sQFA9L3-pHiCjh-GONneOsLsvI"
SUB_LINK = "https://raw.githubusercontent.com/BountyGamesStudio/BountyVPN/refs/heads/main/sub.txt"
SUPPORT_USERNAME = "Durove14"  # Юзернейм поддержки

logging.basicConfig(level=logging.INFO)

# ---------- ИНИЦИАЛИЗАЦИЯ ----------
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ---------- КЛАВИАТУРА ----------
def get_main_keyboard():
    """Главная клавиатура с тремя кнопками."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎁 Получить подписку", callback_data="get_sub")],
            [InlineKeyboardButton(text="📖 Помощь", callback_data="help")],
            [InlineKeyboardButton(text="🆘 Поддержка", callback_data="support")]
        ]
    )

# ---------- ХЭНДЛЕРЫ ----------
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = (
        "╔══════════════════════════════════╗\n"
        "║   🌟 <b>BountyVPN Bot</b> 🌟      ║\n"
        "╚══════════════════════════════════╝\n\n"
        "🔥 <b>Добро пожаловать!</b>\n"
        "Я помогу тебе получить актуальную подписку\n"
        "для приложения <b>Happ</b> всего в один клик.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📌 <b>Как это работает:</b>\n"
        "▸ Нажми кнопку <b>«Получить подписку»</b>\n"
        "▸ Скопируй выданную ссылку\n"
        "▸ Вставь её в приложение Happ (Импорт)\n"
        "▸ Наслаждайся VPN-доступом 🚀\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔒 <b>Безопасность:</b>\n"
        "▸ Ссылка ведёт в официальный репозиторий\n"
        "▸ Подписка обновляется автоматически\n"
        "▸ Данные не сохраняются\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "💡 <i>Нажми «Получить подписку» прямо сейчас!</i>"
    )
    
    await message.answer(
        welcome_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(lambda c: c.data == "get_sub")
async def process_get_sub(callback: types.CallbackQuery):
    await callback.answer()
    
    text = (
        "╔══════════════════════════════════╗\n"
        "║   ✅ <b>Подписка готова!</b>       ║\n"
        "╚══════════════════════════════════╝\n\n"
        "📎 <b>Ваша ссылка:</b>\n"
        f"<code>{SUB_LINK}</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📱 <b>Инструкция:</b>\n"
        "1. Открой приложение <b>Happ</b>\n"
        "2. Перейди в раздел <b>«Импорт»</b>\n"
        "3. Вставь ссылку в поле ввода\n"
        "4. Нажми <b>«Импортировать»</b>\n\n"
        "✨ <i>Готово! Подписка активирована.</i>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔄 <i>Ссылка всегда актуальна — хранится в репозитории BountyVPN.</i>"
    )
    
    await callback.message.answer(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(lambda c: c.data == "help")
async def process_help(callback: types.CallbackQuery):
    await callback.answer()
    
    help_text = (
        "╔══════════════════════════════════╗\n"
        "║   📖 <b>Помощь</b>                ║\n"
        "╚══════════════════════════════════╝\n\n"
        "❓ <b>Частые вопросы:</b>\n\n"
        "▸ <b>Где взять подписку?</b>\n"
        "  Нажми «Получить подписку» — бот выдаст ссылку.\n\n"
        "▸ <b>Как импортировать в Happ?</b>\n"
        "  Скопируй ссылку → Открой Happ → Импорт → Вставь → Готово.\n\n"
        "▸ <b>Ссылка не работает?</b>\n"
        "  Убедись, что скопировал полностью.\n"
        "  Если проблема повторяется — напиши в поддержку.\n\n"
        "▸ <b>Откуда берутся ссылки?</b>\n"
        "  Из официального репозитория BountyVPN на GitHub.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔗 <b>Полезные ссылки:</b>\n"
        "▸ <a href='https://t.me/BountyVPN'>Официальный канал</a>\n"
        "▸ <a href='https://github.com/BountyGamesStudio/BountyVPN'>GitHub-репозиторий</a>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "💬 <i>Есть вопросы? Напиши в поддержку.</i>"
    )
    
    await callback.message.answer(
        help_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_keyboard(),
        disable_web_page_preview=True
    )

@dp.callback_query(lambda c: c.data == "support")
async def process_support(callback: types.CallbackQuery):
    await callback.answer()
    
    support_text = (
        "╔══════════════════════════════════╗\n"
        "║   🆘 <b>Поддержка</b>             ║\n"
        "╚══════════════════════════════════╝\n\n"
        "📞 <b>Связь с поддержкой:</b>\n\n"
        "По всем вопросам, проблемам и предложениям\n"
        "обращайтесь к нашему специалисту:\n\n"
        f"👤 <b>@Durove14</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📌 <b>Что можно решить:</b>\n"
        "▸ Проблемы с подпиской\n"
        "▸ Ошибки при импорте\n"
        "▸ Вопросы по работе VPN\n"
        "▸ Предложения и пожелания\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⏰ <b>Время работы:</b>\n"
        "▸ 24/7 — отвечаем быстро\n"
        "▸ Среднее время ответа: 5-15 минут\n\n"
        "💬 <i>Напишите @Durove14 прямо сейчас!</i>"
    )
    
    # Создаём клавиатуру с кнопкой для прямого перехода в чат поддержки
    support_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✍️ Написать в поддержку", url=f"https://t.me/{SUPPORT_USERNAME}")],
            [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_menu")]
        ]
    )
    
    await callback.message.answer(
        support_text,
        parse_mode=ParseMode.HTML,
        reply_markup=support_keyboard,
        disable_web_page_preview=True
    )

@dp.callback_query(lambda c: c.data == "back_to_menu")
async def process_back_to_menu(callback: types.CallbackQuery):
    await callback.answer()
    
    # Возвращаем пользователя в главное меню
    menu_text = (
        "╔══════════════════════════════════╗\n"
        "║   🏠 <b>Главное меню</b>          ║\n"
        "╚══════════════════════════════════╝\n\n"
        "Вы вернулись в главное меню.\n"
        "Выберите действие ниже:"
    )
    
    await callback.message.answer(
        menu_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_keyboard()
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "╔══════════════════════════════════╗\n"
        "║   📖 <b>Помощь</b>                ║\n"
        "╚══════════════════════════════════╝\n\n"
        "❓ <b>Частые вопросы:</b>\n\n"
        "▸ <b>Где взять подписку?</b>\n"
        "  Нажми «Получить подписку» — бот выдаст ссылку.\n\n"
        "▸ <b>Как импортировать в Happ?</b>\n"
        "  Скопируй ссылку → Открой Happ → Импорт → Вставь → Готово.\n\n"
        "▸ <b>Ссылка не работает?</b>\n"
        "  Убедись, что скопировал полностью.\n"
        "  Если проблема повторяется — напиши в поддержку.\n\n"
        "▸ <b>Откуда берутся ссылки?</b>\n"
        "  Из официального репозитория BountyVPN на GitHub.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔗 <b>Полезные ссылки:</b>\n"
        "▸ <a href='https://t.me/BountyVPN'>Официальный канал</a>\n"
        "▸ <a href='https://github.com/BountyGamesStudio/BountyVPN'>GitHub-репозиторий</a>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "💬 <i>Есть вопросы? Напиши в поддержку.</i>"
    )
    
    await message.answer(
        help_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_keyboard(),
        disable_web_page_preview=True
    )

# ---------- ЗАПУСК ----------
async def main():
    logging.info("Бот BountyVPN запущен с кнопкой поддержки.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
