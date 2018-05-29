import mapnik

from tilesets import GoogleProjection
from tilesets import render_tiles

from extents import BOUNDING_BOX

m = mapnik.Map(2800, 1800)
mapnik.load_map(m, '/opt/stylesheets/states.xml')
mapnik.register_fonts('/opt/fonts')

projection = mapnik.Projection(m.srs)
tile_projection = GoogleProjection()

render_tiles(
    m=m,
    projection=projection,
    tile_projection=tile_projection,
    bbox=BOUNDING_BOX,
    tile_dir='/opt/output/states/',
    minZoom=4,
    maxZoom=6,
)
