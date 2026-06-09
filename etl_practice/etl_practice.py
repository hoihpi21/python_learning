import pandas as pd 
import glob 
import xml.etree.ElementTree as ET 
from datetime import datetime 

log_file = 'log_file.txt'
target_file = 'transformed_data.csv'

# Extract Data
def extract_csv(file):
    df = pd.read_csv(file)
    return df 

def extract_json(file):
    df = pd.read_json(file, lines=True)
    return df 

def extract_xml(file):
    df = pd.DataFrame(columns=['car_model', 'year_of_manufacture', 'price', 'fuel'])
    tree = ET.parse(file)
    root = tree.getroot()
    for row in root:
        car_model = row.find('car_model').text
        year_of_manufacture = row.find('year_of_manufacture').text
        price = float(row.find('price').text)
        fuel = row.find('fuel').text
        df = pd.concat([df, pd.DataFrame([{'car_model':car_model, 'year_of_manufacture':year_of_manufacture, 'price':price, 'fuel':fuel}])])
    return df

def extract():
    extracted_data = pd.DataFrame(columns=['car_model','year_of_manufacture', 'price', 'fuel'])

    for csvfile in glob.glob("*.csv"):
        if csvfile != target_file:
            extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_csv(csvfile))])
    
    for jsonfile in glob.glob("*.json"):
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_json(jsonfile))])

    for xmlfile in glob.glob("*.xml"):
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_xml(xmlfile))])
    
    return extracted_data


# Transform Data 
def transform(data):
    data['price'] = round(data.price, 2)
    return data 

# Load Data
def load_data(target_file, transformed_data):
    transformed_data.to_csv(target_file)

def log(message):
    timestamp_format = '%Y-%m-%d-%H:%M%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(log_file, 'a') as f:
        f.write(timestamp + ',' + message + '\n')

log("ETL Job Processing ...")
extracted_data = extract()
transformed_data = transform(extracted_data)
print(transformed_data)
load_data(target_file, transformed_data)
log("ETL Job Finished!")