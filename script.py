"""
Os managment, helper function, extraction stuff
"""
import extraction_file as ef
from helper_function import extract_name
import os

def main():
    """
    Main file
    """
    for file_name in ['statements/Barclay_11_2023.csv',
                      'statements/Barclay_12_2023.csv',
                      'statements/TestA_11_2023.csv']:
        # file_name = 'statements/TestA_11_2023.csv'
        bank, month, year = extract_name(file_name.split('.')[0])

        statement = ef.FinanacialManager(bank, year, month)
        amount, memo, colours, dates = statement.clean(file_name)
        statement.tally_account(amount, memo, colours, dates)

def clean_through():
    """
    Goes through all files and cleans anything that was unknown
    e.g. Adds colour and proper naming convention to columns
    """
    path = 'finance/'
    files = os.listdir(path=path)

    for year in files:
        statement = ef.FinanacialManager(None, year.split('.')[0], None)

if __name__ == "__main__":
    main()
