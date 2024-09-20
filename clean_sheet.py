"""
openpyxl : workbook, PattenFill, Font, Alignment
"""
from icecream import ic
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Alignment


def clean_cells(output_file:str, month:str, given_idx: int) -> None:
    """
    Cleans each row of workbook sheet.

    The function will iterate though each row of the workbook sheet;
    - Change width of column
    - Add colour to category
    - Convert all currancy to £, at 2 decimal place.

    Parameters:
    ----------
    output_file : str
    File location. This should be finance/year.xlsx
    month : str
    The month its searching in the workbook. i.e 1 (Jan) or 2 (Feb)
    data : pd.DataFrame
    This is the pandas dataframe of all the colour, so it can fill into the sheet
    given_idx : int
    Where to start in the spreadsheet, either at the end or could be at the start
    """
    workbook = load_workbook(filename=output_file)
    sheet = workbook[month]

    sheet.column_dimensions['A'].width = 10.50 # 2.10
    sheet.column_dimensions['C'].width = 13.05 # 2.61
    sheet.column_dimensions['D'].width = 18.10 # 3.62
    sheet.column_dimensions['E'].width = 12.10 # 2.42

    # If starting index 0 (+2) if its a continuation of a line +1
    if given_idx:
        given_idx += 1
    else:
        given_idx += 2

    for idx, row in enumerate(sheet.iter_rows(min_row=given_idx, values_only=True)):
        hex_color = row[1]
        idx_row = given_idx+idx

        if hex_color:
            fill = PatternFill(start_color=hex_color, end_color=hex_color, fill_type="solid")

            # Excel starts on indexed-1 and pandas is indexed-0 (Also header on the first line)
            # Fills only Column B
            # Removing Colour list
            cell = sheet[idx_row][1]
            cell_spending = sheet[idx_row][3]
            cell_total = sheet[idx_row][4]

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
    workbook.save(output_file)
    workbook.close()
