"""
Os management, helper function, extraction stuff
"""
import os
import extraction_file as ef
from extract_info import extract_name, check_empty_data
from clean_sheet import clean_year

def create_file(dir_file: str) -> None:
    """
    Main file
    """

    statement: list[str] = [file for file in os.listdir(f'{dir_file}\\statements\\')]

    sorted_statement: list[str] = sorted(statement,
                              key=lambda x: (int(x.split('_')[-1].split('.')[0]), int(x.split('_')[-2]))
                              )

    for file_name in sorted_statement:
        bank, month, year = extract_name(file_name.split('.')[0])
        statement = ef.FinancialManager(bank, year, month, 'memo.json', dir_file)
        data = statement.clean(file_name)
        if not check_empty_data(data):
            statement.tally_account(data)
            statement.update_sheets()

def clean_through(dir_file: str) -> None:
    """
    Goes through all files and cleans anything that was unknown
    e.g. Adds colour and proper naming convention to columns
    """
    files = [f'{dir_file}/finance/{file}' for file in os.listdir(f'{dir_file}/finance/')]

    for year in files:
        clean_year(year)
