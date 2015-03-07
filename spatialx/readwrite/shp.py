""" Read/write graphs in shapefile format """
import math
import networkx as nx

__all__ = ['read_shp']

#
# Helper functions
#

def _compute_length(G, e):
    (x0, y0) = (G.node[e[0]]['x'],
                G.node[e[0]]['y'])
    (x1, y1) = (G.node[e[1]]['x'],
                G.node[e[1]]['y'])

    return math.sqrt( (x0-x1)**2 + (y0-y1)**2 )



#
# Callable functions
#

def read_shp(path):
    G = nx.read_shp(path)

    ## Read position from node labels
    for v in G:
       G.node[v]['x'] = v[0]
       G.node[v]['y'] = v[1]

    ## Compute the length of all edges
    for e in G.edges():
        G.edge[e]['length'] = _compute_length(G, e)

    return G
