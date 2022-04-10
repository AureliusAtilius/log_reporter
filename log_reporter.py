from netmiko import ConnectHandler
import json, getpass


def load_config(config):
        # Load connection configuration from .JSON file
        with open(config) as json_file:
                config = json.load(json_file)
        return config

def get_creds():
        # Get logserver credentials
        username,pw= input("Username: "), getpass.getpass(prompt="Password: ", stream=None)
        return username,pw
        
def logger_connect():
        config = load_config(config.json)
        logserver= config['host1']
        fileshares= config['host2']
        username,pw=get_creds()

        # Login to logserver using Netmiko and creds

# Check logserver logs against fileshares

# Write to CSV file.

