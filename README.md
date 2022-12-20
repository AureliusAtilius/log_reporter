Log Reporter:
Connects to Linux logging server to create report of logs.

Log Cleaner:
After a user selects logs to delete in the report by placing a "*" in the "Set to Delete" column, 
the Log Cleaner will read the spreadsheet and delete the marked logs.
Uncomment the the "rm -RF" command on lines 67 and 93 when you are ready to delete.
Output.txt file is generated containing the command output of the remote server when run.