import os
import sys

import mapnik

from google_projection import GoogleProjection


def render_tiles(m, projection, tile_projection, bbox, tile_dir, minZoom=1, maxZoom=18):
    if not os.path.isdir(tile_dir):
         os.mkdir(tile_dir)

    gprj = GoogleProjection(maxZoom + 1)

    ll0 = (bbox[0], bbox[3])
    ll1 = (bbox[2], bbox[1])

    for z in range(minZoom, maxZoom + 1):
        px0 = gprj.fromLLtoPixel(ll0, z)
        px1 = gprj.fromLLtoPixel(ll1, z)

        # check if we have directories in place
        zoom = "%s" % z
        if not os.path.isdir(tile_dir + zoom):
            os.mkdir(tile_dir + zoom)

        for x in range(int(px0[0]/256.0), int(px1[0]/256.0)+1):
            # Validate x co-ordinate
            if (x < 0) or (x >= 2**z):
                continue

            # check if we have directories in place
            str_x = "%s" % x

            if not os.path.isdir(tile_dir + zoom + '/' + str_x):
                os.mkdir(tile_dir + zoom + '/' + str_x)

            for y in range(int(px0[1]/256.0), int(px1[1]/256.0)+1):
                # Validate x co-ordinate
                if (y < 0) or (y >= 2**z):
                    continue

                str_y = "%s" % y
                tile_uri = tile_dir + zoom + '/' + str_x + '/' + str_y + '.png'
                # Submit tile to be rendered into the queue
                render_tile(m, projection, tile_projection, tile_uri, x, y, z)


def render_tile(m, projection, tile_projection, tile_uri, x, y, z):
    # Calculate pixel positions of bottom-left & top-right
    p0 = (x * 256, (y + 1) * 256)
    p1 = ((x + 1) * 256, y * 256)

    # Convert to LatLong (EPSG:4326)
    l0 = tile_projection.fromPixelToLL(p0, z)
    l1 = tile_projection.fromPixelToLL(p1, z)

    # Convert to map projection (e.g. mercator co-ords EPSG:900913)
    c0 = projection.forward(mapnik.Coord(l0[0], l0[1]))
    c1 = projection.forward(mapnik.Coord(l1[0], l1[1]))

    bb = mapnik.Envelope(c0.x, c0.y, c1.x, c1.y)
    render_size = 256

    m.resize(render_size, render_size)
    m.zoom_to_box(bb)
    m.buffer_size = 128

    # Render image with default Agg renderer
    im = mapnik.Image(render_size, render_size)
    mapnik.render(m, im)
    im.save(tile_uri, 'png256')
