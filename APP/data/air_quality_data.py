def get_air_quality_data(city):
    import pandas as pd
    import requests
    api_url = 'https://api.api-ninjas.com/v1/airquality?city={}'.format(city)
    response = requests.get(api_url, headers={'X-Api-Key': 'XhKog+U7kqeVm1jW7MeNDg==ZsJmH2sbNbEnRq3H'})
    if response.status_code == requests.codes.ok:
        air_quality_data = response.json()
        if 'error' in air_quality_data:
            raise ValueError("Error: City not found in the database")
        else:
            data = {k.lower(): [v['concentration'], v['aqi']] for k, v in air_quality_data.items() if k != 'overall_aqi'}
            data['overall_aqi'] = [None, air_quality_data['overall_aqi']]
            pollution_df = pd.DataFrame(data)
            
            # Fill NaN values with 0
            pollution_df = pollution_df.fillna(0)
            
            return pollution_df
    else:
        raise requests.ConnectionError(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    city_name = input("Enter a city name: ")
    try:
        pollution_df = get_air_quality_data(city_name)
        print(pollution_df)
    except ValueError as ve:
        print(ve)
    except requests.ConnectionError as ce:
        print(ce)