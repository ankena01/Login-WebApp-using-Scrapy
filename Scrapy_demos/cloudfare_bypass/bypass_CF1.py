from seleniumbase import SB
import time

# from selenium import webdriver

### Scenario -1 - Bypass captcha at user login without interaction (click)
# with SB(uc=True) as sb:
#     url = "https://gitlab.com/users/sign_in"
#     sb.driver.uc_open_with_reconnect(url, 5)
#     if not sb.is_text_visible("Username ", "//div[@class='form-group']/label[contains(text(), 'Username')]"):
#         sb.driver.uc_open_with_reconnect(url, 4)
#     sb.assert_text("Username", "//div[@class='form-group']/label[contains(text(), 'Username')]")
#     sb.highlight("//div[@class='form-group']/label[contains(text(), 'Username')]", loops=4)
#     sb.post_message("Selenium Base is not detected ", 6)

### Scenario -2 - Bypass captcha at user login with interaction (click)

# url = "seleniumbase.io/apps/turnstile"
# url = "https://www.advice.co.th/product/notebook"
# def open_turnstile(sb):
    
#     sb.driver.uc_open_with_reconnect(url, reconnect_time = 4)

# def click_turnstile_and_verify(sb):
#     sb.switch_to_frame("iframe")
#     sb.driver.uc_click("span")
#     time.sleep(5)
#     # sb.assert_element("img#captcha-success", timeout=3)

# with SB(uc=True) as sb:
#     open_turnstile(sb)
#     try:
#         click_turnstile_and_verify(sb)
#     except:
#         open_turnstile(sb)
#         click_turnstile_and_verify(sb)
#     sb.set_messenger_theme(location="top_right")
#     sb.post_message("Selenium Base is not detected ", 6)


url = "https://www.electronet.gr/pliroforiki/laptops"
def open_turnstile(sb):
    sb.driver.uc_open_with_reconnect(url, reconnect_time = 4)

def click_turnstile_and_verify(sb):
    sb.switch_to_frame("iframe")
    sb.driver.uc_click("span")
    time.sleep(5)
    # sb.assert_element("img#captcha-success", timeout=3)

with SB(uc=True) as sb:
    open_turnstile(sb)

    # try:
    #     click_turnstile_and_verify(sb)
    # except:
    #     open_turnstile(sb)
    #     click_turnstile_and_verify(sb)
    
    sb.set_messenger_theme(location="top_right")
    sb.post_message("Selenium Base is not detected ", 8)
    page_content = sb.driver.get_page_source()
    print(page_content)
