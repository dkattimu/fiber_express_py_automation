import os
import platform, datetime, toml, time
from functools import reduce
import logging, json, shutil
#networkDr = "/Volumes/CorpFin/ERM/Model Risk"
logging.basicConfig(level=logging.DEBUG)

def get_last_modified_time(file_name: str) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(os.path.getmtime(file_name))


def format_time(dt: datetime.datetime) -> str:
    res = str(dt).replace(":", "_")
    res = res.replace(" ", "..")
    return res

def check_for_updates(prod_dir: str, 
                     env_file_name:str ="_mrm.model_env.toml",
                      msg_dispatch_port: int = 5003
                      ) -> bool:
    """determine if the file to be watched has different timestamp than the 
    reference time-stamp.

    Args:
        file_name (str): watched file
    """
    env_file_full_name = os.path.join(prod_dir,env_file_name)
    config = toml.load(env_file_full_name)
    watch_files = config['change_management']['watch_file']
    #watch files are relative to prod_dir
    watch_files = [os.path.join(prod_dir, file_) for file_ in watch_files]
    last_modified_times = config['change_management']['model_last_modified'] 
    updated_last_modified_times = [format_time(get_last_modified_time(file_)) for file_ in watch_files]
    logging.info(f"updated last modified-times: {updated_last_modified_times}")
    res = [(index, updated_time != time_, updated_time, time_ + "||" + updated_time) for index, (_, time_, updated_time) in 
    enumerate(zip(watch_files, last_modified_times, updated_last_modified_times))]
    #print(f"res !!!!!!!!!!!! {res}")
    changed_list = [(index, changed, updated_time, chk) for index, changed, updated_time,chk  in res if changed]
    was_updated =  len(changed_list) > 0 # updated if  at least one tr
    curl_cmd:str = "" 
    if was_updated:
        logging.info(f"Model update detected in... {prod_dir}")
        #save current version of _mrm.env.toml
        backup_filename = env_file_name.split(".toml")[0]+'_('+ format_time(datetime.datetime.now()) + ").toml" 
        backup_file_full_name = os.path.join(prod_dir, backup_filename)
        #cmd = f"cp {env_file_full_name} {backup_file_full_name}"
        #print("-----",cmd)
        #os.system(cmd)
        shutil.move(env_file_full_name, backup_file_full_name)

        config['change_management']['model_last_modified'] =  updated_last_modified_times 
        with open(env_file_full_name, "w") as f:
            toml.dump(config, f)

        id = config["info"]["id"]
        last_modified = changed_list[0][2]
        curl_cmd = get_command(
            model_id=id, modified_time=last_modified, 
            validated="No", msg_dispatch_port=msg_dispatch_port
            )
    return curl_cmd


def get_command(model_id: str, modified_time: str, validated: str, msg_dispatch_port: int) -> str:
    return f"curl -X PUT http://localhost:{msg_dispatch_port}/update/{model_id}/{modified_time}/{validated}"


def autheticate_run():
    pass


def run(prod_dir: str,env_file_name:str, port: int, watch_interval: int = 2):
    while True:
        time.sleep(watch_interval)
        print(f"Watching {prod_dir}: {datetime.datetime.now()}")   
        curl_cmd =check_for_updates(prod_dir, env_file_name, port)
        
        if len(curl_cmd) > 0:
            print(f"About to execute... {curl_cmd}")
            stream = os.popen(curl_cmd)
            output = stream.read()
        else:
            print(f"No change detected...{datetime.datetime.now()}")

# TODO:
# Support multiple files watch for each environment
# Support multiple environments
# support multiprocessing for watching

if __name__ == "__main__":
    networkDir = "/Volumes/erm/Model Risk Management"
    config_file = "/Users/mm51630/Documents/Programming/GO/Demo/fiber_express_py_automation/automation.config.json" # "../../automation.config.json"
    env_file_name = "_mrm.model_env.toml"

    
    with open(config_file) as config_file_obj:
        config = json.load(config_file_obj)
        MSG_DISPATCHER_PORT = int(config["PORTS"]["MSG_DISPATCHER"])
        
    prod_dir ="/Volumes/erm/Model Risk Management/Automation/sample-model"
    #prod_dir = "/Users/mm51630/Documents/Programming/JS/Demo/sample-model"
    PORT = 3003 # PORT for msg-dispatcher
    INTERVAL = 5
    run(prod_dir=prod_dir, env_file_name=env_file_name, port=MSG_DISPATCHER_PORT, watch_interval=INTERVAL)
 
