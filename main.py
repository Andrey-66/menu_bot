import os
from datetime import datetime

from dotenv import load_dotenv
from telegram import (CallbackQuery, InlineKeyboardButton,
                      InlineKeyboardMarkup, Update)
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes)

from constants import (MENU_TITLE, SPREADSHEET_ID,
                       SPREADSHEET_RANGE_AVAILABLE_COCKTAILS,
                       SPREADSHEET_RANGE_COCKTAILS,
                       SPREADSHEET_RANGE_INGREDIENTS,
                       SPREADSHEET_RANGE_RECIPES)
from spreadsheets import google_auth, read_menu, read_sheet
from utils import (build_menu_buttons, menu_dict_to_str, str_to_markdown,
                   update_message)

load_dotenv()

SERVICE, CREDENTIALS = google_auth()


async def wake_up(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('Показать меню', callback_data='action_selection_menu'),
        ],
    ])
    await context.bot.send_message(
        chat_id=chat.id,
        text='Спасибо, что включили меня',
        reply_markup=buttons
    )


async def error(query: CallbackQuery):
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('Показать меню', callback_data='action_selection_menu'),
        ],
    ])
    await update_message(query, buttons, 'Что-то пошло не так, начнём с начала?')


async def show_menu_list(query: CallbackQuery) -> None:
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Назад", callback_data="action_selection_menu"),
            InlineKeyboardButton("Обновить", callback_data="update_list"),
        ],
    ])
    await update_message(
        query,
        buttons,
        menu_dict_to_str(read_menu(SERVICE, SPREADSHEET_ID, SPREADSHEET_RANGE_RECIPES,
                                   SPREADSHEET_RANGE_INGREDIENTS), menu_title=MENU_TITLE) + str_to_markdown(
            f'\n\n UPD: {datetime.now()}'),
        parse_mode='MarkdownV2'
    )


async def show_menu(query: CallbackQuery, text='Нажми на коктейль, чтобы узнать подробнее') -> None:
    print(text)
    menu = read_menu(SERVICE, SPREADSHEET_ID, SPREADSHEET_RANGE_RECIPES, SPREADSHEET_RANGE_INGREDIENTS)
    buttons = build_menu_buttons(menu)
    await update_message(query, buttons, text)


async def show_cocktail(query: CallbackQuery) -> None:
    menu = read_menu(SERVICE, SPREADSHEET_ID, SPREADSHEET_RANGE_RECIPES, SPREADSHEET_RANGE_INGREDIENTS)
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Назад", callback_data="action_selection_menu")
        ],
    ])
    cocktail = {
        query.data: menu.get(query.data)
    }
    text = menu_dict_to_str(cocktail)
    if query.message.reply_markup != buttons:
        await query.edit_message_text(
            text=text,
            reply_markup=buttons,
            parse_mode='MarkdownV2'
        )


async def buttons_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    FUNCTIONS = {
        'update_list': show_menu_list,
        'show_menu_list': show_menu_list,
        'action_selection_menu': show_menu
    }
    chat = update.effective_chat
    await context.bot.send_chat_action(chat_id=chat.id, action='typing')
    query = update.callback_query
    await query.answer()
    print(query.data)
    if query.data in FUNCTIONS.keys():
        await FUNCTIONS[query.data](query)
    else:
        cocktails_range = read_sheet(SERVICE, SPREADSHEET_ID, SPREADSHEET_RANGE_COCKTAILS).get('values')
        available_cocktails_range = read_sheet(SERVICE, SPREADSHEET_ID, SPREADSHEET_RANGE_AVAILABLE_COCKTAILS).get(
            'values')
        cocktails = set()
        available_cocktails = set()
        for row in available_cocktails_range:
            if row[0]:
                available_cocktails.add(row[0])
        for row in cocktails_range:
            if row and row[0]:
                cocktails.add(row[0])
        if query.data in available_cocktails:
            await show_cocktail(query)
        elif query.data in cocktails:
            await show_menu(query, 'Коктейль закончился :(')
        else:
            await error(query)


def main() -> None:
    auth_token = os.getenv('TOKEN')
    application = Application.builder().token(auth_token).build()
    application.add_handler(CallbackQueryHandler(buttons_handler))
    application.add_handler(CommandHandler('start', wake_up))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
