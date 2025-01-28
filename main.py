import os

from dotenv import load_dotenv
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update, ReplyKeyboardRemove
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler, ContextTypes, Application, filters

from constants import MENU

load_dotenv()


async def say_hi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Показать меню", callback_data="menu"),
        ],
    ])
    await context.bot.send_message(
        chat_id=chat.id,
        text='Используй, пожалуйста, команды',
        reply_markup=buttons
    )


async def wake_up(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Показать меню", callback_data="menu"),
        ],
    ])
    await context.bot.send_message(
        chat_id=chat.id,
        text='Спасибо, что включили меня',
        reply_markup=buttons
    )


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    await context.bot.send_message(chat_id=chat.id, text=MENU)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.delete_message()
    await show_menu(update, context)
    print(query.data)


def main() -> None:
    auth_token = os.getenv('TOKEN')
    application = Application.builder().token(auth_token).build()
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(CommandHandler('start', wake_up))
    application.add_handler(CommandHandler('menu', show_menu))

    application.add_handler(MessageHandler(filters.TEXT, say_hi))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
