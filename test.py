"""
.
"""
import unittest
import helper_function as hf
import extraction_file as ef
from openpyxl import load_workbook

class TestExtractionFile(unittest.TestCase):
    """
    .
    """
    def get_last_total(self):
        """
        .
        """
        file_name = 'statements/FirstD_12_2023.csv'
        bank, month, year = hf.extract_name(file_name.split('.')[0])

        statement = ef.FinanacialManager(bank, year, month)
        print(statement.get_last_total())

    def get_last_cell(self):
        """
        .
        """
        workbook = load_workbook(filename='finance/2023.xlsx')
        print(workbook.sheetnames)
        sheet = workbook['11']

        for row in sheet.iter_rows(min_row=sheet.max_row-1, max_row=sheet.max_row-1, min_col= 5, max_col= 5, values_only=False):
            for cell in row:
                workbook.close()
                print(cell.coordinate) # String

if __name__ == '__main__':
    unittest.main()
