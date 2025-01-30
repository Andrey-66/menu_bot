import os
from datetime import datetime
from typing import Any, Callable, Coroutine, Dict, Optional

from constants import (
    MEDIA_DIR,
    MENU_TITLE,
    SPREADSHEET_ID,
    SPREADSHEET_RANGE_AVAILABLE_COCKTAILS,
    SPREADSHEET_RANGE_COCKTAILS,
    SPREADSHEET_RANGE_INGREDIENTS,
    SPREADSHEET_RANGE_RECIPES,
)
from dotenv import load_dotenv
from spreadsheets import google_auth, read_menu, read_sheet
from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes
from utils import build_menu_buttons, menu_dict_to_str, str_to_markdown, update_message

load_dotenv()

SERVICE, CREDENTIALS = google_auth()


async def wake_up(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Показать меню", callback_data="action_selection_menu"),
            ],
        ]
    )
    await context.bot.send_message(chat_id=chat.id, text="Спасибо, что включили меня", reply_markup=buttons)


async def error(query: CallbackQuery):
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Показать меню", callback_data="action_selection_menu"),
            ],
        ]
    )
    await update_message(query,              buttons, "Что-то пошло не так, начнём с начала?")


async def show_menu_list(query: CallbackQuery, text: Optional[str] = MENU_TITLE) -> None:
    if text is None:
        text = ""
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Назад", callback_data="action_selection_menu"),
                InlineKeyboardButton("Обновить", callback_data="update_list"),
            ],
        ]
    )
    await update_message(
        query,
        buttons,
        menu_dict_to_str(
            read_menu(
                SERVICE,
                SPREADSHEET_ID,
                SPREADSHEET_RANGE_RECIPES,
                SPREADSHEET_RANGE_INGREDIENTS,
            ),
            menu_title=text,
        )
        + str_to_markdown(f"\n\n UPD: {datetime.now()}"),
        parse_mode="MarkdownV2",
    )


async def show_menu(
    query: CallbackQuery,
    text: Optional[str] = "Нажми на коктейль, чтобы узнать подробнее",
) -> None:
    menu = read_menu(
        SERVICE,
        SPREADSHEET_ID,
        SPREADSHEET_RANGE_RECIPES,
        SPREADSHEET_RANGE_INGREDIENTS,
    )
    buttons = build_menu_buttons(menu)
    if text is None:
        text = ""
    await update_message(query, buttons, text)


async def show_cocktail(query: CallbackQuery) -> None:
    menu = read_menu(
        SERVICE,
        SPREADSHEET_ID,
        SPREADSHEET_RANGE_RECIPES,
        SPREADSHEET_RANGE_INGREDIENTS,
    )
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Назад", callback_data="action_selection_menu")],
        ]
    )
    cocktail = {query.data: menu.get(query.data)}
    text = menu_dict_to_str(cocktail)
    file_path = f"{MEDIA_DIR}/{query.data}.jpg"
    file = None
    if os.path.exists(file_path):
        file = open(file_path, "rb")
    await update_message(query, buttons, text, parse_mode="MarkdownV2", media=file)


async def buttons_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    FUNCTIONS: Dict[str, Callable[[CallbackQuery, Optional[str]], Coroutine[Any, Any, None]]] = {
        "update_list": show_menu_list,
        "show_menu_list": show_menu_list,
        "action_selection_menu": show_menu,
    }
    chat = update.effective_chat
    await context.bot.send_chat_action(chat_id=chat.id, action="typing")
    query = update.callback_query
    await query.answer()
    if query.data in FUNCTIONS.keys():
        await FUNCTIONS[query.data](query)  # type: ignore
    else:
        cocktails_range = read_sheet(SERVICE, SPREADSHEET_ID, SPREADSHEET_RANGE_COCKTAILS).get("values")
        available_cocktails_range = read_sheet(SERVICE, SPREADSHEET_ID, SPREADSHEET_RANGE_AVAILABLE_COCKTAILS).get(
            "values"
        )
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
            await show_menu(query, "Коктейль закончился :(")
        else:
            await error(query)


def main() -> None:
    auth_token = os.getenv("TOKEN")
    application = Application.builder().token(auth_token).read_timeout(30).connect_timeout(30).build()
    application.add_handler(CallbackQueryHandler(buttons_handler))
    application.add_handler(CommandHandler("start", wake_up))
    application.run_polling(allowed_updates=Update.ALL_TYPES, timeout=30)


if __name__ == "__main__":
    main()
