import base64
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common import by, keys, action_chains
from selenium.common.exceptions import StaleElementReferenceException

options = webdriver.ChromeOptions()
options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
options.debugger_address = "localhost:9222"
driver = webdriver.Chrome(options=options, service=Service("../venv/chromedriver.exe"))
driver.maximize_window()
Action = action_chains.ActionChains(driver)
successes = 0

driver.switch_to.window(driver.window_handles[0])

# photo_data, video_data, audio_data, doc_data are the strings in base64
def authentication_by_user():
    driver.get('https://web.whatsapp.com/')
    authenticated = False
    time.sleep(10)
    driver.find_element(by.By.CSS_SELECTOR, value="div[data-testid='qrcode']").screenshot('QR Code.png')
def open_contact(contact_number):
    driver.get(f'https://web.whatsapp.com/send/?phone={contact_number}&text&type=phone_number&app_absent=0')
    time.sleep(20)
def get_contact_number_from_name(contact_name):
    all_contacts = []
    driver.find_element(by.By.CSS_SELECTOR, value="div[data-testid='chat-list-search']").send_keys( keys.Keys.CONTROL + 'a' + keys.Keys.CONTROL + contact_name)
    time.sleep(2)
    contacts = [i for i in driver.find_elements(by.By.TAG_NAME, value="span") if i.get_attribute("title") == contact_name]

    for contact in contacts:
        contact.click()
        time.sleep(1)
        driver.find_element(by.By.CSS_SELECTOR, value="header[data-testid='conversation-header']").click()
        time.sleep(1)
        # driver.find_element(by.By.CSS_SELECTOR, value="section[data-testid='group-info-drawer-body']>div>div>div:nth-child(3)>span>span")
        # Upper code is the alternative of the below code
        if driver.find_element(by.By.CLASS_NAME, value="AjtLy").text.split('·')[0] == 'Group ':
            pass
        else:
            all_contacts.append(driver.find_element(by.By.CLASS_NAME, value="AjtLy").text.replace(' ', ''))

    driver.find_element(by.By.TAG_NAME, value="body").send_keys(keys.Keys.ESCAPE)
    time.sleep(1)
    driver.find_element(by.By.TAG_NAME, value="body").send_keys(keys.Keys.ESCAPE)
    time.sleep(1)
    driver.find_element(by.By.CSS_SELECTOR, value="button[data-testid='icon-search-morph']").click()
    driver.find_element(by.By.CSS_SELECTOR, value="button[data-testid='icon-search-morph']").click()

    return [*set(all_contacts)]
def create_group(group_name, group_contacts):
    driver.find_element(by.By.CSS_SELECTOR, value="div[aria-label='Menu']").click()
    time.sleep(1)
    driver.find_element(by.By.CSS_SELECTOR, value="div[aria-label='New group']").click()
    time.sleep(1)
    for contact in group_contacts:
        driver.find_element(by.By.CSS_SELECTOR, value="input[data-testid='inputarea']").send_keys(keys.Keys.CONTROL + 'a' + keys.Keys.CONTROL + contact)
        time.sleep(1)
        driver.find_element(by.By.CSS_SELECTOR, value="div[data-testid='contact-list-key']").click()
    time.sleep(1)
    driver.find_element(by.By.CSS_SELECTOR, value="span[data-testid='arrow-forward']").click()
    time.sleep(1)
    driver.find_element(by.By.CSS_SELECTOR, value="div[data-testid='pluggable-input-body']").send_keys(group_name)
    time.sleep(1)
    driver.find_element(by.By.CSS_SELECTOR, value="span[data-testid='checkmark-medium']").click()
    time.sleep(1)
    driver.find_element(by.By.TAG_NAME, value="body").send_keys(keys.Keys.ESCAPE)
def send_msg(contact_person, message):
    message_encoded = urllib.parse.quote(message)
    driver.get(
        f'https://web.whatsapp.com/send/?phone={contact_person}&text={message_encoded}&type=phone_number&app_absent=0')
    time.sleep(10)
    driver.find_element(by.By.CSS_SELECTOR, value="span[data-testid='send']").click()
    driver.find_element(by.By.TAG_NAME, value="body").send_keys(keys.Keys.ESCAPE)

    global successes
    successes += 1
