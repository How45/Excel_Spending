"""
Helper functions
"""
import os

def extract_name(file: str) -> tuple[str, str, str]:
    """
    Extract name of file
    """
    names = file.split('_')
    bank, month, year = names[0].split('/')[1], names[1], names[2]
    return bank, month, year

def last_year(year) -> list[str]:
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

def memo_extraction(memo_operations, key: str) -> tuple[str, list[int]]:
    """
    Memos that should be in sheets converted to simply categories (e.g. Food, Housing)
    """
    # Goes through memo.json file to match memo to
    # simplified naming scheme

    for memo_naming in memo_operations:
        for m in memo_operations[memo_naming]['memos']:
            if m.lower() in key.lower():
                return memo_naming, memo_operations[memo_naming]['colour']
    # If memo is not find in JSON file
    return key, [255,255,255]

def rgb_to_rbga(rgb: list[int]) -> str:
    """
    Convert an RGB list to a RGBa string
    """
    r,g,b = rgb[0], rgb[1], rgb[2]
    return  f'{r:02x}{g:02x}{b:02x}'
