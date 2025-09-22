import warnings
warnings.simplefilter(action="ignore",category=FutureWarning)
import atexit
import time
import csv
from pynvml import *
import os


def Get_new_logfile_name(base_name="GPU_m_log", extension=".csv", folder=""):
    i = 0
    while True:
        if i == 0:
            filename = f"{base_name}{extension}"
        else:
            filename = f"{base_name}{i}{extension}"
        full_path = os.path.join(folder, filename)
        if not os.path.exists(full_path):
            return filename
        i += 1


save_dirct = "C:/Users/D/Desktop/P/GPU Monitor/LOG_FILES"
filename = Get_new_logfile_name(folder = save_dirct)
full_path = os.path.join(save_dirct,filename)

csvfile = open(full_path, mode = "w", newline = '')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(["Timestamp","GPU TEMP °", "Power Consumption W", "Utilization %", "GPU name"])

print(f"\nLogging Data to : {filename} at : {save_dirct}\n")

nvmlInit()

try:
    while True:

        handler = nvmlDeviceGetHandleByIndex(0)

        GPUname = nvmlDeviceGetName(handler)

        temp = nvmlDeviceGetTemperature(handler,0)

        powercons = nvmlDeviceGetPowerUsage(handler) / 1000

        util = nvmlDeviceGetUtilizationRates(handler)

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        csvwriter.writerow([timestamp,temp,powercons,util.gpu,GPUname])
        csvfile.flush()

        print(f"---------------------------------  {GPUname}  ---------------------------------")
        print(f"GPU Temperature : {temp}° \nPower consumption : {powercons} W \nUtilization : {util.gpu} % \n---------------------------------------------------------------------------------------------")
        time.sleep(2)
except KeyboardInterrupt:
    print("Shutting down Monitoring.....\n")
finally:
    nvmlShutdown()
    csvfile.close()
    print(f"Data Logged to {filename} at : {save_dirct} at {time.strftime("%Y-%m-%d %H:%M:%S")}")

