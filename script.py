"""
Os management, helper function, extraction stuff
"""
import os
import extraction_file as ef
from extract_info import extract_name, check_empty_data
from clean_sheet import clean_year

def main():
    """
    Main file
    """
    statement = [f'statements/{file}' for file in os.listdir('statements/')]
    sorted_statement = sorted(statement,
                              key=lambda x: (int(x.split('_')[-1].split('.')[0]), int(x.split('_')[-2]))
                              )
    for file_name in sorted_statement:
        bank, month, year = extract_name(file_name.split('.')[0])

        statement = ef.FinanacialManager(bank, year, month, 'memo.json')
        data = statement.clean(file_name)
        if not check_empty_data(data):
            statement.tally_account(data)
            statement.update_sheets()

def clean_through():
    """
    Goes through all files and cleans anything that was unknown
    e.g. Adds colour and proper naming convention to columns
    """
    files = [f'finance/{file}' for file in os.listdir('finance/')]

    for year in files:
        clean_year(year)


if __name__ == "__main__":
    num = input("""
1. Main()
2. Clean_through()
""")
    match int(num):
        case 1:
            main()
        case 2:
            clean_through()
        case _:
            print("Nope")
