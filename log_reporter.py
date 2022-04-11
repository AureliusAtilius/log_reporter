from netmiko import ConnectHandler
from subprocess import check_output
import json, getpass


def load_config(configJSON):
        # Load connection configuration from .JSON file
        with open(configJSON) as json_file:
                config = json.load(json_file)
        return config

def get_creds():
        # Get logserver credentials
        username,pw= input("Username: "), getpass.getpass(prompt="Password: ", stream=None)
        return username,pw

def share_logs(projects, fileshares):
        # Get logs off network shares.
        share_logs={}
        for i in projects:
                log_list= (check_output("dir {} /b /a-d".format(fileshares["log_filepath"]), shell=True).decode()).split()
                share_logs[i]=log_list
        return share_logs




def logger_connect():
        # Connect to logserver and retrieve dictinary of logs by project number
        config = load_config("config.json")
        
        logserver= config['hosts']['host1']
        fileshares= config['hosts']['host2']
        projects= config["Projects"]
        username,pw=get_creds()
        logs={"raw":{},"ark":{}}
        # Login to logserver using Netmiko and creds
        try:

                logserver_connection= ConnectHandler(**{"device_type":logserver["device_type"],"host":logserver["hostname"],"username":username, "password":pw})
        except Exception:
                print("SSH connection failed on",logserver["hostname"])

        # Send command listing logs
        try:
                for i in projects:
                        raw_logs= logserver_connection.send_command("ls -lh {} | awk '{{print $9}}'".format(logserver["raw_log_path"]+i))
                        logs["raw"][i]=raw_logs.split()
                        ark_logs= logserver_connection.send_command("ls -lh {} | awk '{{print $9}}'".format(logserver["ark_log_path"]+i))
                        logs["ark"][i]=ark_logs.split()
                logserver_connection.disconnect()
                return logs
        except:
                print("Command failed")
                logserver_connection.disconnect()
        


# Check logserver logs against fileshares

# Write to CSV file.

if __name__=="__main__":
        print(logger_connect())