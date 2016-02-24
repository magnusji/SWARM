from numpy import *
from matplotlib.pyplot import *
import math
from mpl_toolkits.basemap import Basemap
import datetime as dt
from time import mktime

class Readdata():
    def __init__(self,filename, filename_gps):
        self.filename = filename #self.infile.readlines();
        self.filename_gps = filename_gps 

    def set_var(self): 
        self.infile = open(self.filename,'r');
        self.Date = []; self.Latitude = []; self.Longitude = []; self.electrondensity = []
        for line in self.infile:
            words = line.split()
            self.Date.append(words[1]); self.Latitude.append(words[4]); self.Longitude.append(words[5]); self.electrondensity.append(words[10]); #getting the data from the data set, and setting variables
        self.infile.close()
        
    def alltime(self):
        n = len(self.Date)
        self.swarm_time = []
        for i in range(n):
            self.swarm_time.append(dt.datetime.strptime(self.Date[i], "%Y-%m-%dT%H:%M:%S.%f"))

        self.swarm_time_sec = zeros(len(self.swarm_time))
        for i in range(len(self.swarm_time)):
            self.swarm_time_sec[i] = mktime(self.swarm_time[i].timetuple()) + self.swarm_time[i].microsecond/1e6
        print self.swarm_time_sec

    def distance(self): #calculating the distance from the gps to the satellite using Haversine formula
        self.Svalbardlat = 78.15; self.Svalbardlong = (16.04); #position of gps 
        lat1 = math.radians(self.Svalbardlat); lon1 = math.radians(self.Svalbardlong)
	R = 6371000
	self.distances = []
        self.indices = []
        self.electron = []
        count = 0
        count2 = 0
        for i in range(len(self.Latitude)):
		self.Latitude[i] = float(self.Latitude[i])
		self.Longitude[i] = float(self.Longitude[i])
        	lat2 = math.radians(self.Latitude[i])
                lon2 = math.radians(self.Longitude[i])
                dlat = lat2-lat1
                dlon = lon2-lon1

                a = math.sin(dlat/2.0)**2 + math.cos(lat1)* math.cos(lat2)*math.sin(dlon/2.0)**2
                c = 2.0*math.atan2(math.sqrt(a), math.sqrt(1-a))
                distance = R*c
                count2 += 1
                if distance<=600000.0:
                    self.distances.append(distance)
                    self.indices.append(i)
                    self.electron.append(float(self.electrondensity[i])) #electron density when in range
                    count += 1 #counting the points measured when the satellite is in range
        
        print ( count, count2)
        figure()
        plot(self.indices,self.electron, 'b.')

    def makemap(self): #for setting up a map and plotting positions of the satellite
        figure()
        map = Basemap(projection='merc', lat_0=78.15, lon_0=16.04,
                      resolution = 'l', area_thresh = 1000.0,
                      llcrnrlon=-20, llcrnrlat=70,
                      urcrnrlon=50, urcrnrlat=85) #setting up the base map
 
        map.drawcoastlines()
        map.drawcountries()
        map.fillcontinents(color='coral')
        map.drawmapboundary()
        
        map.drawmeridians(np.arange(0, 360, 5)) #adding longitude lines every 5 deg
        map.drawparallels(np.arange(-90, 90, 5)) #adding latitude lines
        map.plot(16.04,78.15,'k*',latlon='true') #adding position of gps
        for i in range(len(self.indices)):
            k = self.indices[i]
            map.plot(self.Longitude[k],self.Latitude[k], 'r.',latlon='true') #adding the positions of the satellite every time it is within range


    def set_var_gps(self): 
        self.infile_gps = open(self.filename_gps,'r');
        firstline = self.infile_gps.readline()
        self.year_gps = []; self.plat = []; self.plong = [];
        for line in self.infile_gps:
            item = line.rstrip()
            words = line.split()
            self.year_gps.append(words[0]); self.plat.append(float(words[6])); self.plong.append(words[7]); #getting the data from the data set, and setting variables
        #print self.plat
        self.infile_gps.close()

            
        




a = Readdata('./Data/SW_PREL_EFIA_LP_1B_20131229T000000_20131229T235959_0102.txt', './Data/tec.dat') ;  a.set_var(); a.distance();a.makemap(); a.alltime();a.set_var_gps()
figure()
plot(a.plong, a.plat, 'b-', 16.04,78.15, 'r*')
show()                        