def send_img(contact_person, photo_data):
    open_contact(contact_person)
    driver.find_element(by.By.CSS_SELECTOR, value="span[data-testid='clip']").click()
    for i in driver.find_elements(by.By.TAG_NAME, value="input"):
        if i.get_attribute('accept') == 'image/*,video/mp4,video/3gpp,video/quicktime':
            with open('TestData/test.jpg', 'wb') as image:
                decoded_data = base64.b64decode(photo_data)
                image.write(decoded_data)
            i.send_keys(r'C:\Program Files\100 Days Of Python\Arihant AI\TestData\test.jpg')
    time.sleep(10)
    driver.find_element(by.By.CSS_SELECTOR, value="div[aria-label='Send']")

    driver.find_element(by.By.TAG_NAME, value="body").send_keys(keys.Keys.ESCAPE)
    global successes
    successes += 1
    time.sleep(5)
def send_video(contact_person, video_data):
    open_contact(contact_person)
    driver.find_element(by.By.CSS_SELECTOR, value="span[data-testid='clip']").click()
    time.sleep(2)
    for i in driver.find_elements(by.By.TAG_NAME, value="input"):
        if i.get_attribute('accept') == 'image/*,video/mp4,video/3gpp,video/quicktime':
            with open('TestData/test.mp4', 'wb') as video:
                decoded_data = base64.b64decode(video_data)
                video.write(decoded_data)
            i.send_keys(r'C:\Program Files\100 Days Of Python\Arihant AI\TestData\test.mp4')
    time.sleep(5)
    driver.find_element(by.By.CSS_SELECTOR, value="span[data-testid='send']").click()
    time.sleep(1)
    driver.find_element(by.By.TAG_NAME, value="body").send_keys(keys.Keys.ESCAPE)
    global successes
    successes += 1
    time.sleep(5)
def send_audio(contact_person, audio_data):
    open_contact(contact_person)
    driver.find_element(by.By.CSS_SELECTOR, value="span[data-testid='clip']").click()
    time.sleep(5)
    for i in driver.find_elements(by.By.TAG_NAME, value="input"):
        if i.get_attribute('accept') == '*':
            with open('TestData/test.mp3', 'wb') as audio:
                decoded_data = base64.b64decode(audio_data)
                audio.write(decoded_data)
            i.send_keys(r'C:\Program Files\100 Days Of Python\Arihant AI\TestData\test.mp3')
    time.sleep(5)
    driver.find_element(by.By.CSS_SELECTOR, value="div[aria-label='Send']").click()
    driver.find_element(by.By.TAG_NAME, value="body").send_keys(keys.Keys.ESCAPE)
    global successes
    successes += 1
    time.sleep(5)
def send_doc(contact_person, doc_data, file_extension):
    open_contact(contact_person)
    driver.find_element(by.By.CSS_SELECTOR, value="span[data-testid='clip']").click()
    for i in driver.find_elements(by.By.TAG_NAME, value="input"):
        if i.get_attribute('accept') == '*':
            with open(f'TestData/test.{file_extension}', 'wb') as document:
                decoded_data = base64.b64decode(doc_data)
                document.write(decoded_data)
            i.send_keys(rf'C:\Program Files\100 Days Of Python\Arihant AI\TestData\test.{file_extension}')
    time.sleep(5)
    driver.find_element(by.By.CSS_SELECTOR, value="div[aria-label='Send']").click()
    driver.find_element(by.By.TAG_NAME, value="body").send_keys(keys.Keys.ESCAPE)
    global successes
    successes += 1
    time.sleep(5)

