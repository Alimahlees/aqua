import sqlite3
from datetime import datetime, timedelta
import subprocess
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

class dimension():
    def __init__(self,title):
        self.title = title

class graph():
    def __init__(self,title,data,units,color,dimensions):
        self.title = title
        self.data  = data
        self.units = units
        self.color = color
        self.dimensions = dimensions

def createGraphs():
    graphs = list()

    d = []
    d.append(dimension("Room"))
    d.append(dimension("Water"))
    graphs.append(graph("Temperature", "aqua.Temperature", "degrees (F)", "", d))

    d = []
    d.append(dimension("Humidity"))
    graphs.append(graph("Humidity", "aqua.Humidity", "percent", "#55ffaa", d))

    d = []
    d.append(dimension("Left"))
    d.append(dimension("Right"))
    d.append(dimension("Tank"))
    d.append(dimension("Room"))
    graphs.append(graph("Lighting", "aqua.Light", "percent", "", d))

    d = []
    d.append(dimension("pH"))
    graphs.append(graph("pH", "aqua.tankpH", "ppi", "#ffaa55", d))

    d = []
    d.append(dimension("Level"))
    graphs.append(graph("Water Level", "aqua.tankLevel", "inches", "#aaff55", d))

    return graphs

def createSystemGraphs():
    graphs = list()

    d = []
    graphs.append(graph("CPU Utilization", "system.cpu"," "," ",d))
    graphs.append(graph("System Load", "system.load"," "," ",d))
    graphs.append(graph("Disk I/O", "system.io"," "," ",d))
    graphs.append(graph("System Memory", "system.ram"," "," ",d))

    return graphs

def getIP(card):
    proc = subprocess.Popen("/sbin/ifconfig",stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        if card in str(line):
            line = proc.stdout.readline()
            line = str(line)
            #im sorry
            ip = line.split(" ")[11][5:]

    return ip

def insert(d):
    d = str(d)
    d = d.replace("b","")
    d = d.replace("'","")
    d = d.split(",")
    d = list(map(float,d))
    conn = sqlite3.connect('/mnt/data.db')
    c = conn.cursor()

    try:
        c.execute('''CREATE TABLE data
        (date TEXT,
        rtemp REAL,
        humid REAL,
        wtemp REAL,
        wlevl INTEGER,
        rlite INTEGER,
        llite INTEGER,
        blite INTEGER,
        tlite INTEGER,
        ph    REAL)''')

    except:
        print("data.db already created")

    now = datetime.now().replace(microsecond=0)

    c.execute('''INSERT INTO data VALUES
            ('%s',   %f,   %f,   %f,   %d,   %d,   %d,   %d,   %d,   %f)''' % (
              now, d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8]))

    conn.commit()
    conn.close()

def plot():
    data  = "wlevl"
    begin = "2016-11-26"
    end   = "2016-11-26"

    conn = sqlite3.connect('/mnt/data.db')
    c = conn.cursor()

    c.execute("SELECT date FROM data WHERE date LIKE '%%%s%%'" % (begin))
    x = c.fetchall()
    c.execute("SELECT %s FROM data WHERE date LIKE '%%%s%%'" % (data,begin))
    y = c.fetchall()

    fig, ax = plt.subplots(1)
    fig.autofmt_xdate()

    x = mpl.dates.datestr2num(x)

    data = data.split(',')
    for i in range(len(data)):
        ny = [z[i] for z in y]
        plt.plot(x,ny,label=data[i])

    plt.legend()
    ax.set_xlim(x[0][0],x[-1][0])
    plt.gcf().autofmt_xdate()

    plt.savefig('/home/pi/Desktop/aqua/static/plot_bmh.png',bbox_inches='tight')

    conn.close()


