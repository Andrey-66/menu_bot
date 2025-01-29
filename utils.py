from typing import Dict, List

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from constants import COCKTAIL_SMILE


def str_to_markdown(string: str) -> str:
    string = string.replace('%', '\\%')
    string = string.replace('#', '\\#')
    string = string.replace('+', '\\+')
    string = string.replace('&', '\\&')
    string = string.replace('-', '\\-')
    string = string.replace('.', '\\.')
    return string


def menu_dict_to_str(menu: Dict[str, List[str]], menu_title: str = '') -> str:
    answer = ''
    if menu_title != '':
        answer = '*' + menu_title + '*'
    for cocktail in menu.keys():
        answer += str_to_markdown(COCKTAIL_SMILE) + '*' + str_to_markdown(cocktail) + '*\n'
        for ingredient in menu.get(cocktail):
            answer += str_to_markdown('- ' + ingredient) + '\n'
    return answer


def range_to_dict(recipes_range: list, ingredients_range: list) -> Dict[str, List[str]]:
    ingredients = {}
    menu = {}
    for ingredient in ingredients_range:
        ingredients[ingredient[0]] = ingredient[3]

    for row in recipes_range:
        cocktail = row[0]
        ingredient = row[1]
        if not menu.get(cocktail):
            if ingredients.get(ingredient) == 'нет':
                menu[cocktail] = [ingredient]
        else:
            menu[cocktail].append(ingredient)
    return menu


def build_menu_buttons(menu: Dict[str, List[str]]) -> InlineKeyboardMarkup:
    buttons = []
    cocktails = list(menu.keys())
    for i in range(int(len(cocktails) / 2)):
        buttons.append([InlineKeyboardButton(cocktails[i * 2], callback_data=cocktails[i * 2]),
                        InlineKeyboardButton(cocktails[i * 2 + 1], callback_data=cocktails[i * 2 + 1])])
    if len(cocktails) % 2 > 0:
        buttons.append(([InlineKeyboardButton(cocktails[-1], callback_data=cocktails[-1])]))
    buttons.append([InlineKeyboardButton('Показать списком', callback_data='show_menu_list'),
                    InlineKeyboardButton('Обновить', callback_data='action_selection_menu')])
    return InlineKeyboardMarkup(buttons)


async def update_message(query: CallbackQuery, buttons: InlineKeyboardMarkup, text: str, parse_mode=None) -> None:
    if query.message.reply_markup == buttons and query.message.text == text:
        return
    if parse_mode:
        await query.edit_message_text(
            text=text,
            reply_markup=buttons,
            parse_mode=parse_mode
        )
    else:
        await query.edit_message_text(
            text=text,
            reply_markup=buttons
        )


if __name__ == "__main__":
    build_menu_buttons({'Пабло Эскобар': ['Текила', 'Сироп кокос', 'Лимонный сок', 'Сок грейпфрут', 'Сок ананас'],
                        'Пабло Эскобар1': ['Текила', 'Сироп кокос', 'Лимонный сок', 'Сок грейпфрут', 'Сок ананас'],
                        'Пабло Эскобар2': ['Текила', 'Сироп кокос', 'Лимонный сок', 'Сок грейпфрут', 'Сок ананас']})