# In Development ---
def get_group_contacts(group_name):
    driver.find_element(by.By.CSS_SELECTOR, value="div[data-testid='chat-list-search']").send_keys(keys.Keys.CONTROL + 'a' + keys.Keys.CONTROL + group_name)
    time.sleep(1)

    all_groups = driver.find_elements(by.By.CSS_SELECTOR, value=f"span[title*='{group_name}']")
    for contact in all_groups:
        contact.click()
        time.sleep(1)
        driver.find_element(by.By.CSS_SELECTOR, value="header[data-testid='conversation-header']").click()
        time.sleep(1)
    try:
        for i in driver.find_elements(by.By.CSS_SELECTOR, value="section[data-testid='group-info-drawer-body'] div"):
            if 'View all ' in i.text.split('('):
                i.click()
        time.sleep(5)
        driver.find_element(by.By.CSS_SELECTOR, value="div[data-testid='contacts-modal']").send_keys(keys.Keys.PAGE_DOWN)
        all_contacts = [i.text for i in driver.find_elements(by.By.CSS_SELECTOR, value="div[role='gridcell']>div>span")]
        all_contacts.remove(group_name)
    except StaleElementReferenceException:
        all_contacts = [i.text for i in driver.find_elements(by.By.CSS_SELECTOR, value="div[role='gridcell']>div>span")]
    print(all_contacts)

    try:
        parent_scroll = driver.find_elements_by_class_name("_1H6CJ")[0]
        parent_scroll_element_height = parent_scroll.value_of_css_property("height")

        view_all_button = driver.find_element_by_class_name("_3p0T6")
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollIntoView();", view_all_button)
        view_all_button.click()
        print(parent_scroll_element_height)
        # print(len(all_contacts))
        height = 72
        parent_scroll_element_height = parent_scroll_element_height[:-2]
        totalHeight = int(parent_scroll_element_height)
        while height <= totalHeight:
            # driver.execute_script("arguments[0].scrollIntoView();", contact)
            # search_expression = '//div[@transformY="'+str(height)+'px" and contains(@class, "X7YrQ")]'
            all_contacts_elms = parent_scroll.find_elements_by_class_name("X7YrQ")
            for presentElm in all_contacts_elms:
                transformProp = presentElm.value_of_css_property("transform")

                tempProp = transformProp[22:]
                currentHeight = int(tempProp[:-1])
                # print(height)
                # print(currentHeight)
                nextHeight = height + 72
                # if height == nextHeight:

                if height == currentHeight:
                    # print("Matched Element")
                    text_element = presentElm.find_element_by_class_name("_3H4MS")
                    print(text_element.text)
                    contact_list.append(text_element.text)
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollIntoView();", presentElm)
            # search_expression = "//div[contains(@style='transform: translateY("+str(height)+"px);')]"
            # current_node = driver.find_element_by_xpath(search_expression)
            # text_element = current_node.find_element_by_class_name("_3NWy8")
            # print(text_element.text)
            # contact_list.append(text_element.text)

            height = height + 72
    finally:
        pass
def fetch_all_contacts_old():
    driver.find_element_by_xpath("/html/body/div[1]/div/div").click()
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    scroll_view = driver.find_element_by_class_name("rK2ei")
    size = scroll_view.size
    height = size["height"]
    last_height = driver.execute_script("return arguments[0].scrollHeight;", height)

    while True:
        scroll_view = driver.find_element_by_class_name("rK2ei")
        size = scroll_view.size
        height = size["height"]
        # Scroll down to bottom
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", height)

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        all_contacts = driver.find_elements_by_class_name("_3NWy8")
        for contact in all_contacts:
            print(contact.text)
        # Calculate new scroll height and compare with last scroll height
        scroll_view = driver.find_element_by_class_name("rK2ei")
        size = scroll_view.size
        height = size["height"]
        new_height = driver.execute_script("return arguments[0].scrollHeight;", height)
        if new_height == last_height:
            break
        last_height = new_height
