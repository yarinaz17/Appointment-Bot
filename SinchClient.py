import logging
import requests

from configparser import ConfigParser

class SinchClient:

    def __init__(self) -> None:
        parser = ConfigParser()
        config_header = "SINCH"
        parser.read("config/config.ini")
        self.service_plan_id = parser.get(config_header,'service_plan_id')
        self.api_token = parser.get(config_header,'token')
        self.sinch_number = parser.get(config_header,'sinch_number')
        self.destination_number = parser.get(config_header,'destination_number')
        self.api_url = parser.get(config_header,'api_url')
        

    def send_sms(self):
        servicePlanId = self.service_plan_id
        apiToken = self.api_token
        sinchNumber = self.sinch_number
        toNumber = self.destination_number
        url = self.api_url + servicePlanId + "/batches"
        payload = {
            "from": sinchNumber,
            "to": [
                toNumber
            ],
            "body": "Appointments for cartao are available: https://agendamentosonline.mne.gov.pt/AgendamentosOnline/index.jsf"
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + apiToken
        }

        response = requests.post(url, json=payload, headers=headers)

        data = response.json()
        logging.info(f"SMS JSON :{data}")
