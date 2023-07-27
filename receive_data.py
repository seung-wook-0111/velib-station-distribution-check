from threading import Timer
import requests
import pandas as pd
from time import localtime, strftime
 
def update():
    getData()
    set_timer()
  
def set_timer():
    Timer(durationinsec, update).start()
  
def main():
    update()
 
def getData():
    global iteration
    nbrows = 1500
    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel%40parisdata&rows=" + str(nbrows) + "&facet=overflowactivation&facet=creditcard&facet=kioskstate&facet=station_state"
    mytime = strftime("%Y-%m-%d %H:%M:%S", localtime())
 
    resp = requests.get(url)
    if resp.status_code != 200:
        print(mytime, " - ", iteration, " - Error receiving data")
    else:
        data = resp.json()
        dff = pd.DataFrame(columns =['Timer', 'ID', 'Station Code', '# of Ebikes', '# of Mech Bikes',
                                     '# of Docks Available',
                                     'Timestamp'])
        for rec in data['records']:
            dff.loc[len(dff)] = [mytime, 
                                 rec['recordid'],
                                 rec['fields']['stationcode'],
                                 rec['fields']['ebike'],
                                 rec['fields']['mechanical'],
                                 rec['fields']['numdocksavailable'],
                                 rec['record_timestamp']
                                 ]
        if int(data['nhits']) > 0:
            with open("velib19-2.csv", 'a') as f:
                dff.to_csv(f, header=True, index=False)
            print(mytime, " - ", iteration, " - Data fetched. # of rows: ", data['nhits'])
        else:
            print(mytime, " - ", iteration, " - No data.")
    iteration = iteration + 1
 
durationinsec = 1*60*10
iteration = 144
main()