import streamlit as st
import numpy as np
import pandas as pd
import time
from data.air_quality_data import get_air_quality_data
from data.get_city_data import get_city_data
import streamlit as st
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
    st.title('Air Quality Data Analysis')

    city_name = st.text_input("Enter the city name", "New York")

    if st.button('Get Air Quality Data'):
        try:
            pollution_df = get_air_quality_data(city_name)
            st.write("Air Quality Data:")
            st.write(pollution_df)
        except ValueError as ve:
            st.write(ve)
        except requests.ConnectionError as ce:
            st.write(ce)

if __name__ == '__main__':
    main()