import os
from PIL import Image
import random
import urllib.request
import cairo
import time
import math
import pandas as pd

# for finding lat long
import mercantile

# To get place name
import geopy
from geopy.geocoders import Nominatim

def getName(lat, lon):
    
    locator = Nominatim(user_agent="myGeocoder")
    coordinates = str(lat)+", "+str(lon)
    location = locator.reverse(coordinates)
    location = str(location).split(",")

    return location[0]


class TileServer(object):

    def __init__(self, layers):
        self.imdict = {}
        self.surfdict = {}
        self.layers = layers
        self.path = './'
        self.urltemplate = 'http://ecn.t{4}.tiles.virtualearth.net/tiles/{3}{5}?g=0'
        self.layerdict = {'SATELLITE': 'a', 'HYBRID': 'h', 'ROADMAP': 'r'}

    def tiletoquadkey(self, xi, yi, z):
        quadKey = ''
        for i in range(z, 0, -1):
            digit = 0
            mask = 1 << (i - 1)
            if(xi & mask) != 0:
                digit += 1
            if(yi & mask) != 0:
                digit += 2
            quadKey += str(digit)
        return quadKey

    def loadimage(self, fullname, tilekey):
        im = Image.open(fullname)
        self.imdict[tilekey] = im
        return self.imdict[tilekey]

    def tile_as_image(self, xi, yi, zoom):
        tilekey = (xi, yi, zoom)
        result = None
        try:
            result = self.imdict[tilekey]
        except:
            filename = '{}_{}_{}_{}.jpg'.format(zoom, xi, yi, self.layerdict[self.layers])
            fullname = self.path + filename
            try:
                result = self.loadimage(fullname, tilekey)
            except:
                server = random.choice(range(1,4))
                quadkey = self.tiletoquadkey(*tilekey)
                print(quadkey)
                url = self.urltemplate.format(xi, yi, zoom, self.layerdict[self.layers], server, quadkey)
                print("Downloading tile %s to local cache." % filename)
                urllib.request.urlretrieve(url, fullname)
                result = self.loadimage(fullname, tilekey)
        return result


        


if __name__ == "__main__":

    # Start the clock
    start_time = time.time()

    ts = TileServer("ROADMAP")
    
    # Hardcoded for bangalore
    meta_data = {

        "begin_x":46863,
        "begin_y":30352,
        "end_x":46926,
        "end_y":30423,
        "zoom_level": 16
    }


    # Empty Data dict
    my_data ={

        "Sector":[],
        "Lat":[],
        "Long":[],
        "Name":[],
        "Greenery":[]
    }



    # Getting all the images of a region
    # For zoom level 15
    # By dividing it into sub-tiles
    # Tile data from : https://www.maptiler.com/google-maps-coordinates-tile-bounds-projection/
    # Code Inspiration : 
    # https://docs.microsoft.com/en-us/bingmaps/rest-services/imagery/get-a-static-map 
    # https://discourse.metabase.com/t/satellite-map/7969
    # https://docs.microsoft.com/en-us/bingmaps/rest-services/imagery/imagery-metadata

    count = 0

    for i in range(meta_data["begin_x"],meta_data["end_x"]+1):
        for j in range(meta_data["begin_y"], meta_data["end_y"]+1):

            # Fetching the map-tile for satellite image
            # im_s = ts.tile_as_image(i,j,meta_data["zoom_level"])

            print("The current count : ",count)

            # Finding the lat long
            co_ordinates = mercantile.ul(i, j, meta_data["zoom_level"])
            print(co_ordinates.lng , co_ordinates.lat)

            # Storing the data
            my_data["Sector"].append("sector"+str(count))
            my_data["Lat"].append(co_ordinates.lat)
            my_data["Long"].append(co_ordinates.lng)
            my_data["Name"].append(getName(co_ordinates.lat, co_ordinates.lng))
            my_data["Greenery"].append(0)


            # Saving the images/satellite
            # path_s = os.path.join("images","roadmap","sector"+str(count)+".png")
            # im_s.save(path_s)



            if(count % 10 == 0):
                path_to_csv = os.path.join("csv","greenery_percentage.csv")
                df = pd.DataFrame.from_dict(my_data)
                df.to_csv(path_to_csv, index=False)


            # Time wait
            if(count % 100 == 0):
                print("Sleeping now >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                time.sleep(69)
            if(count % 1000 == 0):
                print("Mega sleep >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                time.sleep(200)


            count += 1

    # Making a dataframe
    df = pd.DataFrame.from_dict(my_data)
    
    # Saving as csv
    path_to_csv = os.path.join("csv","greenery_percentage.csv")
    df.to_csv(path_to_csv, index=False)
    print("--- %s seconds ---" % (time.time() - start_time))



    
