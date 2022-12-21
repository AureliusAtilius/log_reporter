from netmiko import ConnectHandler
from subprocess import check_output
from datetime import date
import json, getpass
import xlsxwriter
import sys


def load_config(configJSON):
        # Load connection configuration from .JSON file
        with open(configJSON) as json_file:
                config = json.load(json_file)
        return config

def get_creds():
        # Get logserver credentials
        username,pw= input("Username: "), getpass.getpass(prompt="Password: ", stream=None)
        return username,pw

def share_logs(projects, fileshares_path):
        # Get logs off network shares.
        share_logs={}
        for i in projects:
                log_list= (check_output("dir {} /b /a-d".format(fileshares_path+i), shell=True).decode()).split()
                share_logs[i]=log_list
        return share_logs

def logger_connect(config):
        # Connect to logserver and retrieve dictionary of logs by project number
        config = load_config("config.json")
        username,pw=get_creds()
        
        for host in config['hosts']:
                logserverIP= config['hosts'][host]["IP"]
                fileshares= config['hosts'][host]["log_filepath"]
                projects= config["Projects"]
                hostname= config["hosts"][host]["hostname"]
                raw_log_path=config["hosts"][host]["raw_log_path"]
                ark_log_path=config["hosts"][host]["ark_log_path"]
                logs={"raw":{},"ark":{}}
                device_type=config['hosts'][host]["device_type"]
                # Login to logserver using Netmiko and creds
                try:

                        logserver_connection= ConnectHandler(**{"device_type":device_type,"host":logserverIP,"username":username, "password":pw})
                        try:
                                for i in projects:
                                        raw_logs= logserver_connection.send_command("ls -lh {} | awk '{{print $9}}'".format(raw_log_path+i))
                                        logs["raw"][i]=raw_logs.split()
                                        ark_logs= logserver_connection.send_command("ls -lh {} | awk '{{print $9}}'".format(ark_log_path+i))
                                        logs["ark"][i]=ark_logs.split()
                                logserver_connection.disconnect()
                        
                        except:
                                print("Command failed")
                                logserver_connection.disconnect()
                                sys.exit()
                        
                except Exception:
                        print("SSH connection failed on ",hostname,". Check authentication.")
                        sys.exit()  
                shares= share_logs(config["Projects"], fileshares)
                spreadsheet_writer(logs,share_logs=shares,hostname=hostname)
# Create Spreadsheet
def spreadsheet_writer(server_logs, share_logs,hostname):
        file_name= str(date.today())+"_"+hostname+".xlsx"
        workbook = xlsxwriter.Workbook(file_name)
        
        # Create worksheet 1 with raw logs on log server
        worksheet1=workbook.add_worksheet("Raw Logs")
        worksheet1.write(0,0, "Project")
        worksheet1.write(0,1, "Log")
        worksheet1.write(0,2,"Archived")
        worksheet1.write(0,3,"On Shares")
        worksheet1.write(0,4, "Set to Delete")

        dict_writer(server_logs,share_logs,worksheet1)
        
        workbook.close()   

def dict_writer(server_logs, share_logs, worksheet):
        row=1
        col=0
        for key in server_logs['raw'].keys():
                for log in server_logs['raw'][key]:
                        worksheet.write(row,col, key )
                        worksheet.write(row, col+1, log)
                        if log+'.7z' in server_logs['ark'][key]:
                                worksheet.write(row,col+2, "*")
                        if log+".7z" in share_logs[key]:
                                worksheet.write(row,col+3, "*")
                        row+=1
        row=str(row)
        #Apply data verification in Set to Delete column so only * is used.
        worksheet.data_validation(f"E2:E{row}", {'validate': 'list',"source": ["*"]})

def main():
        config=load_config("config.json")
        logs=logger_connect(config)
        


        


if __name__=="__main__":
        main()