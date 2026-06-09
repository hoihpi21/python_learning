import pandas as pd
import sqlite3 

conn = sqlite3.connect("Staff.db")

table_name = "Departments"
attribute_list = ['DEPT_ID', 'DEP_NAME', 'MANAGER_ID', 'LOC_ID']

file_path = './INSTRUCTOR.csv'
df = pd.read_csv(file_path, names = attribute_list)

df.to_sql(table_name, conn, if_exists='replace', index=False)
print("Table is ready.")

query_statement = f"SELECT * FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_output)
print(query_statement)
print('\n')

query_statement = f"SELECT COUNT(*) FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_output)
print(query_statement)

data_dict = {'DEPT_ID': ['Department ID'],
            'DEP_NAME': ['Department Name'],
            'MANAGER_ID': ['Manager ID'],
            'LOC_ID': ['Location ID']}

data_append = pd.DataFrame(data_dict)
conn.close()