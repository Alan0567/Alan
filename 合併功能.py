import pandas as pd
excel_data_df1 = pd.read_excel('1.xlsx', sheet_name='地址詳情')
excel_data_df = pd.read_excel('1.xlsx', sheet_name='Total')
join = pd.merge(excel_data_df1,excel_data_df, on ='地址')
join.to_excel (r'/Users/alan/Desktop/Dataset.xlsx', index = False, header=True)