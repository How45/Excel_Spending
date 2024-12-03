"""
Helper functions
"""
import os
import re
import pandas as pd

def last_row(sheet):
    """
    Gets last row of chosen sheet (e.g month) and year
    """
    for row in sheet.iter_rows(min_row=sheet.max_row, max_row=sheet.max_row,
                                           min_col= 5, max_col= 5, values_only=False):
        for cell in row:
            return cell

def extract_name(file: str) -> tuple[str, str, str]:
    """
    Extract name of file
    """
    names = file.split('_')
    bank, month, year = names[0].split('/')[1], names[1], names[2]
    return bank, month, year

def privous_year_from_self(year) -> list[str]:
    """
    Gets last known year from starting year
    """
    xlsx_files = os.listdir('finance/')

    closes_year = None
    for file in xlsx_files:
        file_year = int(file.split('.')[0])
        if file_year == int(year)-1:
            return file_year

        elif int(file.split('.')[0]) < int(year):
            if closest_year is None or file_year > closest_year:
                closest_year = file_year

    if closes_year is None:
        return 0
    return closes_year

def category_memos(memo_json: dict, key: str) -> tuple[str, str]:
    """
    Memos converted to catergories from the memo.json file (e.g. Food, Housing)

    Parameters:
    ----------
    memo_json : dict
        This is the memo.json file in that is opened and stored in a veriable
    key : str
        The key is the memo in the bank statement that needs to be matched with a category in the memo.json
    """

    for memo_category in memo_json:
        for m in memo_json[memo_category]['memos']:

            if bool(re.match(m,key,re.IGNORECASE)):
                return memo_category, memo_json[memo_category]['colour']
            if m.lower() in key.lower():
                return memo_category, memo_json[memo_category]['colour']

    return key, "ffffff" #ffffff

def check_empty_data(data: pd.DataFrame) -> bool:
    """
    Checks if dataframe is empty
    """
    if data.empty:
        print('❗️ Empty, nothing to add')
        return True
    return False

def closest_month_from_self(month: str, sheets:list[str]) -> str|None:
    """
    Finds the closest month from the starting month
    """
    closest_month: str = None
    for target_month in sheets:
        if int(month) < int(target_month):
            if not closest_month or int(target_month) < int(closest_month):
                closest_month = target_month
    return closest_month
