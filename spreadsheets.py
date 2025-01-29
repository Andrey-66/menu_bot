from constants import GOOGLE_CREDENTIALS_FILE, GOOGLE_SCOPES
from google.oauth2.service_account import Credentials
from googleapiclient import discovery
from utils import range_to_dict


def google_auth():
    credentials = Credentials.from_service_account_file(
        filename=GOOGLE_CREDENTIALS_FILE, scopes=GOOGLE_SCOPES
    )
    service = discovery.build("sheets", "v4", credentials=credentials)
    return service, credentials


def read_menu(service, spreadsheet_id, recipe_range, ingredients_range):
    recipes = read_sheet(service, spreadsheet_id, recipe_range)
    ingredients = read_sheet(service, spreadsheet_id, ingredients_range)
    return range_to_dict(recipes.get("values"), ingredients.get("values"))


def read_cocktails_id(service, spreadsheet_id, cocktails_range):
    cocktails = read_sheet(service, spreadsheet_id, cocktails_range)
    answer = {}
    for row in cocktails:
        answer[row[0]] = row[1]
    return answer


def read_sheet(service, spreadsheet_id, sheet_range):
    request = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range=sheet_range,
        )
    )
    result = request.execute()
    return result
