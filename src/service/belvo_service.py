import os
import requests
from requests.auth import HTTPBasicAuth
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

def get_flows(response):
        total_inflows = 0.0
        total_outflows = 0.0
        for transaction in response.get("results",[]):
            amount = transaction.get("amount",0)
            if transaction.get("type") == "INFLOW":
                total_inflows += amount
            elif transaction.get("type") == "OUTFLOW":
                total_outflows += amount
        return {
            "total_inflows": total_inflows,
            "total_outflows": total_outflows,
            "net_balance": total_inflows - total_outflows,
        }




class BelvoService:
    def __init__(self):
        self.api_key = os.getenv("BELVO_API_KEY")
        self.secret_key = os.getenv("BELVO_SECRET_KEY").strip('"\'')
        self.base_url = os.getenv("BELVO_API_URL")
        self.auth = HTTPBasicAuth(self.api_key,  self.secret_key);

    def get_banks(self):
        try:
            response = requests.get(
                f"{self.base_url}/institutions/",
                auth=self.auth,
            )
            response.raise_for_status()

            response_data = response.json()
            banks_data = (
                response_data.get("results") 
                if isinstance(response_data, dict) 
                else response_data if isinstance(response_data, list) 
                else []
            )
            return {
                "data": banks_data,
            }

        except requests.exceptions.RequestException as e:
            error_detail = getattr(e.response, "text", str(e))
            raise ValueError(f"Error al consultar Belvo: {error_detail}")

    def get_links(self, page: int, page_size: int):
        try:
            params = {
                "page": page,
                "page_size": page_size
            }
            response = requests.get(
                f"{self.base_url}/links/",
                auth=self.auth,
                params=params
            )
            response.raise_for_status()

            response_data = response.json()
            banks_data = (
                response_data.get("results") 
                if isinstance(response_data, dict) 
                else response_data if isinstance(response_data, list) 
                else []
            )
            return {
                "data": banks_data,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "count":response_data.get("count"),
                }
            }
        except requests.exceptions.RequestException as e:
            error_detail = getattr(e.response, "text", str(e))
            raise ValueError(f"Error al consultar Belvo: {error_detail}")

    def get_accounts(self, link_id:str):
        try:
            response = requests.get(
                f"{self.base_url}/accounts",
                auth=self.auth,
                params={"link":link_id}
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener cuentas: {e.response.text}")
            raise

    def get_transactions(self,link: str, account: str, page: int, page_size: int):
        try:
            params = {
                "link": link,
                "account": account,
                "page": page,
                "page_size": page_size
            }
            response = requests.get(
                f"{self.base_url}/transactions/",
                auth=self.auth,
                params=params
            )
            response.raise_for_status()

            response_data = response.json()
            account_flows = get_flows(response_data)

            transactions_data = (
                response_data.get("results") 
                if isinstance(response_data, dict) 
                else response_data if isinstance(response_data, list) 
                else []
            )


            return {
                "":response_data.get("results"),
                "data": transactions_data,
                "account_flows": account_flows,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "count":response_data.get("count"),
                }
            }
        except requests.exceptions.RequestException as e:
            error_detail = getattr(e.response, "text", str(e))
            raise ValueError(f"Error al consultar Belvo: {error_detail}")