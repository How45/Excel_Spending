"""
File to get statements to put them on spreadsheet
"""
import os
import json
from zipfile import BadZipfile
import pandas as pd
from openpyxl import load_workbook, Workbook
from openpyxl.cell.cell import Cell
from icecream import ic
from extract_info import get_privous_year, memo_extraction, last_row
from clean_sheet import clean_cells

STARTING_VALUE: int = 11774.72
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

                if colour == "ffffff":
                    print(f'❌ You need to add {type_memo} to json file')

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
            clean_cells(self.output_file, self.month, 0)

        # If year file exists
        elif os.path.exists(self.output_file):
            workbook = load_workbook(filename=self.output_file)
            sheets = workbook.sheetnames

            # Checking if month is in the year workbook
            if self.month in sheets:

                # Checks if that bank is already added
                if not self.check_existing_bank():
                    sheet = workbook[self.month]
                    last_row = sheet.max_row

                    with pd.ExcelWriter(self.output_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer: # pylint: disable=abstract-class-instantiated
                        df.to_excel(writer, sheet_name=self.month, startrow=last_row, index=False, header=False)

                    clean_cells(self.output_file, self.month, int(last_row))

                else:
                    print(f'❗️ {self.bank} exists already in that year')
                    print(f'❗️ {self.bank}_{self.month}_{self.year}, can be removed')

            # New month in year file
            else:
                with pd.ExcelWriter(self.output_file, engine='openpyxl', mode='a') as writer: # pylint: disable=abstract-class-instantiated
                    df.to_excel(writer, sheet_name=self.month, index=False)

                clean_cells(self.output_file, self.month, 0)
        else:
            raise ValueError('No files found')

    def update_sheets(self):
        """
        Checks and updates any needs in the workbook or in workbooks head of the one being created
        """

        files: list[str] = os.listdir(path='finance/')
        closest_month: int = None
        closest_year: int = None

        try:
            for file in files:
                file_year = file.split('.')[0]

                if int(file_year) >= int(self.year):
                    if closest_year is None or int(file_year) < closest_year:
                        closest_year = int(file_year)

            workbook = load_workbook(f'finance/{closest_year}.xlsx')
            sheet_names = workbook.sheetnames

            for sheet in sheet_names:
                if int(sheet) > int(self.month):
                    if closest_month is None or int(sheet) < closest_month:
                        closest_month = int(sheet)
            workbook.close()

            if closest_month and closest_year:
                self.update_first_line(closest_month, closest_year)
            else:
                print(f"❌ Nothing to update -> {self.month}/{self.year}")

        except (ValueError):
            print("❌ Nothing above it")

    def update_first_line(self, closest_month: int, closest_year: int) -> None:
        """
        Updates the closes workbook top row, linking to new last row
        """
        current_total_cell = self.get_last_total_cell()

        workbook = load_workbook(filename=f'finance/{closest_year}.xlsx')
        page_no: str = '0'+str(closest_month) if closest_month < 10 else str(closest_month)
        sheet = workbook[page_no]

        # If in the same year workbook, just reference sheet month
        if not current_total_cell[1]:
            function_total = f"=SUM(D2,{STARTING_VALUE})"

        elif current_total_cell[1] == f'finance/{closest_year}.xlsx':
            function_total = f"=SUM(D2,'{current_total_cell[2]}'!{current_total_cell[0].coordinate})"

        # If in diff year workbook, closes_year ahead of current_workbook needs to reference current_workbook
        else:
            path_year = os.path.abspath(current_total_cell[1]).replace("\\","/")
            function_total = f"=SUM(D2,'file:///[{path_year}]{current_total_cell[2]}'!{current_total_cell[0].coordinate})"

        sheet.cell(row=2,column=5).value = function_total
        workbook.save(f'finance/{self.year}.xlsx')
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
            cell_coordinate: str = "E2"

        # If refrencing another sheet or workbook
        # I don't believe we will need cell_value
        # Believe is only needed when no workbook has existed
        else:
            # cell_value = last_total_cell[0].value
            cell_value: int = 0
            cell_coordinate: str = last_total_cell[0].coordinate

        iteration: int = 0
        for amount, memo, colour, date in zip(amounts, memos, colours, dates):
            if iteration == 0:
                # If we are adding a bank in the same month. Iteration: 1 is skipped
                function_total, iteration = self.sum_function(last_total_cell[1], last_total_cell[2], iteration, cell_value, cell_coordinate)

            elif iteration == 1:
                # Current spending row + last total
                cell_coordinate = "E2"
                function_total = f"=SUM(D3,{cell_coordinate})"

            else:
                # Increase the cell E(n) to E(n+1)
                cell_coordinate = f"E{int(cell_coordinate[1:])+1}"
                # Current spending row + last total
                function_total = f"=SUM(D{int(cell_coordinate[1:])+1},{cell_coordinate})"

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
        year_before_dir: str = f'finance/{get_privous_year(self.year)}.xlsx'

        # This year
        if os.path.exists(self.output_file):
            workbook: Workbook = load_workbook(filename=self.output_file)
            sheets: list[str] = workbook.sheetnames

            # Current month
            if self.month in sheets:
                sheet = workbook[self.month]

                last_cell = last_row(sheet)
                workbook.close()
                return (last_cell,self.output_file, self.month)

            privious_month: str = '0'+str(int(self.month)-1) if int(self.month)-1 < 10 else str(int(self.month)-1)

            # Privious month
            if privious_month in sheets:
                sheet = workbook[privious_month]
            else:
                print('❗️ no privous month found')
                return (STARTING_VALUE, None, None)

            last_cell = last_row(sheet)
            workbook.close()
            return (last_cell, self.output_file, privious_month)

        # Last Year
        elif os.path.exists(year_before_dir):
            workbook = load_workbook(filename=year_before_dir)
            sheets = workbook.sheetnames

            try:
                sheet_str = sheets[-1]
                sheet = workbook[sheet_str]
                # Gets the last month in that year, returing last total of that month
                last_cell = last_row(sheet)
                workbook.close()
                return (last_cell, year_before_dir, sheet_str)
            except ValueError as val_error:
                print(f"❌ {val_error}")

        # None
        else:
            print('❗️ no privous year has been found')
            return (STARTING_VALUE, None, None)

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
            function_total = f'=SUM(D2,{cell_value})'

        # Needing to reference the total of the last_row of another sheet or workbook

        # Same Year
        elif last_year == self.output_file:
            # Same Month
            if last_month == self.month:
                # int(cell_coordinate[1])+1 : Getting the last known cell then +1 to get the correct row.
                function_total = f"=SUM(D{int(cell_coordinate[1:])+1},{cell_coordinate})"
                iteration += 1

            # Different Month in workbook
            # Function is the SUM of amount with the month.cell_of_last_total (LibreOffice)
            else:
                function_total = f"=SUM(D2,'{last_month}'!{cell_coordinate})"

        # Different Year (LibreOffice VERSION ONLY) path#$month.cell_of_last_total<----
        else:
            path_year = os.path.abspath(last_year).replace("\\","/")

            function_total = f"=SUM(D2,'file:///[{path_year}]{last_month}'!{cell_coordinate})"

        return function_total, iteration
