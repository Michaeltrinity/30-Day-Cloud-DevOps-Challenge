import streamlit as st # type: ignore
import boto3
import pandas as pd # type: ignore
from io import StringIO

# Initialize boto3 S3 client
s3_client = boto3.client('s3')

# Function to read data from S3
def get_data_from_s3(bucket_name, file_name):
    try:
        # Fetching the file from S3 bucket
        obj = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        # Read the data into a string
        data = obj['Body'].read().decode('utf-8')
        # Convert the data into a pandas DataFrame
        return pd.read_csv(StringIO(data))
    except Exception as e:
        st.error(f"Error fetching data from S3: {e}")
        return None

# Streamlit UI
st.title('Weather Data from S3')

# Input fields
bucket_name = st.text_input('Enter S3 Bucket Name', 'weather-dashboard-dallastrinity85')
file_name = st.text_input('Enter File Name', 'weather-data.csv')  # Assuming CSV file

# Display the data if inputs are provided
if bucket_name and file_name:
    data = get_data_from_s3(bucket_name, file_name)
    if data is not None:
        st.write(f"Displaying weather data from S3 bucket: {bucket_name} - File: {file_name}")
        
        # Show data in a table format
        st.dataframe(data)
        
        # Ensure the columns are correctly formatted
        if 'City' in data.columns and 'Temperature' in data.columns:
            # Create a bar chart with City on the x-axis and Temperature on the y-axis
            st.bar_chart(data.set_index('City')['Temperature'])
        else:
            st.error("Missing 'City' or 'Temperature' columns in the data.")
