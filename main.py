import ticker
import stock_price
import financial_data

# #  for american fed data
# import pandas_datareader as web

# def fed_constant_maturity():
#     t10y2y = web.DataReader('T10Y2Y', 'fred', start='2002-01-01')
#     t10y3m = web.DataReader('T10Y3M', 'fred', start='2002-01-01')

#     rate_diff = pd.concat([t10y2y, t10y3m], axis=1)
#     rate_diff.columns = ['10Y-2Y', '10Y-3M']
#     print(rate_diff.tail())


# def setting_display():  # Setting for the display
#     InteractiveShell.ast_node_interactivity = "all"
#     pd.set_option('display.float_format', lambda x: '%.3f' % x)
#     pd.set_option('display.max_columns', None)


# setting_display()
# fed_constant_maturity()

def main():
    ticker
    stock_price
    financial_data


if __name__ == '__main__':
    main()
