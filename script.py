"""
Os managment, helper function, extraction stuff
"""
import os
import extraction_file as ef
from extract_info import extract_name
from clean_sheet import clean_year

def main():
    """
    Main file
    """
    statement = [f'statements/{file}' for file in os.listdir('statements/')]
    for file_name in statement:
        # file_name = 'statements/TestA_11_2023.csv'
        bank, month, year = extract_name(file_name.split('.')[0])

        statement = ef.FinanacialManager(bank, year, month)
        data = statement.clean(file_name)
        statement.tally_account(data)
        # statement.update_sheets()

def clean_through():
    """
    Goes through all files and cleans anything that was unknown
    e.g. Adds colour and proper naming convention to columns
    """
    files = [f'finance/{file}' for file in os.listdir('finance/')]
    print(files)

    for year in files:
        clean_year(year)
        # | Work in progress |


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
