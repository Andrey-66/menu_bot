from typing import Dict, List

from constants import COCKTAIL_SMILE
from logger import LOGGER
from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup


def str_to_markdown(string: str) -> str:
    string = string.replace("%", r"\%")
    string = string.replace("#", r"\#")
    string = string.replace("+", r"\+")
    string = string.replace("&", r"\&")
    string = string.replace("-", r"\-")
    string = string.replace(".", r"\.")
    LOGGER.debug(f"string: {string}")
    return string


def menu_dict_to_str(menu: Dict[str, List[str]], menu_title: str = "") -> str:
    answer = ""
    if menu_title != "":
        answer = "*" + menu_title + "*"
    for cocktail in menu.keys():
        answer += str_to_markdown(COCKTAIL_SMILE) + "*" + str_to_markdown(cocktail) + "*\n"
        for ingredient in menu.get(cocktail, []):
            answer += str_to_markdown("- " + ingredient) + "\n"
    LOGGER.debug(f"answer: {answer}")
    return answer


def range_to_dict(recipes_range, ingredients_range) -> Dict[str, List[str]]:
    ingredients = {}
    menu: Dict[str, List[str]] = {}
    for ingredient in ingredients_range:
        ingredients[ingredient[0]] = ingredient[3]

    for row in recipes_range:
        cocktail = row[0]
        ingredient = row[1]
        if not menu.get(cocktail):
            if ingredients.get(ingredient) == "нет":
                menu[cocktail] = [ingredient]
        else:
            menu[cocktail].append(ingredient)
    LOGGER.debug(f"menu: {menu}")
    return menu


def build_menu_buttons(menu: Dict[str, List[str]]) -> InlineKeyboardMarkup:
    buttons = []
    cocktails = list(menu.keys())
    for i in range(int(len(cocktails) / 2)):
        buttons.append(
            [
                InlineKeyboardButton(cocktails[i * 2], callback_data=cocktails[i * 2]),
                InlineKeyboardButton(cocktails[i * 2 + 1], callback_data=cocktails[i * 2 + 1]),
            ]
        )

    if len(cocktails) % 2 > 0:
        buttons.append(([InlineKeyboardButton(cocktails[-1], callback_data=cocktails[-1])]))
    buttons.append(
        [
            InlineKeyboardButton("Показать списком", callback_data="show_menu_list"),
            InlineKeyboardButton("Обновить", callback_data="action_selection_menu"),
        ]
    )
    LOGGER.debug(f"buttons: {buttons}")
    return InlineKeyboardMarkup(buttons)


async def update_message(
    query: CallbackQuery, buttons: InlineKeyboardMarkup, text: str, parse_mode=None, media=None
) -> None:
    if not query.message.text or media:
        await query.delete_message()
        if media:
            await query.get_bot().send_photo(
                chat_id=query.message.chat.id, photo=media, caption=text, reply_markup=buttons, parse_mode=parse_mode
            )
        else:
            await query.get_bot().send_message(
                chat_id=query.message.chat.id, text=text, reply_markup=buttons, parse_mode=parse_mode
            )
    else:
        LOGGER.debug(f"Пользователь {query.from_user.username} обновил меню")
        LOGGER.debug(f"query: {query.data}")
        LOGGER.debug(f"buttons: {buttons}")
        LOGGER.debug(f"text: {text}")
        LOGGER.debug(f"parse_mode: {parse_mode}")
        await update_message_text(query, buttons, text, parse_mode)


async def update_message_text(query: CallbackQuery, buttons: InlineKeyboardMarkup, text: str, parse_mode=None) -> None:
    if query.message.reply_markup == buttons and query.message.text == text:
        return
    await query.edit_message_text(text=text, reply_markup=buttons, parse_mode=parse_mode)
