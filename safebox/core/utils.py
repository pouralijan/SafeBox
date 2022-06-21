import os

def get_dev_name(path="/dev/", removable=True):
    dev_name = [f"{file}" for file in os.listdir(path) if file.startswith("sd") and file[-1] not in [str(i) for i in range(9)]]
    dev_name.sort()

    if removable:
        dev_name = [dev for dev in dev_name if open(f"/sys/block/{dev}/removable", "r").read().strip() == "1"]
    
    dev_name = [f"{path}{dev}" for dev in dev_name]

    return dev_name