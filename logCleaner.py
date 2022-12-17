import pandas as pd

from log_reporter import get_creds

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
    

#TODO: function for deleting logs.
'''def logRemover(toDeleteRAW):
    selection = input("Input 1 to print logs to delete. n\Input 2 to delete logs. n\Input 3 to cancel")
    if selection in ["1","2","3"]:
        
        if 

    for log in toDeleteRAW:'''

if __name__ =="__main__":
    results=readSpreadsheet()
    print(results)