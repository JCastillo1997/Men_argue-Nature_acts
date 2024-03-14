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
import seaborn as sns
import matplotlib.pyplot as plt


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
    avg_row = merged_df[numeric_columns].sum()
    return merged_df,avg_row


def make_predictions(city, num_predictions):
    merged_df, avg_row = fetch_data(city)
    predictions_df = make_predictions_for_df(merged_df, num_predictions)
    return predictions_df, avg_row

def display_map(data):
    st.map(data)


def plot_pollution_comparison(df1, df2):
    pollutants = ['co', 'no2', 'o3', 'so2', 'pm2.5', 'pm10']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for pollutant in pollutants:
        ax.plot(pollutants, df1[pollutant], label=f'{pollutant} - Average Rows', marker='o')
        ax.plot(pollutants, df2[pollutant], label=f'{pollutant} - Predictions', marker='o')
    
    ax.set_xlabel('Pollutant')
    ax.set_ylabel('Quantity')
    ax.set_title('Comparison of Pollution Levels')
    ax.legend()
    ax.grid(True)
    
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

# Your existing main function
def main():
    data = None
    st.markdown("<h2 style='color: #fff; font-size: 16px;'>Welcome, in this app you may input a city, obtain some data about pollution about said city and get an insight based on Madrid pollution policies</h2>", unsafe_allow_html=True)

    city_input = st.text_input('Enter a city name:', 'New York')
    num_predictions = 1

    if st.button('Fetch Data and Make Predictions'):
        st.write(f'Fetching data for {city_input}...')
        data, avg_row = fetch_data(city_input)
        st.write(data)

        st.write('average values for pollutants:')
        st.write(avg_row[['co','no2','o3','so2','pm2.5','pm10']])

        st.write('applying the model to the predictions')
        predictions, _ = make_predictions(city_input, num_predictions)
        st.write(predictions)

   
    col1, col2 = st.columns([2, 3])

    
    pred_button = st.text_input('Would you like to compare predictions with average values? (yes/no)', 'no')
    if pred_button.lower() == 'yes':
        if data is not None and not data.empty:
            with col1:
                st.write("Comparison Results")
                selected_variables = ['co', 'no2', 'so2', 'pm2.5', 'pm10']

                
                selected_predictions = predictions[selected_variables]

                
                comparison_result = {}
                for variable in selected_variables:
                    average_value = avg_row[variable]
                    prediction_value = selected_predictions[variable]

                    
                    percentage_difference = ((prediction_value - average_value) / average_value) * 100

                   
                    comparison_result[variable] = {'average_value': average_value,
                                                    'prediction_value': prediction_value,
                                                    'percentage_difference': percentage_difference}

                
                for variable, values in comparison_result.items():
                    st.write(f"{variable.upper()} (Average Value: {values['average_value']:.3f})")
                    st.write(f"Prediction Value: {values['prediction_value'].iloc[0]}")
                    st.write(f"Percentage Difference: {values['percentage_difference'].iloc[0]:.2f}%")

        else:
            st.write("Please fetch data first before comparing predictions.")

    
    with col2:
        if data is not None and not data.empty:
            with st.expander("Map", expanded=True):
                display_map(data[['latitude', 'longitude']])
    

    col1, col2 = st.columns(2)
    with col1:
        plt.style.use('dark_background')

        if data is not None and not data.empty:
            fig, ax = plt.subplots()
            prediction_color = "#00C18B"
            average_color = "#003333"  
            sns.barplot(x=['Average', 'Prediction'], y=[avg_row['co'], predictions['co'].mean()], 
                ax=ax, alpha=0.7, palette=[average_color, prediction_color])
            
            ax.set_title('Comparison of CO Levels')
            ax.set_ylabel('CO Levels')

            ax.patch.set_alpha(0)
            fig.patch.set_alpha(0)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.yaxis.grid(color='white', linestyle='--', linewidth=0.5)

            st.pyplot(fig)

        with col2:
            plt.style.use('dark_background')

            if data is not None and not data.empty:
                fig, ax = plt.subplots()
                prediction_color = "#AF4FD1"
                average_color = "#49235C"  
                sns.barplot(x=['Average', 'Prediction'], y=[avg_row['no2'], predictions['no2'].mean()], 
                    ax=ax, alpha=0.7, palette=[average_color, prediction_color])
                
                ax.set_title('Comparison of no2 Levels')
                ax.set_ylabel('no2 Levels')
                ax.patch.set_alpha(0)
                fig.patch.set_alpha(0)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.yaxis.grid(color='white', linestyle='--', linewidth=0.5)

                st.pyplot(fig)

    # Add line chart comparison after bar plots
    col1, col2 = st.columns(2)
    with col1:
        plt.style.use('dark_background')

        if data is not None and not data.empty:
            fig, ax = plt.subplots()
            prediction_color = "#30A3D9"
            average_color = "#1C5875"  
            sns.barplot(x=['Average', 'Prediction'], y=[avg_row['o3'], predictions['o3'].mean()], 
                ax=ax, alpha=0.7, palette=[average_color, prediction_color])
            
            ax.set_title('Comparison of O3 Levels')
            ax.set_ylabel('O3 Levels')
            ax.patch.set_alpha(0)
            fig.patch.set_alpha(0)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.yaxis.grid(color='white', linestyle='--', linewidth=0.5)

            st.pyplot(fig)

        with col2:
            plt.style.use('dark_background')

            if data is not None and not data.empty:
                fig, ax = plt.subplots()
                prediction_color = "#E30000"
                average_color = "#690000"  
                sns.barplot(x=['Average', 'Prediction'], y=[avg_row['so2'], predictions['so2'].mean()], 
                    ax=ax, alpha=0.7, palette=[average_color, prediction_color])
                
                ax.set_title('Comparison of SO2 Levels')
                ax.set_ylabel('SO2 Levels')
                ax.patch.set_alpha(0)
                fig.patch.set_alpha(0)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.yaxis.grid(color='white', linestyle='--', linewidth=0.5)

                st.pyplot(fig)
                
    # Line chart comparison
    col1, col2 = st.columns(2)
    with col1:
        plt.style.use('dark_background')

        if data is not None and not data.empty:
            fig, ax = plt.subplots()
            prediction_color = "#EBCF1E"
            average_color = "#8F7C13"  
            sns.barplot(x=['Average', 'Prediction'], y=[avg_row['pm2.5'], predictions['pm2.5'].mean()], 
                ax=ax, alpha=0.7, palette=[average_color, prediction_color])
            
            ax.set_title('Comparison of Pm2.5')
            ax.set_ylabel('Pm µm 2.5')
            ax.patch.set_alpha(0)
            fig.patch.set_alpha(0)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.yaxis.grid(color='white', linestyle='--', linewidth=0.5)

            st.pyplot(fig)

        with col2:
            plt.style.use('dark_background')

            if data is not None and not data.empty:
                fig, ax = plt.subplots()
                prediction_color = "#D3D19E"
                average_color = "#5F5E47"  
                sns.barplot(x=['Average', 'Prediction'], y=[avg_row['pm10'], predictions['pm10'].mean()], 
                    ax=ax, alpha=0.7, palette=[average_color, prediction_color])
                
                ax.set_title('Comparison of Pm10')
                ax.set_ylabel('Pm µm 10')
                ax.patch.set_alpha(0)
                fig.patch.set_alpha(0)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.yaxis.grid(color='white', linestyle='--', linewidth=0.5)

                st.pyplot(fig)
                


if __name__ == '__main__':
    main()
