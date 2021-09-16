#!/usr/bin/python3

from selenium import webdriver
import time

# target url for rps
URL = "https://rockpaperprizes.circlekgames.ca/"
f = open("/Users/geoffreylee/Desktop/rps_results.csv", "a")

# xpaths of (most) elements used
play_again_xpath = '//*[@id="__next"]/main/section/form/button'
rock_xpath = '//*[@id="__next"]/div[2]/div[4]/div/div[1]/label'
lose_message_xpath = '//*[@id="__next"]/main/section/h2' # SORRY, TRY AGAIN! YOU HAVE 2 PLAYS LEFT TODAY
win_message_xpath = '//*[@id="__next"]/main/section/div[1]/p'
final_lose_message_xpath = '//*[@id="__next"]/main/section/p'

already_won_xpath = '//*[@id="__next"]/main/section/div[2]/h1'
already_lost_xpath = '//*[@id="__next"]/main/section/div[2]/h3'

def print_and_write(message):
    print(message)
    f.write(f"{message}\n")

def already_used(driver):
    return check_exists_by_xpath(already_won_xpath, driver) or check_exists_by_xpath(already_lost_xpath, driver)

# choose rock up to 4 times (but may leave after 2)
def click_rocks(driver):
    for i in range(4):
        time.sleep(2)
        did_click = safe_click(rock_xpath, driver)
        if not did_click:
            break

# checks if the element of xpath exists
def check_exists_by_xpath(xpath, driver):
    try:
        driver.find_element_by_xpath(xpath)
    except:
        return False
    return True

# if the element exists, it will click it
def safe_click(xpath, driver):
    if check_exists_by_xpath(xpath, driver):
        element = driver.find_element_by_xpath(xpath)
        element.click()
        return True
    return False

# selects province, provides number, agrees, submits
def start_up(phone_number, driver):
    driver.get(URL)
    province_select = driver.find_element_by_xpath('//*[@id="__next"]/main/section/div[2]/div/div/form/select')
    province_select.click()
    ontario = driver.find_element_by_xpath('//*[@id="__next"]/main/section/div[2]/div/div/form/select/option[9]')
    ontario.click()
    agree = driver.find_element_by_xpath('//*[@id="__next"]/main/section/section[1]/form/div[1]/label[1]/span')
    agree.click()
    number = driver.find_element_by_xpath('//*[@id="__next"]/main/section/section[1]/form/div[2]/input')
    number.send_keys(phone_number)
    # click phone number submit
    safe_click('//*[@id="__next"]/main/section/section[1]/form/div[2]/button', driver)

# return true if a win or lose, return false if still more games to play
def print_result(phone_number, driver):
    if check_exists_by_xpath(win_message_xpath, driver):
        win_message = driver.find_element_by_xpath(win_message_xpath)
        prize_won = driver.find_element_by_xpath('//*[@id="__next"]/main/section/div[1]/h2[1]')
        print_and_write(f"WIN:, {phone_number}, {win_message.text}, {prize_won.text}")
    else:
        print_and_write(f"LOSE:, {phone_number}, N/A, N/A")

# checks if the screen is a final game over screen
# (win or FINAL lost (lose 3 times))
def is_end_of_all_games(driver):
    return check_exists_by_xpath(win_message_xpath, driver) or check_exists_by_xpath(final_lose_message_xpath, driver)

# open chrome, play all games until finished, close chrome
def play_one_number(phone_number):
    driver = webdriver.Chrome()
    start_up(phone_number, driver)
    time.sleep(2)
    if already_used(driver):
        print(f"ALREADY USED: {phone_number}")
        driver.close()
        return
    end_of_all_games = False

    while not end_of_all_games:
        safe_click(play_again_xpath, driver)
        click_rocks(driver) # clicks rocks all the way to a win or lose or FINAL lose
        time.sleep(2)
        end_of_all_games = is_end_of_all_games(driver)

    print_result(phone_number, driver)
    driver.close()

def main():
    numbers = [
        "4379930844",
        "2899219835",
        "6478084591",
        "6476559008",
        "4163330028",
        "6477870353",
        "6473001522",
        "4164004898",
        "2896847936",
        "6478063318"]

    for number in numbers:
        play_one_number(number)

    print("FINISHED")
    f.close()

if __name__ == "__main__":
    main()
