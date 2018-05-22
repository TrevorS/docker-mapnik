# Adapted from https://github.com/mapnik/mapnik/wiki/GettingStartedInPython
#              with https://github.com/mapnik/mapnik/issues/3258 to work with current bindings

import os
import sys

from math import pi
from math import cos
from math import sin
from math import log
from math import exp
from math import atan

import mapnik

DEG_TO_RAD = pi/180
RAD_TO_DEG = 180/pi

def minmax (a,b,c):
    a = max(a,b)
    a = min(a,c)
    return a

class GoogleProjection:
    def __init__(self,levels=18):
        self.Bc = []
        self.Cc = []
        self.zc = []
        self.Ac = []
        c = 256
        for d in range(0,levels):
            e = c/2;
            self.Bc.append(c/360.0)
            self.Cc.append(c/(2 * pi))
            self.zc.append((e,e))
            self.Ac.append(c)
            c *= 2

    def fromLLtoPixel(self,ll,zoom):
         d = self.zc[zoom]
         e = round(d[0] + ll[0] * self.Bc[zoom])
         f = minmax(sin(DEG_TO_RAD * ll[1]),-0.9999,0.9999)
         g = round(d[1] + 0.5*log((1+f)/(1-f))*-self.Cc[zoom])
         return (e,g)

    def fromPixelToLL(self,px,zoom):
         e = self.zc[zoom]
         f = (px[0] - e[0])/self.Bc[zoom]
         g = (px[1] - e[1])/-self.Cc[zoom]
         h = RAD_TO_DEG * ( 2 * atan(exp(g)) - 0.5 * pi)
         return (f,h)

def render_tile(tile_uri, x, y, z):
    #print tile_uri,":",z,x,y
    # Calculate pixel positions of bottom-left & top-right
    p0 = (x * 256, (y + 1) * 256)
    p1 = ((x + 1) * 256, y * 256)

    # Convert to LatLong (EPSG:4326)
    l0 = tileproj.fromPixelToLL(p0, z);
    l1 = tileproj.fromPixelToLL(p1, z);

    # Convert to map projection (e.g. mercator co-ords EPSG:900913)
    c0 = prj.forward(mapnik.Coord(l0[0],l0[1]))
    c1 = prj.forward(mapnik.Coord(l1[0],l1[1]))

    bb = mapnik.Envelope(c0.x,c0.y, c1.x,c1.y)
    render_size = 256
    m.resize(render_size, render_size)
    m.zoom_to_box(bb)
    m.buffer_size = 128

    # Render image with default Agg renderer
    im = mapnik.Image(render_size, render_size)
    mapnik.render(m, im)
    im.save(tile_uri, 'png256')

def render_tiles(bbox, tile_dir, minZoom=1,maxZoom=18):

    if not os.path.isdir(tile_dir):
         os.mkdir(tile_dir)

    gprj = GoogleProjection(maxZoom+1)

    ll0 = (bbox[0],bbox[3])
    ll1 = (bbox[2],bbox[1])

    for z in range(minZoom,maxZoom + 1):
        px0 = gprj.fromLLtoPixel(ll0,z)
        px1 = gprj.fromLLtoPixel(ll1,z)

        # check if we have directories in place
        zoom = "%s" % z
        if not os.path.isdir(tile_dir + zoom):
            os.mkdir(tile_dir + zoom)
        for x in range(int(px0[0]/256.0),int(px1[0]/256.0)+1):
            # Validate x co-ordinate
            if (x < 0) or (x >= 2**z):
                continue
            # check if we have directories in place
            str_x = "%s" % x
            if not os.path.isdir(tile_dir + zoom + '/' + str_x):
                os.mkdir(tile_dir + zoom + '/' + str_x)
            for y in range(int(px0[1]/256.0),int(px1[1]/256.0)+1):
                # Validate x co-ordinate
                if (y < 0) or (y >= 2**z):
                    continue
                str_y = "%s" % y
                tile_uri = tile_dir + zoom + '/' + str_x + '/' + str_y + '.png'
                # Submit tile to be rendered into the queue
                render_tile(tile_uri, x, y, z)

    print(zoom + ' ' + str_x + ' ' + str_y)

m = mapnik.Map(2800, 1800)
mapnik.load_map(m, 'stylesheet.xml')

# http://en.wikipedia.org/wiki/Extreme_points_of_the_United_States#Westernmost
# TODO: switch this to include all 50 states
top = 49.3457868 # north lat
left = -124.7844079 # west long
right = -66.9513812 # east long
bottom =  24.7433195 # south lat

bbox = (left, bottom, right, top)
prj = mapnik.Projection(m.srs)
tileproj = GoogleProjection()

render_tiles(bbox, '/output/counties/', minZoom=7, maxZoom=9)
