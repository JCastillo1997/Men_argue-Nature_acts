def air_url(search_query):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.keys import Keys
    
    options = Options()  # Create options object
    options.add_argument("--headless")  # Add the headless argument

    driver = webdriver.Chrome(options=options)  # Pass the options to the Chrome constructor
    driver.implicitly_wait(10)

    try:
        
        driver.get("https://www.iqair.com/")

        uk_link = driver.find_element(By.XPATH, "//li/a[contains(text(),'United Kingdom')]")
        uk_link.click()

        # Replace time.sleep(3) with WebDriverWait
        wait = WebDriverWait(driver, 10)
        accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Accept All Cookies')]")))
        accept_button.click()

        search_bar = driver.find_element(By.ID, "search-dropdown-input")
        search_bar.send_keys(search_query)
        search_bar.send_keys(Keys.TAB)

        wait = WebDriverWait(driver, 10)
        first_element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "locality-item")))
        first_element.click()

        # Adding an explicit wait for the Accept All Cookies button
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