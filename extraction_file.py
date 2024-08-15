"""
File to get statements to put them on spreadsheet
"""
import os
import json
import pandas as pd
from numpy import int64
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from helper_function import last_year, memo_extraction, rgb_to_rbga

class FinanacialManager:
    """
    Deals with cleaning of statements and puts them in sheets
    """
    def __init__(self, bank, year, month):
        self.bank = bank
        self.year = year
        self.month = month
        self.output_file = f'finance/{year}.xlsx' # Where records are kept

    # Needs to be re-done (normalise so it can gt all data)
    def clean(self, statement: str) -> pd.DataFrame:
        """
        Cleans bank statement
        """
        # Loads the json file to extract the needed data for cleaning of statement
        with open('banks.json', 'r', encoding='utf-8') as f:
            bank_operations = json.load(f)

        # Checks bank
        bank_info = bank_operations.get(self.bank)
        if bank_info is None:
            raise KeyError(f'No banks under {self.bank} found')

        data = pd.read_csv(statement)

        # Barclays (doesn't have null values, I think)v
        amount = data[bank_info['amount_column']].tolist()
        date = data[bank_info['Dates']].tolist()

        memo = [name.replace('\t', '').replace(' ', '')
                for name in data[bank_info['memo_column']].tolist()]

        # Removes any amount and memo thats in the remove_memo (sync indexs)
        with open('memo.json', 'r', encoding='utf-8') as f:
            memo_operations = json.load(f)

        amounts, memos, colours, dates = [], [], [], []
        for index, key in enumerate(memo):
            # Checks if item is not in remove_memo
            if key.lower() not in [x.lower() for x in bank_info['remove_memo']]:
                type_memo, colour = memo_extraction(memo_operations, key)
                if colour == [255,255,255]:
                    # Rise any non memo.json naming
                    print(f'You need to add {type_memo} to json file')

                # Keeps amount same index as coresponding memo
                dates.append(date[index])
                memos.append(type_memo)
                colours.append(colour)
                amounts.append(amount[index])

        # gets the last known total
        last_total = self.get_last_total()

        return self.to_dataframe(amounts, memos, last_total, colours, dates)

    def tally_account(self, df: pd.DataFrame) -> None:
        """
        Adds either a new year file or a new month sheet to the year
        """
        # Checks if a year file has been created
        if not os.path.exists(self.output_file):
            df.to_excel(self.output_file, sheet_name=self.month, index=False)
            # setting row to start at 0
            self.set_colour_row(df, 0)

        # If year file exists
        elif os.path.exists(self.output_file):
            # Loads workbook and gets the lists of sheets name
            workbook = load_workbook(filename=self.output_file)
            sheet_list = workbook.sheetnames

            # Checking if month is in the year workbook
            if self.month in sheet_list:

                # Checks if that bank is already added
                if not self.check_existing_bank():
                    # Adding Data to existing month sheet
                    sheet = workbook[self.month]
                    # Adding to the bottom of the sheet
                    last_row = sheet.max_row

                    # Getting row of dataframe (overlay at end of the row), workbook auto-closes
                    with pd.ExcelWriter(self.output_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                        df.to_excel(writer, sheet_name=self.month, startrow=last_row, index=False, header=False)

                    # Set all to the colour
                    self.set_colour_row(df, int(last_row))
                else:
                    # Skips the adding of already exiting bank
                    print(f'{self.bank} exists already in that year')
                    print(f'{self.bank}_{self.month}_{self.year}, can be removed')

            # New month in year file
            else:
                # Workbook auto closes
                with pd.ExcelWriter(self.output_file, engine='openpyxl', mode='a') as writer:
                    df.to_excel(writer, sheet_name=self.month, index=False)

                # Set all to the colour
                self.set_colour_row(df, 0)
        else:
            raise ValueError('No files found')

    def check_existing_bank(self):
        """
        Checks if theres already the name of the bank in the month of that year
        """
        df = pd.read_excel(self.output_file)
        return self.bank in df['Bank'].values

    def to_dataframe(self, amounts: list[int], memos: list[str],
                  last_total: int, colours: list[int], dates: list[str]) -> pd.DataFrame:
        """
        Creates dataframe to a new sheet
        """

        df = pd.DataFrame()
        for amount, memo, colour, date in zip(amounts, memos, colours, dates):
            last_total += amount
            row = {"Date": date,
                    "Colour": colour,
                    "What?": memo,
                    "Income/Spending": amount,
                    "Total": last_total,
                    "Bank": self.bank}
            df = df._append(row, ignore_index=True)
        return df

    def get_last_total(self) -> int64:
        """
        Retrieves last total from file (checks current year or previous year)
        """
        # If the year before exits
        year_before = f'finance/{last_year(self.year)}.xlsx'

        # If year exists
        if os.path.exists(self.output_file):
            workbook = load_workbook(filename=self.output_file)
            sheets = workbook.sheetnames

            if self.month in sheets:  # gets current month
                sheet = workbook[self.month]
                # Gets the last row of the sheet.
                # max.row-1, as the file leaves a bank row at the end
                for row in sheet.iter_rows(min_row=sheet.max_row-1, max_row=sheet.max_row-1,
                                           min_col= 5, max_col= 5, values_only=False):
                    for cell in row:
                        workbook.close()
                        return cell.coordinate

            # Gets last month avaiable
            sheet = sheets[-1]
            # Gets the last month in that year, returing last total of that month
            for row in sheet.iter_rows(min_row=sheet.max_row-1, max_row=sheet.max_row-1,
                                           min_col= 5, max_col= 5, values_only=False):
                for cell in row:
                    workbook.close()
                    return cell.coordinate

        # Gets the last month of the year before
        elif os.path.exists(year_before):
            workbook = load_workbook(filename=year_before)
            sheets = workbook.sheetnames

            try:
                # Gets last month avaiable
                sheet = sheets[-1]
                # Gets the last month in that year, returing last total of that month
                for row in sheet.iter_rows(min_row=sheet.max_row-1, max_row=sheet.max_row-1,
                                            min_col= 5, max_col= 5, values_only=False):
                    for cell in row:
                        workbook.close()
                        return cell.coordinate
            except ValueError as val_error:
                print(val_error)

        else: # For very first statement
            print('no privous month or year has been found')
            return 1000
            # raise ValueError('Error: no privous month or year has been found')

    def set_colour_row(self, data: pd.DataFrame, given_idx: int) -> None:
        """
        Goes through month to change RBG to fill colour
        """
        workbook = load_workbook(filename=self.output_file)
        sheet = workbook[self.month]
        for idx, row in data.iterrows():
            rgb = row['Colour']
            if rgb:
                hex_color = rgb_to_rbga(rgb)
                fill = PatternFill(start_color=hex_color, end_color=hex_color, fill_type="solid")

                # Excel starts on indexed-1 and pandas is indexed-0 (Also header on the first line)
                # Fills only Column B
                # Removing Colour list
                cell = sheet[idx+given_idx+2][1]
                cell.fill = fill
                cell.value = None
        # Save the workbook
        workbook.save(self.output_file)
        workbook.close()
