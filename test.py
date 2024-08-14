"""
.
"""
import unittest
import helper_function as hf
import extraction_file as ef

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

    def years_file(self):
        print(f'finance/{int(hf.get_year_list()[-1])}.xlsx')

if __name__ == '__main__':
    unittest.main()
