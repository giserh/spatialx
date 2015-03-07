""" Read/write graphs in shapefile format """
import math
import pyproj
import fiona
import networkx as nx

__all__ = ['read_shp']

#
# Helper functions
#
def _project(lat, lon, projection):
    """ Project coordinates to LAEA """
    proj = pyproj.Proj(proj=projection)
    mx, my = proj(lat, lon)
    return mx, my


def _length(G, e):
    """ Compute length of an edge """
    x0, y0 = (G.node[e[0]]['x'],
            G.node[e[0]]['y'])
    x1, y1 = (G.node[e[1]]['x'],
            G.node[e[1]]['y'])

    return math.sqrt( (x0-x1)**2 + (y0-y1)**2 )


def _shp_to_spatial(layer, projection=None):
    """ Convert graphs from shapefiles to SpatialX format """
    G = nx.Graph()

    ## Break down lines in elementary segments 
    for f in layer:
        if f['geometry']['type'] == 'LineString':
            coords = f['geometry']['coordinates'] 
            for s, t in zip(coords[:-1], coords[1:]):
                G.add_edge(s,t)

        # Break down MultilineString
        elif f['geometry']['type'] == 'MultiLineString':
            for coords in f['geometry']['coordinates']:
                for s, t in zip(coords[:-1], coords[1:]):
                    G.add_edge(s,t)

        else:
            print l['type']

    ## Project the nodes and compute edges
    for v in G:
        if projection is not None:
            x, y = _project(v[0], v[1], projection)
        else:
            x, y = v
        G.node[v]['x'] = x 
        G.node[v]['y'] = y 

    for e in G.edges_iter():
        s,t = e
        G[s][t]['length'] = _length(G, e)

    return G



#
# Callable functions
#

def read_shp(path, projection=None):
    """ Read shapefile into a SpatialX graph

    Parameters
    ----------

    path: string
        Path to the shapfile to import

    projection: string (optional)
        Map projection to use for the graph. If none is indicated, the positions
        are kept as they are in the shapefile (leave None if shapefile is
        already projected, for instance). Refer to the pyproj documentation for
        a list of possible projections.

    Returns
    -------

    G: SpatialX graph
        Spatial network, nodes have positions and edges have a length.
    """
    # Insert tests on existence of file, and right type
    with fiona.open(path, "r", "ESRI Shapefile") as source:
        G = _shp_to_spatial(source, projection)

    return G
