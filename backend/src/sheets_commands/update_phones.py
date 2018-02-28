from typing import Dict

from backend.src.google_apis import sheets_api


def update_all_phone_numbers() -> None:
    """
    Attempt to add missing phone numbers to roster.

    Do not modify if phone already exists.
    """
    spreadsheet = '1omms6ldwSZWgDXRf2HYDtGoCwzekfuSt7OAA8yVyRwY'
    asurite_to_phones = {'ecarell1': '925858', 'ecka13': '111'}
    update_roster_phone_numbers(spreadsheet_id=spreadsheet,
                                asurite_to_phones=asurite_to_phones,
                                overwrite=False)


def update_roster_phone_numbers(spreadsheet_id: str, *,
                                asurite_to_phones: Dict[str, str],
                                overwrite: bool = False) -> None:
    """
    Update roster's phone numbers if missing.
    """
    phone_column_index = sheets_api.get_column_numeric_index(spreadsheet_id, 'phone')
    phone_column_letter = sheets_api.get_column_letter_index(spreadsheet_id, 'phone')
    if phone_column_index is None:
        return
    all_data = sheets_api.get_values(spreadsheet_id, f'A2:{phone_column_letter}')
    asurite_index = 0
    if overwrite:
        updated_phones = [[asurite_to_phones.get(row[asurite_index], row[asurite_index])]  # if not found, keep original
                          for row in all_data]
    else:
        updated_phones = [[asurite_to_phones.get(row[asurite_index])
                           if len(row) < phone_column_index or not row[phone_column_index]  # only check if missing
                           else row[phone_column_index]]  # else use original phone
                          for row in all_data]
    sheets_api.update_values(spreadsheet_id, f'{phone_column_letter}2:{phone_column_letter}', updated_phones)
