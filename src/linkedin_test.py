import time

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pandas as pd
import random


class Scraper:
    scraping_done = False

    def __init__(self, personal_page):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome("drivers/chromedriver.exe", options=options)
        self.driver.implicitly_wait(2)
        self.personal_page = personal_page
        self.connection_names = []
        self.awards = []
        self.certifications = []
        self.articles = []
        self.events = []
        self.group_names = []
        self.instititions = {"work": [], "education": [], "volunteering": []}
        self.names = []
        self.places = []
        self.platforms = []
        self.postitions = []
        self.projects = []
        self.publications = []
        self.skills = []
        self.topics = []
        self.templates = pd.read_excel('templates.xlsx')

    def __del__(self):
        self.driver.close()

    def send_message(self):
        website_name = "https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom" \
                       "%2Fnotifications%2F&fromSignIn=true&trk=cold_join_sign_in "
        username = "legendary.lion2@gmail.com"
        password = "mergcubicicleta9"

        self.driver.get(website_name)
        self.driver.find_element_by_id("username").send_keys(username)
        self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_xpath("//button[text()='Sign in']").click()

        search_text = "Maior Valentin"

        self.driver.find_element_by_class_name("search-global-typeahead__input").send_keys(search_text)
        self.driver.find_element_by_class_name("search-global-typeahead__input").send_keys(Keys.ENTER)

        self.driver.find_element_by_xpath("//span[contains(@class,'entity-result__title-text')]").click()

        name_elem = self.driver.find_element_by_class_name("inline.t-24.t-black.t-normal.break-words")
        print(name_elem.text)

        self.driver.find_element_by_xpath("//a[contains(@class,'message-anywhere-button')]").click()

        message = "Salutari de la Ovidiu si Miruna. Am reusit sa rezolvam treaba pe LinkedIn fara OCR. \n\nP.S.: " \
                  "Acesta este un mesaj trimis automat. ;) "
        message_box = self.driver.find_element_by_xpath("//div[contains(@class,'msg-form__contenteditable')]")
        message_box.send_keys(message)
        self.driver.find_element_by_xpath("//button[text()='Send']").send_keys(Keys.ENTER)
        time.sleep(10)

    def get_person_name(self):
        return self.driver.find_element_by_xpath("//h1[contains(@class, 'text-heading')]").text

    def get_person_role(self):
        return self.driver.find_elements_by_xpath("//h1[contains(@class, 'text-heading')]/../../div")[1].text

    def make_breakers_common_connections(self):
        try:
            icebreakers_common_connections = list(
                self.templates.where(self.templates['category'] == "common connections")['template'])
            icebreakers_common_connections = [x for x in icebreakers_common_connections if type(x) == type(" ")]
            to_return = []
            for i in range(len(icebreakers_common_connections)):
                string = str(icebreakers_common_connections[i]).replace('<connection name>', self.connection_names[0])
                string = string.replace('<connection name>', self.connection_names[0])
                if string.find('<') == -1:
                    to_return.append(string)
            return to_return
        except:
            return None

    def make_breakers_experience(self):
        icebreakers_experience = list(self.templates.where(self.templates['category'] == "experience")['template'])
        icebreakers_experience = [x for x in icebreakers_experience if type(x) == type(" ")]
        to_return = []
        for i in range(len(icebreakers_experience)):
            string = str(icebreakers_experience[i])
            val = random.randint(0, len(self.instititions['work']) - 1)
            string = string.replace('<institution>', self.instititions['work'][val])
            if string.find('<') == -1:
                to_return.append(string)
        return to_return

    def make_breakers_volunteering_experience(self):
        icebreakers_experience = list(
            self.templates.where(self.templates['category'] == "volunteer experience")['template'])
        icebreakers_experience = [x for x in icebreakers_experience if type(x) == type(" ")]
        to_return = []
        for i in range(len(icebreakers_experience)):
            string = str(icebreakers_experience[i])
            val = random.randint(0, len(self.instititions['volunteering']) - 1)
            string = string.replace('<institution>', self.instititions['volunteering'][val])
            if string.find('<') == -1:
                to_return.append(string)
        return to_return

    def get_institutions_education(self, title):
        elements = title.find_elements_by_xpath("../../ul/li//div/div/h3")
        for elem in elements:
            self.instititions["education"].append(elem.text)

    def get_institutions_volunteering(self, title):
        elements = title.find_elements_by_xpath("../../ul/li//div/h4/span[contains(@class, 'secondary-title')]")
        for elem in elements:
            self.instititions["volunteering"].append(elem.text)

    def get_institutions_work(self, title):
        elements = title.find_elements_by_xpath("../../ul/li//div/div//p[contains(@class, 'secondary-title')]")
        for elem in elements:
            self.instititions["work"].append(elem.text)

    def get_certifications(self, title):
        elements = title.find_elements_by_xpath("../../ul/li//div/h3")
        for elem in elements:
            self.certifications.append(elem.text)

    def get_connection_names(self):
        try:
            text = self.driver.find_element_by_xpath(
                "//a[contains(@class,'app-aware-link')]//span[@aria-hidden]").text
            try:
                self.connection_names.append(text.split(' both know ')[1].split(',')[0].split(' and')[0])
            except IndexError:
                self.connection_names.append(text.split('mutual connection')[1].replace("s: ", "").split(',')[0].split(' and')[0])
        except:
            text = self.driver.find_element_by_xpath(
                "//p[contains(@class, 'pv-highlight-entity__secondary-text')]").text
            if str(text).find(" both know") != -1:
                self.connection_names.append(text.split(' both know ')[1].split(',')[0].split(' and')[0])

    def get_categories(self):
        self.get_connection_names()

    @staticmethod
    def filter_text(text):
        return "\n".join([s for s in str(text).split("\n") if " " in s])

    def search_for_person(self, name):
        self.driver.find_element_by_class_name("search-global-typeahead__input").send_keys(name)
        self.driver.find_element_by_class_name("search-global-typeahead__input").send_keys(Keys.ENTER)

        search_result_xpath = "//span[contains(@class,'entity-result__title-text')]"
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, search_result_xpath)))
        self.driver.find_element_by_xpath(search_result_xpath).click()

    def login(self):
        website_name = "https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom" \
                       "%2Fnotifications%2F&fromSignIn=true&trk=cold_join_sign_in "
        username = "legendary.lion2@gmail.com"
        password = "mergcubicicleta9"

        self.driver.get(website_name)
        self.driver.find_element_by_id("username").send_keys(username)
        self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_xpath("//button[text()='Sign in']").click()
        try:
            self.driver.find_element_by_class_name('btn__secondary--large-muted').click()
        except:
            pass

    def go_to_page(self, url):
        self.driver.get(url)

    def search_news(self, text):
        self.driver.find_elements_by_tag_name("button")[-1].find_element_by_tag_name("div").click()
        self.driver.find_element_by_xpath("//input[@type='text']").send_keys(text, Keys.ENTER)
        self.driver.find_element_by_xpath("//div[@role='navigation']").find_element_by_xpath(
            "//a[text()='News']").click()
        text = self.driver.find_elements_by_xpath("//div[@role='heading']")[1].text
        link = self.driver.find_elements_by_xpath("//div[@role='heading']/../../..")[1].get_attribute("href")
        print(text)
        print(link)

        return {"link": link, "text": text}

    def get_profile_data(self, sections=None):
        if sections is None:
            sections = []

        self.login()

        # self.search_for_person("Maior Valentin")
        self.driver.get(self.personal_page)

        wrapper_id = "main"
        WebDriverWait(self.driver, 10000).until(ec.presence_of_element_located((By.ID, wrapper_id)))

        show_more_buttons = self.driver.find_elements_by_xpath("//button[contains(text(),' more experiences')]")
        while len(show_more_buttons) != 0:
            show_more_buttons[0].click()
            show_more_buttons = self.driver.find_elements_by_xpath("//button[contains(text(),' more experiences')]")

        show_more_buttons = self.driver.find_elements_by_xpath("//a[text()='see more']")
        show_more_buttons += self.driver.find_elements_by_xpath("//button[text()='see more']")
        show_more_buttons += self.driver.find_elements_by_xpath("//button[span[text()='Show more']]")
        for show_more_button in show_more_buttons:
            try:
                show_more_button.click()
            except ElementNotInteractableException:
                pass
            except ElementClickInterceptedException:
                pass
        header_text = self.driver.find_element_by_xpath("//*[contains(@class,'profile-background-image')]/..").text
        self.get_categories()
        profile_text = self.filter_text(header_text)
        titles = self.driver.find_elements_by_xpath("//section[contains(@class,'pv-profile-section')]//h2")
        for title in titles:
            if title.text in sections:
                if title.text == "Education":
                    self.get_institutions_education(title)
                elif title.text == "Experience":
                    self.get_institutions_work(title)
                elif title.text == "Volunteer experience":
                    self.get_institutions_volunteering(title)
                elif title.text == "Licenses & certifications":
                    self.get_certifications(title)
                profile_text += ("\n" + self.filter_text(title.find_element_by_xpath("../..").text))

        profile_text.replace("+", ", ").replace("see more", "").replace("See all details", "").replace(
            "Show fewer experiences", "")
        return profile_text

    def get_profile_links(self):
        self.driver.get(self.personal_page)
        link_xpath = "//span[contains(@class,'entity-result__title-text')]/a"
        links = []
        new_links = [l.get_attribute("href") for l in self.driver.find_elements_by_xpath(link_xpath)]
        links.extend(new_links)
        page_counter = 2
        while len(new_links) != 0:
            self.driver.get(self.personal_page + "&page=" + str(page_counter))
            new_links = [l.get_attribute("href") for l in self.driver.find_elements_by_xpath(link_xpath)]
            links.extend(new_links)
            page_counter += 10

        return [l for l in links if "linkedin.com/in/" in l]
