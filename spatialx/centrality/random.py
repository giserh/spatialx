# -*- coding: utf-8 -*-
"""random.py

Algorithms to compute the random walk centrality on spatial networks.
We directly use the implementation in NetworkX.
"""
import numpy as np
import networkx as nx


__all__ = ['randomwalk_centrality',
            'e_randomwalk_centrality']


#
# Helper functions
#


#
# Callable functions
#
def randomwalk_centrality(G, normalized=True):
    """ Compute the random walk centrality of nodes

    Parameters
    ----------

    G: Networkx graph
        Graph

    normalized: bool
        If True, we normalise the total betweenness value by the total number of
        pair of nodes in the graph `n(n-1)/2`

    Returns
    -------

    nodes: dictionary
        Dictionary of nodes with RW centrality as values
    """
    return nx.current_flow_betweenness_centrality(G, 
                                                  normalized, 
                                                  weight='length')


def e_randomwalk_centrality(G, normalized=True):
    """ Compute the random walk centrality of edges

    Parameters
    ----------

    G: Networkx graph
        Graph

    normalized: bool
        If True, we normalise the total betweenness value by the total number of
        pair of nodes in the graph `n(n-1)/2`

    Returns
    -------

    edges: dictionary
        Dictionary of edges with RW centrality as values
    """
    return nx.edge_current_flow_betweenness_centrality(G, 
                                                  normalized, 
                                                  weight='length')


