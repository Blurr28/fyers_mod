from fyers_apiv3 import fyersModel
import webbrowser
import requests
import yaml
import json

class Data:
    def __init__(self):
        self._login()
    

    def _login(self):
        with open("auth.yaml", "r") as file:
            response = yaml.safe_load(file)
        
        client_id = response["client_id"]
        access_token = response["access_token"]
        fyers = fyersModel.FyersModel(client_id=client_id, is_async=False,token = access_token, log_path="./api_logs/")
        new_response = fyers.get_profile()
        if (new_response["code"] != 200):
            print("error :",response["message"])
            print("regenerating access token...")
            self._regenerate_access_token_with_refresh(response)
        else:
            print("Login Succesful")
            print("Name :", new_response["data"]["name"])
            print("Email ID:", new_response["data"]["email_id"])
        

    def _regenerate_access_token(self, response : dict):
        client_id = response["client_id"]
        secret_key = response["secret_key"]
        redirect_uri = response["redirect_uri"]
        response_type = response["response_type"]
        state = response["state"]
        grant_type = response["grant_type"]

        session = fyersModel.SessionModel(
            client_id= client_id,
            secret_key = secret_key,
            redirect_uri= redirect_uri,
            response_type= response_type,
            grant_type=grant_type
        )

        new_response = session.generate_authcode()
        webbrowser.open(new_response)
        auth_code = input("Enter Auth Code :")
        session.set_token(auth_code)
        new_response = session.generate_token()

        if new_response.get("code") != 200:
            print("error :", new_response.get("message", "Unknown error"))
        else:
            print("Access Token Generated")
            self._update_response(response=response, new_response=new_response)
            self._login()

    def _regenerate_access_token_with_refresh(self, response : dict):
        url = "https://api-t1.fyers.in/api/v3/validate-refresh-token"
        headers = {"Content-Type" : "application/json"}
        data = {
            "grant_type": response["refresh_grant_type"],
            "appIdHash": response["appIdHash"],
            "refresh_token": response["refresh_token"],
            "pin": str(response["pin"])
        }

        try:

            new_response = requests.post(url, headers=headers, data = json.dumps(data))
            new_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            print("regenerating new refresh token and access token...")
            self._regenerate_access_token(response=response)
            return
        
        print("Access Token Generated")
        new_response = new_response.json()
        self._update_response(response=response, new_response=new_response)
        self._login()


    def _update_response(self, response : dict ,new_response : dict):
        response.update(new_response)
        with open("auth.yaml", "w") as file:
            yaml.dump(response, file)



            

        