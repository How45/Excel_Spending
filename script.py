"""
Os management, helper function, extraction stuff
"""
import os
import extraction_file as ef
from extract_info import extract_name, check_empty_data
from clean_sheet import clean_year

def create(dir_file: str, starting_amount: int) -> None:
    """
    Main file
    """
    statement_dir: list[str] = [file for file in os.listdir(f'{dir_file}\\statements\\')]

    sorted_statement: list[str] = sorted(statement_dir,
                              key=lambda x: (int(x.split('_')[-1].split('.')[0]), int(x.split('_')[-2]))
                              )

    for file_name in sorted_statement:
        bank, month, year = extract_name(file_name.split('.')[0])

        statement = ef.FinancialManager(bank, year, month, dir_file, starting_amount)

        clean_data = statement.clean(f'{dir_file}\\statements\\{file_name}')

        if not check_empty_data(clean_data):
            statement.tally_account(clean_data)
            statement.update_sheets()

def update(dir_file: str) -> None:
    """
    Goes through all files and cleans anything that was unknown
    e.g. Adds colour and proper naming convention to columns
    """
    current_path: str = f'{os.getcwd()}\\spreadsheets\\{dir_file}'
    files = [f'{current_path}\\finance\\{file}' for file in os.listdir(f'{dir_file}/finance/')]

    for year in files:
        clean_year(year)
