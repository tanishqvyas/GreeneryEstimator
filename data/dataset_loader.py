import os
from PIL import Image
import random
import urllib.request
import cairo
import time


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

    ts = TileServer("SATELLITE")
    
    # Hardcoded for bangalore
    meta_data = {

        "begin_x":46863,
        "begin_y":30352,
        "end_x":46926,
        "end_y":30423,
        "zoom_level": 16
    }


    # Getting all the images of a region
    # For zoom level 15
    # By dividing it into sub-tiles
    # Tile data from : https://www.maptiler.com/google-maps-coordinates-tile-bounds-projection/
    # Code Inspiration : https://docs.microsoft.com/en-us/bingmaps/rest-services/imagery/get-a-static-map 

    count = 0

    for i in range(meta_data["begin_x"],meta_data["end_x"]+1):
        for j in range(meta_data["begin_y"], meta_data["end_y"]+1):

            # Fetching the map-tile for satellite image
            im_s = ts.tile_as_image(i,j,meta_data["zoom_level"])
            # im_r = tr.tile_as_image(i,j,meta_data["zoom_level"])



            # Saving the image/satellite
            path_s = os.path.join("images","satellite","sector"+str(count)+".jpg")
            im_s.save(path_s)


            count += 1
    
