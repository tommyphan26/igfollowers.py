#selenium is an open source tool for automating web browsers
from selenium import webdriver
from selenium.webdriver.chrome.service import Service #service tell selenium how to start and manage the driver -> connect the remote to your browser
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By #need this when adding the "By.NAME"
from selenium.webdriver.support.ui import WebDriverWait #waits until webpage is ready to open
from selenium.webdriver.support import expected_conditions as EC #provides functions to handle checking conditions
from getpass import getpass #hide password input (won't be displayed while typing)
import time
import random

time.sleep(random.uniform(1.5, 4.0))

#mimics a real browser
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")
driver = webdriver.Chrome(options=options)


count = 0

#user input for the credentials
username = input("Enter Your Instagram Username: ")
password = input("Enter Your Instagram Password: ")


def login(driver):
    #Replace with webdriver wait
    #By.NAME is a locator stragtegy sed to identify web elements by their name attribute in the HTML
    try:
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        username_field.send_keys(username)


        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'password'))
        )


        password_field.send_keys(password + u'\ue007')


        print("Login Successful.")
        time.sleep(5)
    except Exception as e:
        print("Login Failed:", e)


   
def click_button_with_css(driver, css_selector):
    element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))) #expected condition to where the element will be clickable - selenium.com
    element.click()


def open_list(driver, list_type):
    try:
        list_button_css = f'a[href = "/{username}/{list_type}/"]'
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, list_button_css))).click()
        time.sleep(3)  # Adds wait before trying to open the list
        print(f"Opened {list_type} list.")
        # Adding additional wait to ensure content is loaded
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//ul//li")))
    except Exception as e:
        print(f"Error opening {list_type} list:", e)


def scroll_list(driver):
    try:
        dialog = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//div[contains(@class, 'isgrP')]"))
        )

        print("Starting to scroll...")

        last_height = driver.execute_script("return arguments[0].scrollHeight", dialog)
        print(f"Initial scroll height: {last_height}")

        while True:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
            time.sleep(random.uniform(1, 2))  # Add randomness to mimic human behavior

            new_height = driver.execute_script("return arguments[0].scrollHeight", dialog)
            print(f"New scroll height: {new_height}")

            if new_height == last_height:
                print("Reached the end of the list.")
                break
            last_height = new_height
    except Exception as e:
        print("Scrolling Failed:", e)




   


def navigate_and_scroll(driver):
    print("Navigating to followers...")
    scroll_list(driver,"followers")


    print("Navigating to following...")
    scroll_list(driver, "following")

def get_user_list(driver):
    list_xpath = "//div[@role='dialog']//ul//li"
    users = []
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, list_xpath)))
        
        # Adding a small delay to ensure the elements are loaded
        time.sleep(random.uniform(1, 3))

        user_elements = driver.find_elements(By.XPATH, list_xpath)
        if user_elements:
            for elem in user_elements:
                try:
                    username = elem.find_element(By.CSS_SELECTOR, "a").text
                    if username:
                        users.append(username)
                except:
                    pass
        else:
            print("No user elements found in the dialog.")
        return users
    except Exception as e:
        print("Error fetching user list:", e)
        return []


def scroll_until_end(scrollable_element):
    last_height = driver.execute_script("return arguments[0].scrollTop;", scrollable_element)
    while True:
        driver.execute_script("arguments[0].scrollTop += arguments[0].offsetHeight;", scrollable_element)
        time.sleep(2)  # Adjust delay
        new_height = driver.execute_script("return arguments[0].scrollTop;", scrollable_element)
        if new_height == last_height:  # If no new content loads
            break
        last_height = new_height


def main():
   driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
   driver.get("https://www.instagram.com/")
   time.sleep(random.uniform(3, 5))
   
   login(driver)
   time.sleep(5)


   if "login" in driver.current_url:
       print("Login failed. Please Check Your Username and Password.")
       driver.quit()
       return
   
   driver.get(f"https://www.instagram.com/{username}/")
   time.sleep(random.uniform(2, 4))

   open_list(driver, "followers")
   scroll_list(driver)
   followers = get_user_list(driver)
   print(f'Followers: {len(followers)}')

#close followers dialog
   driver.find_element(By.XPATH, "//div[@role='dialog']//button").click()
   time.sleep(random.uniform(1, 3))

   open_list(driver, "following")
   scroll_list(driver)
   following = get_user_list(driver)
   print(f'Following: {len(following)}')

#users not following back
   not_following_back = [user for user in following if user not in followers]
   print("\nUsers you follow but they don't follow back:", not_following_back)
   driver.quit()
 
if __name__ == "__main__":
   main()