def fetch_all_contacts():
    driver.find_element_by_xpath("/html/body/div[1]/div/div").click()
    contact_list = []
    # SCROLL_PAUSE_TIME = 0.5
    print("Fetching Contacts")
    # Get scroll height
    # scroll_view = driver.find_element_by_class_name("rK2ei")
    # size = scroll_view.size
    # height = size["height"]

    # all_contacts = driver.find_elements_by_class_name("_3NWy8")

    # recentList = driver.find_elements_by_xpath("//div[@class='_3NWy8']")
    try:
        parent_scroll_element_height = driver.find_elements_by_class_name("_1H6CJ")[0].value_of_css_property("height")

        print(parent_scroll_element_height)
        # print(len(all_contacts))
        height = 72
        parent_scroll_element_height = parent_scroll_element_height[:-2]
        totalHeight = int(parent_scroll_element_height)
        while height <= totalHeight:
            # driver.execute_script("arguments[0].scrollIntoView();", contact)
            # search_expression = '//div[@transformY="'+str(height)+'px" and contains(@class, "X7YrQ")]'
            all_contacts_elms = driver.find_elements_by_class_name("X7YrQ")
            for presentElm in all_contacts_elms:
                transformProp = presentElm.value_of_css_property("transform")

                tempProp = transformProp[22:]
                currentHeight = int(tempProp[:-1])
                # print(height)
                # print(currentHeight)
                nextHeight = height + 72
                # if height == nextHeight:

                if height == currentHeight:
                    # print("Matched Element")
                    text_element = presentElm.find_element_by_class_name("_3H4MS")
                    print(text_element.text)
                    contact_list.append(text_element.text)
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollIntoView();", presentElm)
            # search_expression = "//div[contains(@style='transform: translateY("+str(height)+"px);')]"
            # current_node = driver.find_element_by_xpath(search_expression)
            # text_element = current_node.find_element_by_class_name("_3NWy8")
            # print(text_element.text)
            # contact_list.append(text_element.text)

            height = height + 72
    finally:
        pass
        # buffer code - Go back to Normal WIndow (Reset Condition)
    driver.find_element_by_xpath(
        "/html/body/div[1]/div/div/div[2]/div[1]/span/div/span/div/header/div/div[1]/button/span").click()

    for this_contact in contact_list:
        # Go to Search Window
        driver.find_element_by_xpath("/html/body/div[1]/div/div").click()

        # all_contacts = driver.find_elements_by_class_name("_3NWy8")
        search_text_box = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div/div[2]/div[1]/span/div/span/div/div[1]/div/label/input")
        search_text_box.send_keys(this_contact)

        # recentList = driver.find_elements_by_xpath("//div[@class='_3NWy8']")
        try:
            parent_scroll_element_height = driver.find_elements_by_class_name("_1H6CJ")[0].value_of_css_property(
                "height")

            print(parent_scroll_element_height)
            # print(len(all_contacts))
            height = 72
            parent_scroll_element_height = parent_scroll_element_height[:-2]
            totalHeight = int(parent_scroll_element_height)
            while height <= totalHeight:
                # driver.execute_script("arguments[0].scrollIntoView();", contact)
                # search_expression = '//div[@transformY="'+str(height)+'px" and contains(@class, "X7YrQ")]'
                all_contacts_elms = driver.find_elements_by_class_name("X7YrQ")
                for presentElm in all_contacts_elms:
                    transformProp = presentElm.value_of_css_property("transform")

                    tempProp = transformProp[22:]
                    currentHeight = int(tempProp[:-1])
                    # print(height)
                    # print(currentHeight)
                    nextHeight = height + 72
                    # if height == nextHeight:

                    if height == currentHeight:
                        # print("Matched Element")
                        text_element = presentElm.find_element_by_class_name("_3H4MS")
                        print(text_element.text)
                        contact_list.append(text_element.text)
                        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollIntoView();", presentElm)
                # search_expression = "//div[contains(@style='transform: translateY("+str(height)+"px);')]"
                # current_node = driver.find_element_by_xpath(search_expression)
                # text_element = current_node.find_element_by_class_name("_3NWy8")
                # print(text_element.text)
                # contact_list.append(text_element.text)

                height = height + 72
        finally:
            pass

    print("Contacts Fetched")
def only_admin_can_send_msgs(group_name):
    for i in driver.find_elements(by.By.TAG_NAME, value="div"):
        if i.get_attribute('data-testid') == "chat-list-search":
            i.send_keys(keys.Keys.CONTROL + 'a')
            i.send_keys(group_name)
            time.sleep(2)
            break
    all_groups = []
    groups = [i for i in driver.find_elements(by.By.TAG_NAME, value="span") if i.get_attribute("title") == group_name]
    for group in groups:
        time.sleep(2)
        group.click()
        time.sleep(2)
        for j in driver.find_elements(by.By.TAG_NAME, value="header"):
            if j.get_attribute('data-testid') == "conversation-header":
                j.click()
        time.sleep(2)
        group_participants_text = driver.find_element(by.By.CLASS_NAME, value="AjtLy").text.replace(' ', '').split('·')
        if group_participants_text[0] == "Group":
            all_groups.append(group.text)

    driver.find_element(by.By.TAG_NAME, value="body").send_keys(keys.Keys.ESCAPE)
    time.sleep(1)
    driver.find_element(by.By.TAG_NAME, value="body").send_keys(keys.Keys.ESCAPE)
    time.sleep(1)
    for button in driver.find_elements(by.By.TAG_NAME, value="button"):
        if button.get_attribute('data-testid') == "icon-search-morph":
            button.click()
            button.click()

    return [*set(all_groups)]
    if group_found:
        driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/header/div[2]/div[1]/div").click()
        try:
            driver.find_element_by_xpath(
                "/html/body/div[1]/div/div/div[2]/div[3]/span/div/span/div/div/div[1]/div[4]/div[3]/div/div[1]/span").click()
            driver.find_element_by_xpath(
                "/html/body/div[1]/div/div/div[2]/div[3]/span/div/span/div/div/div[1]/div[2]/div/div/div[1]").click()
            chk_boxes = driver.find_elements_by_class_name("_19y4J")
            chk_boxes[1].click()
            driver.find_element_by_xpath("/html/body/div[1]/div/span[2]/div/div/div/div/div/div/div[3]/div[2]").click()
            only_admin_flag = True
        except:
            # Not a Group Admin
            pass

    return only_admin_flag
# --- In Development


send_msg('919974595905', "Hello, This is Test Message")


# cd C:/Program Files/BraveSoftware/Brave-Browser/Application && brave.exe --remote-debugging-port=9222 -user-data-dir="C:\Program Files\100 Days Of Python\Selenium Data"

