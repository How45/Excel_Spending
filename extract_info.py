"""
Helper functions
"""
import os
import re

def extract_name(file: str) -> tuple[str, str, str]:
    """
    Extract name of file
    """
    names = file.split('_')
    bank, month, year = names[0].split('/')[1], names[1], names[2]
    return bank, month, year

def get_privous_year(year) -> list[str]:
    """
    Gets last known year before
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

def memo_extraction(memo_operations: dict, key: str) -> tuple[str, str]:
    """
    Memos that should be in sheets converted to simply categories (e.g. Food, Housing)

    Parameters:
    ----------
    memo_operations : dict
        This is the memo.json file in that is opened and stored in a veriable
    key : str
        The key is the memo in the bank statement that needs to be matched with a category in the memo.json
    """
    # Goes through memo.json file to match memo to
    # simplified naming scheme

    for memo_naming in memo_operations:
        for m in memo_operations[memo_naming]['memos']:
            try:
                if bool(re.match(m.lower(),key.lower())):
                    return memo_naming, memo_operations[memo_naming]['colour']
            except re.error:
                if m.lower() in key.lower():
                    return memo_naming, memo_operations[memo_naming]['colour']
    # If memo is not find in JSON file
    return key, "ffffff" #ffffff
