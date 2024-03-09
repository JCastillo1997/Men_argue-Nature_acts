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
