from selenium import webdriver
from time import sleep

from secrets import username, password
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

delay = 3

class GreyCampusBot():
    target_url = 'https://learn.greycampus.com/elearning/capm-training-instructor-led-old/quiz/274/result/708936'
    grey_campus_url = 'https://learn.greycampus.com/'
    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self):
        self.driver.get(self.target_url)

        fb_btn = self.driver.find_element_by_xpath('/html/body/div[1]/header/div/div/div/a')
        fb_btn.click()

        # switch to login popup
        # base_window = self.driver.window_handles[0]
        # self.driver.switch_to_window(self.driver.window_handles[1])

        email_in = self.driver.find_element_by_xpath('//*[@id="login_user_email"]')
        email_in.send_keys(username)

        pw_in = self.driver.find_element_by_xpath('//*[@id="login_user_password"]')
        pw_in.send_keys(password)

        login_btn = self.driver.find_element_by_xpath('//*[@id="sign_in_user"]/div[3]/button')
        login_btn.click()

        # self.driver.switch_to_window(base_window)

        sleep(.5)

        capm_old_button = self.driver.find_element_by_xpath('/html/body/div[3]/section[2]/div/div/div/div/div[1]/a/div/div[1]')
        capm_old_button.click()

        handles = self.driver.window_handles
        print(handles)
        self.driver.switch_to.window(handles[-1])
        print(self.driver.current_window_handle)
        print(self.driver.current_url)

    def get_reviews(self, review_num, review_url):
        self.driver.get(review_url)

        attempt_review_button = WebDriverWait(self.driver, delay).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div/div/div/table/tbody/tr/td[4]/a')))
        attempt_review_button.click()

        rows = self.driver.find_elements_by_xpath('//*[@id="result_body"]/tr')
        review_buttons = self.driver.find_elements_by_xpath('//*[@id="result_body"]/tr/td[6]/a')

        print(review_buttons)
        print(len(review_buttons))

        count=1
        y_val = 0
        for button in review_buttons:
            row = rows[count-1]
            # actions = ActionChains(self.driver)
            # actions.move_to_element(button).perform()

            # y_val += 53
            self.driver.execute_script(f"window.scrollBy(0, {row.size['height']});")
            # self.driver.execute_script("return arguments[0].scrollIntoView(0, document.documentElement.scrollHeight);", button)
            button.click()
            
            WebDriverWait(self.driver, delay).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="answer-modal"]/div/div/div[1]/button')))

            self.driver.save_screenshot(f'review{review_num}/question_{count}.png')
            count += 1
            close_button = self.driver.find_element_by_xpath('//*[@id="answer-modal"]/div/div/div[1]/button')
            close_button.click()
            # sleep(.8)


bot = GreyCampusBot()
review_urls = [
    'https://learn.greycampus.com/elearning/capm-training-instructor-led-old/quiz/274/quiz_attempts',
    'https://learn.greycampus.com/elearning/capm-training-instructor-led-old/quiz/275/quiz_attempts',
    'https://learn.greycampus.com/elearning/capm-training-instructor-led-old/quiz/276/quiz_attempts']
bot.login()
count = 1
for url in review_urls:
    bot.get_reviews(count, url)
    count += 1
