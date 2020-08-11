import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.proxy import *
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


username = input("Enter the mock username to login with: ")
password = input("Enter the mock password to login with: ")
geck_path = input("Enter geckodriver filepath: ")
max_time = 7


binary = FirefoxBinary(r'C:\\Program Files\\Mozilla Firefox\\firefox.exe') # """ but with firefox
profile = webdriver.FirefoxProfile()
profile.set_preference('permissions.default.desktop-notification', 1)     # Disable notification permissions prompt
profile.set_preference("general.useragent.override", "test")
driver = webdriver.Firefox(
    firefox_binary=binary,
    firefox_profile=profile,
    executable_path='geckodriver.exe'  # download/install GD and drag it into the selenium_stuff directory
)


def wait_until_loaded(browser, delay, xpath):
    try:
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        print("Loading took too much time!")
    return


def visit(target_user, mock_username, mock_password):
    driver.get("https://old.reddit.com/user/" + target_user)
    login_button = '//a[@href="https://www.reddit.com/login"]'
    wait_until_loaded(driver, max_time, login_button)
    driver.find_element_by_xpath(login_button).click()
    username_bar = '/html/body/div[6]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/form/div[5]/button'
    time.sleep(5)
    actions = ActionChains(driver)
    actions.send_keys(mock_username)
    actions.send_keys(Keys.TAB)
    actions.send_keys(mock_password)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    print(mock_username + " has signed in")


def vote():
    counter = 1
    page_count = 1
    upvote_count = 0
    next_clicked = False
    while True:
        try:
            upvotes = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div['+str(counter)+']/div[1]/div[1]').click()
            counter = int(counter)
            counter += 2
            upvote_count += 1
        except NoSuchElementException:
            try:
                next_page_1 = "/html/body/div[4]/div[2]/div[51]/span/span/a"
                next_page_2 = "/html/body/div[4]/div[2]/div[51]/span/span[3]/a"
                counter = 1
                max_time = 7
                if not next_clicked:
                    next_clicked = True
                    driver.find_element_by_xpath(next_page_1).click()
                    page_count += 1
                    print("going to page " + str(page_count) + '!')
                    wait_until_loaded(driver, max_time, next_page_1)
                    pass
                else:
                    driver.find_element_by_xpath(next_page_2).click()
                    page_count += 1
                    print("going to page " + str(page_count) + '!')
                    wait_until_loaded(driver, max_time, next_page_2)
                    pass
            except (NoSuchElementException, ElementNotInteractableException) as finished_1:
                print("finished_1")
                print("Either all unarchived posts and comments have been upvoted"
                      " or unable to find the upvote element by xpath. \n"
                      + str(upvote_count) + " upvotes have been given")
                break
                pass
        except (ElementClickInterceptedException, ElementNotInteractableException) as finished_2:
            print("finished_2")
            print("Either all unarchived posts and comments have been upvoted"
                  " or unable to find the upvote element by xpath. \n"
                  + str(upvote_count) + " upvotes have been given")
            break
            pass
    return


if __name__ == "__main__":
    victim = input("Enter target user: ")
    print("Commencing...")
    visit(target_user=victim, mock_username=username, mock_password=password)
    time.sleep(10)
    vote()
