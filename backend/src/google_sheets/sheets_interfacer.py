from typing import List

from backend.src.google_sheets import authentication


def get_values(spreadsheet_id: str, range_: str) -> List:
    """
    Query spreadsheet from provided range and return its values.
    """
    sheets_service = authentication.build_service()
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_).execute()
    return result.get('values', [])