import pandas as pd
from log_reporter import get_creds

def readSpreadsheet():
    xlsxFile=input("Enter log report filename:")
    required_cols=[0,1,4]
    toDeleteRAW={}
    toDeleteARC={}
    try:
        sheetdata= pd.read_excel(xlsxFile,usecols=required_cols)
        
        for ind in sheetdata.index:
            if sheetdata['Set to Delete'][ind] == "*":
                if sheetdata['Project'][ind] not in toDeleteRAW:
                    toDeleteRAW[sheetdata['Project'][ind]]=[]
                    toDeleteRAW[sheetdata['Project'][ind]].append(sheetdata['Log'][ind])
                else:
                    toDeleteRAW[sheetdata['Project'][ind]].append(sheetdata['Log'][ind])
        
        #TODO: check if log needs to be removed from archived folders.
        return toDeleteRAW,toDeleteARC

        
    except:
        print("Unable to read file. Check filename and path.")
    

#TODO: function for deleting logs.
if __name__ =="__main__":
    readSpreadsheet()
