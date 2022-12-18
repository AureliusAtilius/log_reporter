import pandas as pd
import paramiko
from log_reporter import get_creds, load_config

#Funtion for reading spreadsheet
def readSpreadsheet():
    print("-----------------------------------------------")
    xlsxFile=input("Enter log report filename:")

    #Specify which collumns will be looked at
    required_cols=[0,1,2,4]


    toDeleteRAW={}
    toDeleteARC={}

    try:
        sheetdata= pd.read_excel(io=xlsxFile,usecols=required_cols)
        for ind in sheetdata.index:
        #Find logs that are set to delete
            if sheetdata['Set to Delete'][ind]:
                if sheetdata['Project'][ind] not in toDeleteRAW:
                    toDeleteRAW[sheetdata['Project'][ind]]=[]
                    toDeleteRAW[sheetdata['Project'][ind]].append(sheetdata['Log'][ind])
                else:
                    toDeleteRAW[sheetdata['Project'][ind]].append(sheetdata['Log'][ind])
                #Check if log is archived.
                if sheetdata['Archived'][ind]:
                    if sheetdata['Project'][ind] not in toDeleteARC:
                        toDeleteARC[sheetdata['Project'][ind]]=[]
                        toDeleteARC[sheetdata['Project'][ind]].append(sheetdata['Log'][ind])
                    else:
                        toDeleteARC[sheetdata['Project'][ind]].append(sheetdata['Log'][ind])

        return toDeleteRAW,toDeleteARC

        
    except Exception as ex:
        print(ex)
    
def logRemover(toDeleteRAW,toDeleteARC):
    print('running')

    username,pw =get_creds()
    config=load_config("config.json")
    hostname=config["hosts"]["host1"]["hostname"]
    rawPath=config['hosts']['host1']["raw_log_path"]
    arcPath=config['hosts']['host1']["ark_log_path"]
    try:
        port = '22'
         
        # created client using paramiko
        client = paramiko.SSHClient()
         
        # connecting paramiko using host
        # name and password
        client.load_system_host_keys()
        client.connect(hostname=hostname, port=22, username=username,
                       password=pw)

        #iterate over raw logs to remove them.
        for prj in toDeleteRAW:
            for log in prj:
                #substitute find command for rm -Rf when testing
                #command= f"rm -RF {rawPath}/{prj}/{log}"
                command =f"find {rawPath}/{prj} -name {log}"

                # below line command will actually
                # execute in your remote machine
                (stdin, stdout, stderr) = client.exec_command(command)
         
                # redirecting all the output in cmd_output
                # variable
                cmd_output = stdout.read()
                
                
                # create file which will read our
                # cmd_output and write it in output_file
                output_file="output.txt"
                if cmd_output:
                    with open(output_file, "w+") as file:
                        output="Project "+prj+" "+log+" "+str(cmd_output)
                        file.write(output)
        
        #iterate over archived logs to remove them.
        for prj in toDeleteARC:
            for log in prj:
                #substitute find command for rm -Rf when testing
                #command= f"rm -RF {arcPath}/{prj}/{log}.7z"
                command =f"find {arcPath}/{prj} -name {log}.7z"

                # below line command will actually
                # execute in your remote machine
                (stdin, stdout, stderr) = client.exec_command(command)
         
                # redirecting all the output in cmd_output
                # variable
                cmd_output = stdout.read()
                
                
                # create file which will read our
                # cmd_output and write it in output_file
                output_file="output.txt"
                if cmd_output:
                    with open(output_file, "w+") as file:
                        output="Project "+prj+" "+log+" "+str(cmd_output)
                        file.write(output)
    except Exception as ex:
        print(ex)
        client.close()
    finally:
        client.close()


if __name__ =="__main__":
    toDeleteRAW,toDeleteARC=readSpreadsheet()
    logRemover(toDeleteRAW=toDeleteRAW,toDeleteARC=toDeleteARC)