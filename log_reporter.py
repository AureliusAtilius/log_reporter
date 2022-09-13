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
                try:
                        for i in projects:
                                raw_logs= logserver_connection.send_command("ls -lh {} | awk '{{print $9}}'".format(logserver["raw_log_path"]+i))
                                logs["raw"][i]=raw_logs.split()
                                ark_logs= logserver_connection.send_command("ls -lh {} | awk '{{print $9}}'".format(logserver["ark_log_path"]+i))
                                logs["ark"][i]=ark_logs.split()
                        logserver_connection.disconnect()
                
                except:
                        print("Command failed")
                        logserver_connection.disconnect()
                        sys.exit()
                return logs
        except Exception:
                print("SSH connection failed on",logserver["hostname"],". Check authentication.")
                sys.exit()  



# Create Spreadsheet
def spreadsheet_writer(server_logs, share_logs):
        file_name= str(date.today())+".xlsx"
        headers=["Project","Log","Set to Delete","On server"]
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


def main():
        config=load_config("config.json")
        logs=logger_connect(config)
        shares_logs= share_logs(config["Projects"], config["hosts"]["host2"]["log_filepath"])
        spreadsheet_writer(logs, shares_logs)


        


if __name__=="__main__":
        main()