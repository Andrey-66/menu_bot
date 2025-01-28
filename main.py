import os
from datetime import datetime

from dotenv import load_dotenv
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update, ReplyKeyboardRemove
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler, ContextTypes, Application, filters

from constants import SPREADSHEET_ID, SPREADSHEET_RANGE_INGREDIENTS, SPREADSHEET_RANGE_RECIPES
from spreadsheets import google_auth, read_values
from utils import str_to_markdown

load_dotenv()

SERVICE, CREDENTIALS = google_auth()


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
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Обновить", callback_data="update"),
        ],
    ])
    await context.bot.send_chat_action(chat_id=chat.id, action='typing')
    query = update.callback_query
    await query.answer()
    if query.data == 'menu':
        await query.delete_message()
        await context.bot.send_message(
            chat_id=chat.id,
            text=read_values(SERVICE, SPREADSHEET_ID, SPREADSHEET_RANGE_RECIPES, SPREADSHEET_RANGE_INGREDIENTS),
            reply_markup=buttons,
            parse_mode='MarkdownV2'
        )
    elif query.data == 'update':
        await query.edit_message_text(
            text=read_values(SERVICE, SPREADSHEET_ID, SPREADSHEET_RANGE_RECIPES,
                             SPREADSHEET_RANGE_INGREDIENTS) + str_to_markdown(f'\n\n UPD: {datetime.now()}'),
            reply_markup=buttons,
            parse_mode='MarkdownV2'
        )


def main() -> None:
    auth_token = os.getenv('TOKEN')
    application = Application.builder().token(auth_token).build()
    application.add_handler(CallbackQueryHandler(show_menu))
    application.add_handler(CommandHandler('start', wake_up))
    application.add_handler(CommandHandler('menu', show_menu))

    application.add_handler(MessageHandler(filters.TEXT, say_hi))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
