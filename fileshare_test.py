from log_reporter import share_logs, load_config
import json

config = load_config("config.json")

fileshares= config['hosts']['host2']['log_filepath']
projects= config["Projects"]

logs= share_logs(projects, fileshares)

with open("logstest.json","w") as outfile:
                json.dump(logs, outfile)