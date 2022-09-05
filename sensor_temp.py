#! /usr/binpython3


import os
import requests
from requests.adapters import HTTPAdapter, Retry
import glob
import time
import datetime
import graph_temps
from creds import o_w_m_token,lat,lon,base_dir,output_loc


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

device_folder = glob.glob(base_dir+'28*')[0]
device_file = device_folder + '/w1_slave'

output_scrape_file_name = 'scraped_temps.csv'
output_inside_file_name = 'inside_temps.csv'
output_scrape = output_loc+output_scrape_file_name
output_inside = output_loc+output_inside_file_name
output_pi = output_loc+'pi_temp.csv'

req_url = 'https://api.openweathermap.org/data/2.5/weather?lat='+str(lat)+'&lon='+str(lon)+'&appid='+o_w_m_token+'&units=imperial'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0/5.0 + 32.0
        temp_time = time.time()
    return temp_time, temp_f #,temp_c


def scrape_temp():
    session = requests.Session()
    retry = Retry(connect = 3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://',adapter)
    session.mount('http://',adapter)
    req_json = session.get(req_url).json()
    temp_like = req_json['main']['feels_like']
    hPa = req_json['main']['pressure']
    humidity = req_json['main']['humidity']    
    wind_sp  = req_json['wind']['speed']
    w_code = req_json['weather'][0]['id']
    return temp_like, wind_sp, w_code, hPa, humidity


def get_pi_temp():
    with open('/sys/class/thermal/thermal_zone0/temp','r') as f:
        pt = round(float(f.read())/1000 * 9/5 + 32,1) 
        return pt


def write_temp():
    write_time, write_temp = read_temp()
    wrt_str = str(write_time)+','+str(write_temp)+'\n'
    tl, ws, wc, hPa, humidity = scrape_temp()
    scrape_str = str(write_time)+','+str(tl)+','+str(ws)+','+str(wc)+','+str(hPa)+','+str(humidity)+'\n'
    ptstr = str(write_time)+','+str(get_pi_temp())+'\n'
    with open(output_scrape, 'a') as f:
        f.writelines([scrape_str])
    with open(output_inside, 'a') as g:
        g.writelines([wrt_str])
    with open(output_pi, 'a') as h:
        h.writelines([ptstr])


write_temp()
graph_temps.plot_temps()




