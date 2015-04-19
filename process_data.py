#!/usr/bin/env python
import matplotlib.pyplot as plt
import xlrd
import csv

STARTING_MEDIAN_YEAR=1984
ENDING_MEDIAN_YEAR=2013
MEDIAN_INCOME_FILE='h08.xls'

STARTING_GDP_YEAR=1929
ENDING_GDP_YEAR=2014
GDP_FILE='download.csv'

def process_median_income():
    """
    Returns an assocation list with median-income by year; e.g.:

        [(1984, 22415.0),
         (1985, 23618.0),
         (1986, 24897.0),
         ...
        ]
    """
    workbook = xlrd.open_workbook(MEDIAN_INCOME_FILE)
    sheet = workbook.sheet_by_index(0)
    data_row = sheet.row(6)
    
    # Data row looks like
    # 
    #     [text:u'United States', number:51939.0, number:276.0, number:51017.0, number:209.0,
    # 
    # where the median income for each year is every other value; the years are in descending
    # order so the first median value corresponds to 2013 and the last median value corresponds
    # to 1983; in order to get the data we take out every other value
    yearly_data = [data_row[x+1].value for x in xrange(0, len(data_row)-1) if x % 2 == 0]
    
    # We create association list of the form [[year, median-income], ...] ordered
    # from lowest year to highest year
    return zip(range(STARTING_MEDIAN_YEAR, ENDING_MEDIAN_YEAR + 1), yearly_data[::-1]) 


def process_gdp():
    """
    """
    with open(GDP_FILE, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',') 
        current_line = None
        while True: 
            if current_line and current_line[0] == str(1):
                break
            current_line = csv_reader.next()

        # The data row is formatted: [<line_number>, <label>, <data0>, <data1>, ...]
        return zip(range(STARTING_GDP_YEAR, ENDING_GDP_YEAR + 1), map(lambda v: float(v), current_line[2:]))


def main():
    median_data = dict(process_median_income()) # create dict from assoc list
    gdp_data = dict(process_gdp())

    years = range(max(STARTING_MEDIAN_YEAR, STARTING_GDP_YEAR),
                    min(ENDING_MEDIAN_YEAR, ENDING_GDP_YEAR) + 1)
    years = range(1994, 2013 + 1)

    m_percentages = []
    g_percentages = []
    for year in years[1:]:
        m_percentages.append((median_data[year] - median_data[years[0]]) / median_data[years[0]])
        g_percentages.append((gdp_data[year] - gdp_data[years[0]]) / gdp_data[years[0]])
    
    plt.plot(years[1:], m_percentages)
    plt.plot(years[1:], g_percentages)
    plt.show()

if __name__ == '__main__':
    main()
