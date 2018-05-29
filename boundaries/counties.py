import mapnik

from tilesets import render_tiles
from google_projection import GoogleProjection
from extents import BOUNDING_BOX

m = mapnik.Map(2800, 1800)
mapnik.load_map(m, '/opt/stylesheets/counties.xml')
mapnik.register_fonts('/opt/fonts')

projection = mapnik.Projection(m.srs)
tile_projection = GoogleProjection()

render_tiles(
    m=m,
    projection=projection,
    tile_projection=tile_projection,
    bbox=BOUNDING_BOX,
    tile_dir='/opt/output/counties/',
    minZoom=7,
    maxZoom=9
)
