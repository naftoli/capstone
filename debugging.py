# import json
# import requests
# def set_tokens():
#     manager_url = "https://dev-inm1j600yp4jk16p.us.auth0.com/authorize/?audience=capstone&client_id=U2SPlOSDU4AWFmxPsnYro73MRTQPtGl7&client_secret=drZDTXsmbgapjoJjxyTgkTyBYaQO-oG-h7Fbz1u35KAk-pcTe8MzZRMKeT7FEw6M&response_type=token&redirect_uri=https://mashpia.com/udacity_login"
#     reg_user_url = "https://dev-inm1j600yp4jk16p.us.auth0.com/authorize/?audience=capstone&client_id=U2SPlOSDU4AWFmxPsnYro73MRTQPtGl7&client_secret=drZDTXsmbgapjoJjxyTgkTyBYaQO-oG-h7Fbz1u35KAk-pcTe8MzZRMKeT7FEw6M&response_type=token&redirect_uri=https://mashpia.com/udacity_login"
#
#     # set the user credentials
#     username = "naftolir@gmail.com"
#     password = "Naftoli8770!"
#
#     # send a POST request to the authentication endpoint
#     response = requests.post(manager_url, json={"username": username, "password": password})
#     print(response)
#     exit()
#     data = json.loads(response.text)
#     manager_token = data['access_token']
#     print(manager_token)
#
# set_tokens()
import requests

# Define the Auth0 endpoint for token issuance
url = 'https://dev-inm1j600yp4jk16p.us.auth0.com/oauth/token'

# Define the required parameters for token issuance
params = {
    'grant_type': 'client_credentials',
    'client_id': 'U2SPlOSDU4AWFmxPsnYro73MRTQPtGl7',
    'client_secret': 'drZDTXsmbgapjoJjxyTgkTyBYaQO-oG-h7Fbz1u35KAk-pcTe8MzZRMKeT7FEw6M',
    'audience': 'https://dev-inm1j600yp4jk16p.us.auth0.com/api/v2/'
}

# Send a POST request to the token issuance endpoint
response = requests.post(url, data=params)

# Extract the access token from the response JSON object
access_token = response.json()

print(access_token)

# Print the access token
#print(f'Access token: {access_token}')
