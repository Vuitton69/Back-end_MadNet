import requests
from cryptography.hazmat.bindings.openssl import binding
from stem import Signal
from stem.control import Controller

def renew_tor_connection():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

def run_traffic_script_through_tor():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}

    # Make the HTTP request through the Tor connection
    # the following line contains your traffic script
    response = session.get("https://raw.githubusercontent.com/DmodvGH/Back-end_MadNet/main/tester.py")
    # print the response text
    print(response.text)

if __name__ == "main":
    renew_tor_connection()
    run_traffic_script_through_tor()