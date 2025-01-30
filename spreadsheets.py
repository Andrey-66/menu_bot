from typing import Any, Dict, Tuple

from constants import GOOGLE_CREDENTIALS_FILE, GOOGLE_SCOPES
from google.oauth2.service_account import Credentials
from google.protobuf.service import Service
from googleapiclient import discovery
from logger import LOGGER
from utils import range_to_dict


def google_auth() -> Tuple[Service, Credentials]:
    credentials = Credentials.from_service_account_file(filename=GOOGLE_CREDENTIALS_FILE, scopes=GOOGLE_SCOPES)
    service = discovery.build("sheets", "v4", credentials=credentials)
    LOGGER.info("Google Sheets API initialized")
    return service, credentials


def read_menu(service, spreadsheet_id: str, recipe_range: str, ingredients_range: str) -> Dict[str, list[str]]:
    recipes = read_sheet(service, spreadsheet_id, recipe_range)
    ingredients = read_sheet(service, spreadsheet_id, ingredients_range)
    LOGGER.debug(f"recipes: {recipes}")
    return range_to_dict(recipes.get("values"), ingredients.get("values"))


def read_sheet(service, spreadsheet_id: str, sheet_range: str) -> Dict[str, Any]:
    request = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range=sheet_range,
        )
    )
    result = request.execute()
    LOGGER.debug(f"result: {result}")
    return result
