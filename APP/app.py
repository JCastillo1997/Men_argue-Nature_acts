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
    body {
        color: #ccc; /* Set main body text color to light gray */
        font-size: 14px; /* Set main body font size to 14px */
        background-color: #000; /* Set background color to black */
        margin: 2em;
    }
    .title {
        color: #fff; /* Set title text color to white */
        font-size: 30px; /* Set title font size to 20px */
        margin-bottom: 1em; /* Add margin below the title */
        border-bottom: 2px solid #fff; /* Add a white line below the title */
        padding-bottom: 0.5em; /* Add padding below the title */
        text-align: center; /* Center align the title */
    }

</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

st.markdown('<h1 class="title">Men argues, Nature acts</h1>', unsafe_allow_html=True)


def fetch_data(city):
    air_quality_df = get_air_quality_data(city)
    city_df = get_city_data(city)
    air_quality_df['key'] = 1
    city_df['key'] = 1
    merged_df = pd.merge(city_df, air_quality_df, on='key')
    merged_df.drop(columns=['key'], inplace=True)
    numeric_columns = merged_df.select_dtypes(include=['number']).columns
    avg_row = merged_df[numeric_columns].mean()
    return merged_df, avg_row


def make_predictions(city, num_predictions):
    merged_df, avg_row = fetch_data(city)
    predictions_df = make_predictions_for_df(merged_df, num_predictions)
    return predictions_df, avg_row

def display_map(data):
    st.map(data)

def main():
    data = None
    st.markdown("<h2 style='color: #fff; font-size: 16px;'>Welcome, in this app you may input a city, obtain some data about pollution about said city and get an insight based on Madrid pollution policies</h2>", unsafe_allow_html=True)

    city_input = st.text_input('Enter a city name:', 'New York')
    num_predictions = 1

    if st.button('Fetch Data and Make Predictions'):
        st.write(f'Fetching data for {city_input}...')
        data, avg_row = fetch_data(city_input)
        st.write(data)

        st.write('Average Values for Numeric Columns:')
        st.write(avg_row)

        st.write(f'Making {num_predictions} predictions...')
        predictions, _ = make_predictions(city_input, num_predictions)
        st.write(predictions)

    # Divide the layout into two columns
    col1, col2 = st.columns([2, 3])

    # Compare values when the user selects a pollutant
    pred_button = st.text_input('Would you like to compare predictions with average values? (yes/no)', 'no')
    if pred_button.lower() == 'yes':
        if data is not None and not data.empty:
            with col1:
                selected_variables = ['co', 'no2', 'so2', 'pm2.5', 'pm10']

                # Retrieve predictions based on selected variables
                selected_predictions = predictions[selected_variables]

                # Compare values and calculate percentage difference
                comparison_result = {}
                for variable in selected_variables:
                    average_value = avg_row[variable]
                    prediction_value = selected_predictions[variable]

                    # Calculate percentage difference
                    percentage_difference = ((prediction_value - average_value) / average_value) * 100

                    # Store comparison result
                    comparison_result[variable] = {'average_value': average_value,
                                                'prediction_value': prediction_value,
                                                'percentage_difference': percentage_difference}

                # Display comparison results
                for variable, values in comparison_result.items():
                    st.write(f"{variable.upper()} (Average Value: {values['average_value']:.3f})")
                    st.write(f"Prediction Value: {values['prediction_value'].iloc[0]}")
                    st.write(f"Percentage Difference: {values['percentage_difference'].iloc[0]:.2f}%")

        else:
            st.write("Please fetch data first before comparing predictions.")

    # Display the map
    with col2:
        if data is not None and not data.empty:
            display_map(data[['latitude', 'longitude']])

if __name__ == '__main__':
    main()

