def get_city_data(city_name):
    import requests
    import pandas as pd
    import json

    api_url = 'https://api.api-ninjas.com/v1/city?name={}'.format(city_name)
    response = requests.get(api_url, headers={'X-Api-Key': 'XhKog+U7kqeVm1jW7MeNDg==ZsJmH2sbNbEnRq3H'})
    if response.status_code == requests.codes.ok:
        response_text = response.text
        data = json.loads(response_text)
        df = pd.DataFrame(data)
        return df
    else:
        print("Error:", response.status_code, response_text)
        return None

# For testing:
if __name__ == "__main__":
    city_name = input('Enter the city name: ')
    city_df = get_city_data(city_name)
    if city_df is not None:
        print(city_df)