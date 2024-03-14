def air_url(search_query):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.keys import Keys
    import time

    driver = webdriver.Chrome()
    driver.implicitly_wait(10)  

    try:
        
        driver.get("https://www.iqair.com/")

        
        uk_link = driver.find_element(By.XPATH, "//li/a[contains(text(),'United Kingdom')]")
        uk_link.click()

        
        time.sleep(3)

        
        try:
            accept_button = driver.find_element(By.XPATH, "//button[contains(.,'Accept All Cookies')]")
            accept_button.click()
        except:
            print("Cookie consent pop-up not found or button not clickable")

        
        time.sleep(3)

        
        search_bar = driver.find_element(By.ID, "search-dropdown-input")
        search_bar.send_keys(search_query)
        search_bar.send_keys(Keys.TAB)

       
        wait = WebDriverWait(driver, 10)
        first_element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "locality-item")))
        first_element.click()

        
        accept_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Accept All Cookies')]")))
        accept_button.click()

        
        current_url = driver.current_url
        
        return current_url

    except Exception as e:
        print("An error occurred:", e)
    finally:
        driver.quit()



    search_query = input("Please enter the search query: ")
    url = air_url(search_query)
    print("The URL of the page is:", url)


def get_air_quality_data(city):
    import requests
    import pandas as pd

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
            return pollution_df
    else:
        raise requests.ConnectionError(f"Error: {response.status_code} - {response.text}")

city_name = input("Enter a city name: ")  
try:
    pollution_df = get_air_quality_data(city_name)
    print(pollution_df)
except ValueError as ve:
    print(ve)
except requests.ConnectionError as ce:
    print(ce)




def scrape_air_data(returned_url):
    import pandas as pd

    df_time = pd.read_html(returned_url)[0]
    df_similar = pd.read_html(returned_url)[1]
    df_stations = pd.read_html(returned_url)[2]
    df_index = pd.read_html(returned_url)[3]
    df_poll = pd.read_html(returned_url)[4]
    df_recomendations = pd.read_html(returned_url)[5]
    df_temp_pol_wind = pd.read_html(returned_url)[6]

    return df_time, df_similar, df_stations, df_index, df_poll, df_recomendations, df_temp_pol_wind



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
        print("Error:", response.status_code, respoonse_text)
        return None
city_name = input('Enter the city name: ')
city_df = get_city_data(city_name)
if city_df is not None:
    print(city_df)





def make_predictions_for_df(model, joined_df, num_predictions):
    import pandas as pd
    if __name__ == "__main__":
        expanded_df = pd.concat([joined_df] * (num_predictions // len(joined_df) + 1), ignore_index=True)
        expanded_df = expanded_df.iloc[:num_predictions]

        predictions = model.predict(expanded_df)

        return predictions