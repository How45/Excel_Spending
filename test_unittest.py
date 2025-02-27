"""
.
"""
import pandas as pd
import os
import unittest
import extract_info as extract
import extraction_file as ef

class TestExtractionFile(unittest.TestCase):
    """
    .
    """
    def test_get_last_total(self) -> None:
        """
        Test -> prints the last total from target month/year
        """
        pass

    def test_get_last_cell(self) -> None:
        """
        Test -> the function last cell of a finance statement. Should return amount
        """
        pass

    def test_new_anything(self) -> None:
        """
        Test -> very first statement added to finance
        """
        pass

    def test_order_statements(self) -> None:
        """
        Test -> prints order of statements by month and year
        """
        statement = [f'statements/{file}' for file in os.listdir('statements/')]
        sorted_files = sorted(statement,
                              key=lambda x: (int(x.split('_')[-1].split('.')[0]), int(x.split('_')[-2]))
                              )


    def test_missing_month(self) -> None:
        """
        Test -> when a new month is added, the closest statement it can update is the nearest month of the same year
        """
        for file_name in ['statements/FirstDirect_03_2024.csv', 'statements/Barclay_04_2024.csv',
                          'statements/FirstDirect_04_2024.csv']:

            bank, month, year = extract.extract_name(file_name.split('.')[0])

            statement = ef.FinancialManager(bank, year, month)
            data = statement.clean(file_name)

            if not extract.check_empty_data(data):
                statement.tally_account(data)

        # new month added in between to update next years
        file_name: str = 'statements/Barclay_03_2024.csv'
        bank, month, year = extract.extract_name(file_name.split('.')[0])

        statement = ef.FinancialManager(bank, year, month)
        data = statement.clean(file_name)

        if not extract.check_empty_data(data):
            statement.tally_account(data)
            statement.update_sheets()

    def test_missing_month_next_year(self):
        """
        Test -> when a new month is added, the closest statement it can update it next year
        """
        for file_name in ['statements/Barclay_11_2023.csv', 'statements/FirstDirect_11_2023.csv',
                          'statements/FirstDirect_12_2023.csv', 'statements/Barclay_01_2024.csv']:

            bank, month, year = extract.extract_name(file_name.split('.')[0])

            statement = ef.FinancialManager(bank, year, month)
            data = statement.clean(file_name)

            if not extract.check_empty_data(data):
                statement.tally_account(data)

        # new month added in between to update next years
        file_name: str = 'statements/Barclay_12_2023.csv'
        bank, month, year = extract.extract_name(file_name.split('.')[0])

        statement = ef.FinancialManager(bank, year, month)
        data = statement.clean(file_name)

        if not extract.check_empty_data(data):
            statement.tally_account(data)
            statement.update_sheets()

    def test_check_bank_exists(self):
        """
        Test -> If the bank that's being inputted into a existing month/year exists or not
        """
        file_name: str = 'statements/FirstDirect_06_2024.csv'
        bank, month, year = extract.extract_name(file_name.split('.')[0])
        statement = ef.FinancialManager(bank, year, month)

        df = pd.read_excel(f'finance/{year}.xlsx', sheet_name=month)
        unittest_check = bank in df['Bank'].values

        assert statement.check_existing_bank() == unittest_check, f'Bank values: {df['Bank'].values}'

    def test_read_all_files(self):
        """
        Test -> If all files are readable from pandas
        """
        statement = [f'statements/{file}' for file in os.listdir('statements/')]
        sorted_files = sorted(statement,
                              key=lambda x: (int(x.split('_')[-1].split('.')[0]), int(x.split('_')[-2]))
                              )
        for i in sorted_files:
            try:
                pd.read_csv(i)
                print(f'👉 Able to read file {i}')
            except pd.errors.ParserError as e:
                print(f"""❗️ {i} <--- File issue
Check lines of file: {e}
                    """)


if __name__ == '__main__':
    unittest.main()
