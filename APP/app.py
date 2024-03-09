import streamlit as st
import numpy as np
import pandas as pd
import time
from data.air_quality_data import get_air_quality_data
from data.get_city_data import get_city_data
from data.make_predictions_for_df import make_predictions_for_df
import requests

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

def main():
    st.title('Data Analysis')

    city_name = st.text_input("Enter the city name", "New York")

    if st.button('Get Air and City Data'):
        try:
            pollution_df = get_air_quality_data(city_name)
            city_df = get_city_data(city_name)

            # Create a common key for joining
            pollution_df['city'] = city_name
            city_df['city'] = city_name

            # Perform the join operation based on the common key
            joined_df = pd.merge(city_df, pollution_df, on='city', how='outer')

            # Remove the key used for joining
            joined_df = joined_df.drop(columns=['city'])

            # Display the joined data
            st.write("Joined Data:")
            st.write(joined_df)

            make_prediction = st.radio("Do you want to make a prediction?", ("Yes", "No"))

            if make_prediction == "Yes":
                num_rows = st.number_input("How many rows do you want predicted?", min_value=1)

                # Assuming the make_predictions_for_df function is available
                if num_rows:
                    predictions = make_predictions_for_df(joined_df, num_rows)
                    st.write("Predictions:")
                    st.write(predictions)

        except ValueError as ve:
            st.write(ve)
        except requests.ConnectionError as ce:
            st.write(ce)

if __name__ == '__main__':
    main()