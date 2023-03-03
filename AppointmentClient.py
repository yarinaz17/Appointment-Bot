import logging
import time
import undetected_chromedriver as uc 

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome import options
from SinchClient import SinchClient
from configparser import ConfigParser

class AppointmentClient:

    def __init__(self) -> None:
        parser = ConfigParser()
        parser.read("config/config.ini")
        site_header = "AGENDAMENTOS"
        self.website_url = parser.get(site_header,'url')
        self.login_id = parser.get(site_header,'identification')
        self.sinch_client = SinchClient()
        logging.debug("Sinch client added - SMS mechanism is in use")

    def init_driver(self):
        # TODO : Add options to reduce RAM usage
        chrome_options = options.Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-application-cache")
        self.driver = uc.Chrome(chrome_options) 


    
    def close_popups(self):
        logging.debug("Closing popups...")
        accept_cookies_btn = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="j_idt68"]/span')))
        accept_cookies_btn.click()

        time.sleep(2)
        
        ok_btn = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.ID,'j_idt61')))
        ok_btn.click()

    def login(self):

        eftuar_btn = self.driver.find_element(by=By.ID,value="indexForm:j_idt29")
        eftuar_btn.click()
        
        id_text = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.ID,'scheduleForm:tabViewId:ccnum')))
        
        id_text.send_keys(self.login_id)

        birthdate_text = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.ID,'scheduleForm:tabViewId:dataNascimento')))
        
        birthdate_text.click()

        year = self.driver.find_element(by=By.XPATH, value='//*[@id="ui-datepicker-div"]/div/div/select[2]/option[100]')
        year.click()

        month = self.driver.find_element(by=By.XPATH, value='//*[@id="ui-datepicker-div"]/div/div/select[1]/option[3]')
        month.click()

        day = self.driver.find_element(by=By.XPATH, value='//*[@id="ui-datepicker-div"]/table/tbody/tr[3]/td[1]/a')
        day.click()

        pesquisar_btn = self.driver.find_element(by=By.ID, value="scheduleForm:tabViewId:searchIcon")
        pesquisar_btn.click()

        posto_consular_btn = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.ID,'scheduleForm:postcons_label')))
        posto_consular_btn.click()

        posto_tlv_btn = self.driver.find_element(by=By.XPATH,value='//*[@id="scheduleForm:postcons_panel"]/div/ul/li[2]')
        posto_tlv_btn.click()

        categoria_btn = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="scheduleForm:categato_label"]')))
        categoria_btn.click()

        identificacao_btn = self.driver.find_element(by=By.XPATH,value='//*[@id="scheduleForm:categato_panel"]/div/ul/li[3]')
        identificacao_btn.click()

        adicionar_btn = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="scheduleForm:bAddAto"]/span')))
        adicionar_btn.click()

        declaro_btn = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="scheduleForm:dataTableListaAtos:0:selCond"]/span')))
        declaro_btn.click()
        time.sleep(1)

        self.check_calendar()

    def check_calendar(self):
        while (1):
            calendarizar_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="scheduleForm:dataTableListaAtos:0:bCal"]/span')))
            calendarizar_btn.click()
            time.sleep(0.5)
            # Check if calendar shows up
            if (self.driver.find_element(by=By.XPATH, value='/html/body/form/div[4]/div[1]').is_displayed()):
                logging.info("Appointments are available - SMS is being sent")
                self.sinch_client.send_sms()
                break
            else:
                try:
                    close_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="scheduleForm:j_idt171"]/div[1]/a')))
                except:
                    self.restart()

                close_btn.click()
                time.sleep(0.5)

    def restart(self):
        self.driver.quit()
        time.sleep(1)
        self.init_driver()
        time.sleep(2)
        self.close_popups()
        self.login()

    def run(self):
        # Initialize selenium driver
        self.init_driver()

        # Open website
        self.driver.get(self.website_url)

        self.close_popups()
        self.login()