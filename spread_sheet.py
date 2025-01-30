"""
Class to manipulate the spread sheet for graph extraction
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates
class GraphData():
    """
    All graph function here MAYBE
    """
    def __init__(self, data) -> None:
        self.data = data

    def pie_expenses(self) -> None:
        """
        Pie chart of each categories expenses
        """
        sum_category = self.data.groupby('What?')['Income/Spending'].sum()

        unique_colours = self.data.groupby('What?')['Colour'].unique().tolist()
        colours = [list(map(int, item[0].split(','))) for item in unique_colours]
        colours = [(r/255, g/255, b/255) for r, g, b in colours]

        amounts = [x*-1 if x < 0 else x for x in sum_category]
        categories = list(sum_category.keys())

        plt.pie(np.array(amounts), labels=categories, startangle=90, colors=colours)
        plt.title('Expense Distribution')
        plt.show()

    def line_total(self) -> None:
        """
        Line Chart in the Change of the total
        """
        get_total = list(self.data['Total'])

        plt.plot(get_total,'b-.')
        plt.xticks([])
        plt.title('Change of total')
        plt.show()

    def category_line(self) -> None:
        """
        Categories expenses as line chart
        """
        unique_colours = self.data.groupby('What?')['Colour'].unique().tolist()
        colours = [list(map(int, item[0].split(','))) for item in unique_colours]
        colours = [(r/255, g/255, b/255) for r, g, b in colours]

        for index, x in enumerate(self.data['What?'].unique()):
            cat_ = self.data[self.data['What?'] == x]
            cat_total = []
            for range, spent in enumerate(cat_['Income/Spending']):
                if cat_total:
                    cat_total.append(cat_total[range-1]+spent)
                else:
                    cat_total.append(spent)
            plt.plot(cat_total, color=colours[index])
            plt.xticks([])
        plt.show()


def main():
    """
    Main function
    """
    year = '2023'
    df = pd.read_excel(f'finance/{year}.xlsx')
    gd = GraphData(df)
    # gd.pie_expenses()
    # gd.line_total()
    gd.category_line()

if __name__ == "__main__":
    main()
