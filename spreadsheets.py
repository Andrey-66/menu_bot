from google.oauth2.service_account import Credentials
from googleapiclient import discovery

from constants import GOOGLE_SCOPES, GOOGLE_CREDENTIALS_FILE, MENU_TITLE, COCKTAIL_SMILE
from utils import str_to_markdown


def google_auth():
    credentials = Credentials.from_service_account_file(
        filename=GOOGLE_CREDENTIALS_FILE, scopes=GOOGLE_SCOPES)
    service = discovery.build('sheets', 'v4', credentials=credentials)
    return service, credentials


def read_values(service, spreadsheet_id, recipe_range, ingredients_range):
    recipes = read_sheet(service, spreadsheet_id, recipe_range)
    ingredients = read_sheet(service, spreadsheet_id, ingredients_range)
    return range_to_str(recipes.get('values'), ingredients.get('values'))


def read_sheet(service, spreadsheet_id, sheet_range):
    request = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=sheet_range,
    )
    result = request.execute()
    return result


def range_to_str(recipes_range: list, ingredients_range: list) -> str:
    answer = '*'+MENU_TITLE+'*'
    menu = {}
    ingredients = {}

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

    for cocktail in menu.keys():
        answer += str_to_markdown(COCKTAIL_SMILE) + '*' + str_to_markdown(cocktail) + '*\n'
        for ingredient in menu.get(cocktail):
            answer += str_to_markdown('- ' + ingredient) + '\n'

    return answer
