import os
import time
import base64
import datetime
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common import by, keys
from selenium.webdriver.support import expected_conditions as EC


class whatsappautomation:
    def __init__(self):
        if os.path.exists("WhatsApp Automation Data"):
            if not os.path.exists("WhatsApp Automation Data/WhatsApp Media"):
                os.mkdir("WhatsApp Automation Data/WhatsApp Media")
            if not os.path.exists("WhatsApp Automation Data/Browser Data"):
                os.mkdir("WhatsApp Automation Data/Browser Data")
        else:
            os.mkdir("WhatsApp Automation Data")
            os.mkdir("WhatsApp Automation Data/WhatsApp Media")
            os.mkdir("WhatsApp Automation Data/Browser Data")

        self.BROWSER_DATA = os.getcwd() + r"\WhatsApp Automation Data\Browser Data"
        self.WHATSAPP_MEDIA_PATH = os.getcwd() + r"\WhatsApp Automation Data\WhatsApp Media"

        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument(f"--user-data-dir={self.BROWSER_DATA}")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.driver.switch_to.window(self.driver.window_handles[0])
    # child methods
    def whatsapp_authenticated(self):
        self.driver.get('https://web.whatsapp.com/')
        # time.sleep(100)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((by.By.CSS_SELECTOR, "div[data-testid='qrcode']")))
            return False
        except exceptions.TimeoutException:
            return True
    def base64_encode(self, path_to_file):
        """Input : string of whole path of file including extension; Output : A list with 1st element is base64 encoded
         string and second element is string of file extension without dot(.)."""
        with open(rf'{path_to_file}', 'rb') as data:
            base_message = base64.b64encode(data.read())
        extension = path_to_file.split('.')[-1]
        return [base_message, extension]
    def base64_decode(self, encoded_list):
        """Input : a list with first element of encoded base64 string and second element as string of file extension
        without dot(.); Output : a string of the whole path of the file decoded and saved with file extension."""
        file_name = str(datetime.datetime.now()).replace('-', '').replace(':', '').replace(' ', '_').split('.')[0]
        decoded_data = base64.b64decode(encoded_list[0])
        with open(rf'{self.WHATSAPP_MEDIA_PATH}/{file_name}.{encoded_list[1]}', 'wb') as data:
            data.write(decoded_data)
        return f'{self.WHATSAPP_MEDIA_PATH}/{file_name}.{encoded_list[1]}'
    def open_contact(self, contact_number):
        """Opens the chat of the given contact number"""
        self.driver.get(f'https://web.whatsapp.com/send/?phone={contact_number}&type=phone_number&app_absent=0')
        try:
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((by.By.CSS_SELECTOR, "div[data-testid='conversation-info-header']")))
            return True
        except exceptions.TimeoutException:
            return False
    def open_group(self, group_id):
        """Opens the chat of the group from given group ID"""
        self.driver.get(f'https://web.whatsapp.com/accept?code={group_id}')
        try:
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((
                by.By.CSS_SELECTOR, "div[data-testid='conversation-info-header']")))
            return True
        except exceptions.TimeoutException:
            return False
    def get_contact_number_from_name(self, contact_name):
        """Returns the contact number of the saved contact from the whatsapp account"""
        all_contacts = []
        self.driver.find_element(by.By.CSS_SELECTOR, value="div[data-testid='chat-list-search']").send_keys(
            keys.Keys.CONTROL + 'a' + keys.Keys.CONTROL + contact_name)
        time.sleep(2)
        contacts = self.driver.find_elements(by.By.CSS_SELECTOR, value=f"span[title='{contact_name}']")

        for contact in contacts:
            contact.click()
            time.sleep(1)
            self.driver.find_element(by.By.CSS_SELECTOR, value="header[data-testid='conversation-header']").click()
            time.sleep(1)
            if contact_name in [i.text for i in
                                self.driver.find_elements(by.By.CSS_SELECTOR, value="span.selectable-text[dir='auto']")]:
                for i in [i.text for i in
                          self.driver.find_elements(by.By.CSS_SELECTOR, value="span.selectable-text[dir='auto']")]:
                    if i.split('+')[0] == "":
                        all_contacts.append(i.replace(' ', '').replace('+', ''))
            else:
                print("Given Contact Name is the group name.")

        self.driver.find_element(by.By.TAG_NAME, value="body").send_keys(keys.Keys.ESCAPE)
        time.sleep(1)
        self.driver.find_element(by.By.TAG_NAME, value="body").send_keys(keys.Keys.ESCAPE)
        time.sleep(1)
        self.driver.find_element(by.By.CSS_SELECTOR, value="button[data-testid='icon-search-morph']").click()
        self.driver.find_element(by.By.CSS_SELECTOR, value="button[data-testid='icon-search-morph']").click()

        return [*set(all_contacts)]
    # main methods
    def create_group(self, group_name, group_contacts):
        """Creates a group with given group name and adds the participants given in the list in the group"""
        self.driver.find_element(by.By.CSS_SELECTOR, value="div[aria-label='Menu']").click()
        time.sleep(1)
        self.driver.find_element(by.By.CSS_SELECTOR, value="div[aria-label='New group']").click()
        time.sleep(1)
        for contact in group_contacts:
            self.driver.find_element(by.By.CSS_SELECTOR, value="input[data-testid='inputarea']").send_keys(
                keys.Keys.CONTROL + 'a' + keys.Keys.CONTROL + contact)
            time.sleep(1)
            self.driver.find_element(by.By.CSS_SELECTOR, value="div[data-testid='contact-list-key']").click()
        time.sleep(1)
        self.driver.find_element(by.By.CSS_SELECTOR, value="span[data-testid='arrow-forward']").click()
        time.sleep(1)
        self.driver.find_element(by.By.CSS_SELECTOR, value="div[data-testid='pluggable-input-body']").send_keys(group_name)
        time.sleep(1)
        self.driver.find_element(by.By.CSS_SELECTOR, value="span[data-testid='checkmark-medium']").click()
        time.sleep(1)
        self.driver.find_element(by.By.TAG_NAME, value="body").send_keys(keys.Keys.ESCAPE)
    def send_msg(self, message):
        """Send any text message to the chat. (requires the chat to be opened prior)"""
        self.driver.find_element(by.By.CSS_SELECTOR, "div[data-testid='conversation-compose-box-input']").send_keys(message)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((by.By.CSS_SELECTOR, "span[data-testid='send']"))).click()
        except exceptions.TimeoutException:
            print("Message size is too long to send.")
            return False
        try:
            WebDriverWait(self.driver.find_elements(by.By.CSS_SELECTOR, value="div.message-out")[-1], 10).until(
                EC.presence_of_element_located(
                    (by.By.CSS_SELECTOR, "span[data-testid='msg-dblcheck'],span[data-testid='msg-check']")))
        except exceptions.TimeoutException:
            print("Message is taking too long to send.")
            return False
        self.driver.find_element(by.By.TAG_NAME, value="body").send_keys(keys.Keys.ESCAPE)
        return True
    def send_file(self, filepath):
        """Send any file (audio/video/photo/doc) to the chat. (requires the chat to be opened prior)"""
        if os.path.isfile(filepath):
            filepath = self.base64_decode(self.base64_encode(filepath))
            self.driver.find_element(by.By.CSS_SELECTOR, value="span[data-testid='clip']").click()
            file_extension = filepath.split('.')[-1].lower()
            if file_extension in ['mp4', 'mkv', 'avi', 'mov', '3gp', 'jpeg', 'png', 'jpg']:
                self.driver.find_element(by.By.CSS_SELECTOR, value="input[accept='image/*,video/mp4,video/3gpp,video/quicktime']").send_keys(filepath)
            else:
                self.driver.find_element(by.By.CSS_SELECTOR, value="input[accept='*']").send_keys(filepath)
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((by.By.CSS_SELECTOR, "span[data-testid='send']"))).click()
            except exceptions.TimeoutException:
                print("File is longer than 16 mb.")
                return False
            time.sleep(1)

            message_container = self.driver.find_elements(by.By.CSS_SELECTOR, value="div.message-out")[-1]
            try:
                WebDriverWait(message_container, 10).until(EC.presence_of_element_located(
                    (by.By.CSS_SELECTOR, "span[data-testid='msg-dblcheck'],span[data-testid='msg-check']")))
            except exceptions.TimeoutException:
                print("File is taking too long to send")
                return False
            self.driver.find_element(by.By.TAG_NAME, value="body").send_keys(keys.Keys.ESCAPE)
            return True
        else:
            print("No File Found at the mentioned path.")
            return False


whatsapp_automate = whatsappautomation()
whatsapp_automate.whatsapp_authenticated()
# chat_opened = whatsapp_automate.open_group(group_id="LsAqTkpl6gWKqDMSX8GO6g")
# chat_opened = whatsapp_automate.open_contact(contact_number="7874908622")
# if chat_opened:
#     # filepath = r"C:\Users\chait\Downloads\Masters in Germany\Makkar Speaking PDF.pdf"
#     message = "The tanker with number GJ06XX1107 has been *Started to Load* at IOCL - Kandla. The driver's mobile number is# 9998887776. Thank You. TriGas"
#
#     sent = whatsapp_automate.send_file(filepath=filepath)
#     sent = whatsapp_automate.send_msg(message=message)
#
#     print(sent)
