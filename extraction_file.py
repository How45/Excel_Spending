"""
File to get statements to put them on spreadsheet
"""
import os
import json
from zipfile import BadZipfile
import pandas as pd
from openpyxl import load_workbook
from openpyxl.cell.cell import Cell
from openpyxl.styles import PatternFill, Font, Color, Alignment
from icecream import ic
from helper_function import get_privous_year, memo_extraction, rgb_to_rbga
class FinanacialManager:
    """
    Deals with cleaning of statements and puts them in sheets
    """
    def __init__(self, bank, year, month):
        self.bank:str = bank
        self.year:str = year
        self.month:str = month
        self.output_file:str = f'finance/{year}.xlsx' # Where records are kept

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
        last_total_cell = self.get_last_total_cell()

        return self.to_dataframe(amounts, memos, last_total_cell, colours, dates)

    def tally_account(self, df: pd.DataFrame) -> None:
        """
        Adds either a new year file or a new month sheet to the year
        """
        # Checks if a year file has been created
        if not os.path.exists(self.output_file):
            df.to_excel(self.output_file, sheet_name=self.month, index=False)
            # setting row to start at 0
            self.clean_cells(df, 0)

        # If year file exists
        elif os.path.exists(self.output_file):
            # Loads workbook and gets the lists of sheets name
            workbook = load_workbook(filename=self.output_file)
            sheets = workbook.sheetnames

            # Checking if month is in the year workbook
            if self.month in sheets:

                # Checks if that bank is already added
                if not self.check_existing_bank():
                    # Adding Data to existing month sheet
                    sheet = workbook[self.month]
                    # Adding to the bottom of the sheet
                    last_row = sheet.max_row

                    # Getting row of dataframe (overlay at end of the row), workbook auto-closes
                    with pd.ExcelWriter(self.output_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer: # pylint: disable=abstract-class-instantiated
                        df.to_excel(writer, sheet_name=self.month, startrow=last_row, index=False, header=False)

                    # Set all to the colour
                    self.clean_cells(df, int(last_row))
                else:
                    # Skips the adding of already exiting bank
                    print(f'{self.bank} exists already in that year')
                    print(f'{self.bank}_{self.month}_{self.year}, can be removed')

            # New month in year file
            else:
                # Workbook auto closes
                with pd.ExcelWriter(self.output_file, engine='openpyxl', mode='a') as writer: # pylint: disable=abstract-class-instantiated
                    df.to_excel(writer, sheet_name=self.month, index=False)

                # Set all to the colour
                self.clean_cells(df, 0)
        else:
            raise ValueError('No files found')

    def update_sheets(self):
        """
        Checks and updates any needs in the workbook or in workbooks head of the one being created
        """

        files = os.listdir(path='finance/')
        closes_month, closes_year = None, None

        try:
            for file in files:
                file_year = file.split('.')[0]
                if int(file_year) >= int(self.year):
                    if closes_year is None or int(file_year) < closes_year:
                        closes_year = int(file_year)

            workbook = load_workbook(f'finance/{closes_year}.xlsx')
            sheet_names = workbook.sheetnames
            for sheet in sheet_names:
                if int(sheet) > int(self.month):
                    if closes_month is None or int(sheet) < closes_month:
                        closes_month = int(sheet)

            workbook.close()
            self.update_first_line(closes_year,closes_month)
        except (ValueError, BadZipfile):
            print("Nothing above it")

    def update_first_line(self, closes_year,closes_month) -> None:
        """
        Updates the closes workbook top row, linking to new last row
        """
        current_total_cell = self.get_last_total_cell()

        workbook = load_workbook(filename=f'finance/{closes_year}.xlsx')
        sheet = workbook[str(closes_month)]

        # If in the same year workbook, just reference sheet month
        if current_total_cell[1] == f'finance/{closes_year}.xlsx':
            function_total = f"=SUM(D2,{current_total_cell[2]}!{current_total_cell[0].coordinate})"

        # If in diff year workbook, closes_year ahead of current_workbook needs to reference current_workbook
        else:
            function_total = f"=SUM(D2,[{os.path.abspath(current_total_cell[1])}]{current_total_cell[2]}!{current_total_cell[0].coordinate})"

        sheet.cell(row=2,column=5,value=function_total)
        workbook.close()

    def check_existing_bank(self):
        """
        Checks if theres already the name of the bank in the month of that yearg
        """
        df = pd.read_excel(self.output_file)
        return self.bank in df['Bank'].values

    def to_dataframe(self, amounts: list[int], memos: list[str],
                  last_total_cell: tuple[Cell|None, str|None, str|None],
                  colours: list[int], dates: list[str]) -> pd.DataFrame:
        """
        Creates dataframe to a new sheet
        """
        df = pd.DataFrame()
        # If the very first file is created, using default starting value
        if last_total_cell[1] is None:
            cell_value: int = last_total_cell[0]
            cell_coordinate: str = 'E2'

        # If refrencing another sheet or workbook
        # I don't believe we will need cell_value
        # Believe is only needed when no workbook has existed
        else:
            # cell_value = last_total_cell[0].value
            cell_value = 0
            cell_coordinate: str = last_total_cell[0].coordinate

        iteration = 0
        for amount, memo, colour, date in zip(amounts, memos, colours, dates):
            if iteration == 0:
                # If we are adding a bank in the same month. Iteration: 1 is skipped
                function_total, iteration = self.sum_function(last_total_cell[1], last_total_cell[2], iteration, cell_value, cell_coordinate)

            elif iteration == 1:
                # Current spending row + last total
                cell_coordinate = 'E2'
                function_total = f'=SUM(D3,{cell_coordinate})'

            else:
                # Increase the cell E(n) to E(n+1)
                cell_coordinate = f'E{int(cell_coordinate[1:])+1}'
                # Current spending row + last total
                function_total = f'=SUM(D{int(cell_coordinate[1:])+1},{cell_coordinate})'

            row = {"Date": date,
                    "Colour": colour,
                    "What?": memo,
                    "Income/Spending": amount,
                    "Total": function_total,
                    "Bank": self.bank}
            df = df._append(row, ignore_index=True)
            iteration += 1
        return df

    def get_last_total_cell(self) -> tuple[Cell|None, str|None, str|None]:
        """
        Retrieves last total from file (checks current year or previous year)
        """
        # If the year before exits
        year_before = f'finance/{get_privous_year(self.year)}.xlsx'

        # If year exists
        if os.path.exists(self.output_file):
            workbook = load_workbook(filename=self.output_file)
            sheets = workbook.sheetnames

            if self.month in sheets:  # gets current month
                sheet = workbook[self.month]
                # Gets the last row of the sheet.
                # max.row-1, as the file leaves a bank row at the end
                for row in sheet.iter_rows(min_row=sheet.max_row, max_row=sheet.max_row,
                                           min_col= 5, max_col= 5, values_only=False):
                    # Reading content of cell
                    for cell in row:
                        workbook.close()
                        return (cell, self.output_file, self.month)

            # # List of all sheets of workbook, then loads sheet
            sheet_str = sheets[-1]
            sheet = workbook[sheet_str]
            # Gets the last month in that year, returing last total of that month
            for row in sheet.iter_rows(min_row=sheet.max_row, max_row=sheet.max_row,
                                           min_col= 5, max_col= 5, values_only=False):
                # Reading content of cell
                for cell in row:
                    workbook.close()
                    return (cell, self.output_file, sheet_str)

        # Gets the last month of the year before
        elif os.path.exists(year_before):
            workbook = load_workbook(filename=year_before)
            sheets = workbook.sheetnames

            try:
                # List of all sheets of workbook, then loads sheet
                sheet_str = sheets[-1]
                sheet = workbook[sheet_str]
                # Gets the last month in that year, returing last total of that month
                for row in sheet.iter_rows(min_row=sheet.max_row-1, max_row=sheet.max_row-1,
                                            min_col= 5, max_col= 5, values_only=False):
                    # Reading content of cell
                    for cell in row:
                        workbook.close()
                        return (cell, year_before, sheet_str)
            except ValueError as val_error:
                print(val_error)

        else: # For very first statement
            print('no privous month or year has been found')
            return [1000, None, None]
            # raise ValueError('Error: no privous month or year has been found')

    def clean_cells(self, data: pd.DataFrame, given_idx: int) -> None:
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
                # If starting index 0 (+2) if its a continuation of a line +1
                if given_idx:
                    cell = sheet[idx+given_idx+1][1]

                    cell_spending = sheet[idx+given_idx+1][3]
                    cell_total = sheet[idx+given_idx+1][4]
                else:
                    cell = sheet[idx+given_idx+2][1]

                    cell_spending = sheet[idx+given_idx+2][3]
                    cell_total = sheet[idx+given_idx+2][4]

                cell.fill = fill
                cell.value = None

                # Setting to currency format
                cell_spending.number_format =  '£#,##0.00'
                cell_total.number_format = '£#,##0.00'
                if cell_spending.value < 0:
                    cell_spending.font = Font(color="ff0000", name='Calibri')
                cell_spending.alignment = Alignment(horizontal='center')
                cell_total.alignment = Alignment(horizontal='center')

        # Save the workbook
        workbook.save(self.output_file)
        workbook.close()

    def sum_function(self, last_year: str|None, last_month: str|None, iteration: int,
                     cell_value: int, cell_coordinate: str) -> str:
        """
        Computes the last total for the first row of the sheet.

        The function determines how the first row should derive the last total, either by:
        - Continuing from the same month
        - Fetching the total from another sheet
        - Fetching the total from another workbook

        Parameters:
        ----------
        last_year : str|None
            The privious year gotten from the last_total_cell or None
        last_month : str
            The privious month gotten from the last_total_cell
        iteration : int
            The row number for the current Income/Spending being processed.
            Value will be +2 as excel starts on base 1 and we are skipping the header row
        cell_value : int
            A starting value or 0 if no value is provided.
        cell_coordinate : str
            The cell coordinate indicating where the total is located (e.g., 'E2', 'E36').
        """
        # First time creating a worbook ever
        if last_year is None:
            function_total = f'=SUM(D{2},{cell_value})'

        # Needing to reference the total of the last_row of another sheet or workbook

        # Same Year
        elif last_year == self.output_file:
            # Same Month
            if last_month == self.month:
                # int(cell_coordinate[1])+1 : Getting the last known cell then +1 to get the correct row.
                function_total = f'=SUM(D{int(cell_coordinate[1:])+1},{cell_coordinate})'
                iteration += 1

            # Different Month in workbook
            # Function is the SUM of amount with the month.cell_of_last_total (LibreOffice)
            else:
                function_total = f"=SUM(D{2},'{last_month}'.{cell_coordinate})"

        # Different Year (LibreOffice VERSION ONLY) path#$month.cell_of_last_total<----
        else:
            function_total = f"=SUM(D{2},{os.path.abspath(last_year)}#$'{last_month}'.{cell_coordinate})"
        return function_total, iteration
