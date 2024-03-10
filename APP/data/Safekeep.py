import sklearn; print(sklearn.__version__)
import streamlit as st
import numpy as np
import pandas as pd
import time
from data.air_quality_data import get_air_quality_data
from data.get_city_data import get_city_data
from data.make_predictions_for_df import make_predictions_for_df
import requests
from joblib import load


custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap');
.title {
    font-family: 'Barlow', sans-serif;
    text-align: center;
}
body {
    font-family: 'Roboto', sans-serif;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown('<h1 class="title">Welcome to the Jungle</h1>', unsafe_allow_html=True)

def fetch_data(city):
    # Fetch air quality data
    air_quality_df = get_air_quality_data(city)

    # Fetch city data
    city_df = get_city_data(city)

    # Create a common key for joining
    air_quality_df['key'] = 1
    city_df['key'] = 1

    # Join the dataframes
    merged_df = pd.merge(city_df,air_quality_df,on='key')

    # Drop the created key
    merged_df.drop(columns=['key'], inplace=True)

    # Calculate average values for numeric columns
    numeric_columns = merged_df.select_dtypes(include=['number']).columns
    avg_row = merged_df[numeric_columns].mean()

    return merged_df, avg_row

# Function to make predictions
def make_predictions(city, num_predictions):
    # Fetch data for the city and calculate average values
    merged_df, avg_row = fetch_data(city)

    # Make predictions using the provided function
    predictions_df = make_predictions_for_df(merged_df, num_predictions)

    return predictions_df, avg_row

# Streamlit app
def main():
    st.title('Air Quality, City Data, and Predictions App')

    # Get city input from the user
    city_input = st.text_input('Enter a city name:', 'New York')

    # Get the number of predictions from the user
    num_predictions = st.number_input('Enter the number of predictions:', min_value=1, value=1)

    if st.button('Fetch Data and Make Predictions'):
        # Fetch and display the data
        st.write(f'Fetching data for {city_input}...')
        data, avg_row = fetch_data(city_input)
        st.write(data)

        # Display average values for numeric columns
        st.write('Average Values for Numeric Columns:')
        st.write(avg_row)

        # Make predictions and display the result
        st.write(f'Making {num_predictions} predictions...')
        predictions, _ = make_predictions(city_input, num_predictions)
        st.write(predictions)

if __name__ == '__main__':
    main()
