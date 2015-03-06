# -*- coding: utf-8 -*-
"""greedy_navigator.py

Algorithms to computhe the Greedy Navigator Centrality introduced in [1]_.

.. [1] S.H. Lee and P. Holme 
       Physical Review Letters 108:128701 (2012)
"""
from __future__ import division
from heapq import heappush, heappop
from itertools import count
import numpy as np
import networkx as nx
import itertools

__all__ = ['gsn_centrality']


#
# Helper functions
#
def _angle(G, t, v, w):
   v1 = np.array([G.node[t]['x']-G.node[v]['x'],
                  G.node[t]['y']-G.node[v]['y']])
   v2 = np.array([G.node[w]['x']-G.node[v]['x'],
                  G.node[w]['y']-G.node[v]['y']])
   cosang = np.dot(v1, v2)
   sinang = np.norm(np.cross(v1, v2))
   return np.arctan2(sinang, cosang) 



def _single_gsn_path(G, s, t, weight="length"):
    """ Perform GSN path between s and t

    It is not clear from the paper whether we should take backtracking steps
    into account in the distance and centrality, I am choosing to do so. (Asked
    Sang-Hoon for what they used)
    """
    visited = [] #Keep track of the sequence of nodes
    P = {}
    v = s
    while True:
        visited.append(v)

        if v==t:
            return visited, dist
            
        # Iterate over nodes in angle order
        found = False
        for w, edgedata in sorted(G[v].items(), key=lambda x: _angle(G, t, v, x[0])):
            if w in visited:
                continue
            else:
                found = True
                v = w
                P[w] = v

        # If all neighbours have been visited, go to predecessor
        if not found:
            v = P[v]



def _accumulate(betweenness, L):
    """ Accumulate passage counts for node betweenness """
    for v in L:
        betweenness[v] += 1
    return betweenness 



def _accumulate_edge(betweenness, L):
    """ Accumulate passage counts for edge betweenness """
    for v,w in zip(L[:-1], L[1:]):
        if (w,v) not in betweenness:
            betweenness[(v,w)] += 1
        else:
            betweenness[(w,v)] += 1

    return betweenness



def _rescale(betweenness, n, normalized=True, directed=False)
    """ Normalise by the size of the graph """
    if normalized is True:
        if n <= 2:
            scale = None
        else:
            scale = 1.0 / ((n-1) * (n-2))
    else:
        if not directed:
            scale = 1.0 / 2.0
        else:
            scale = None

    if scale is not None:
        for v in betweenness:
            betweenness[v] *= scale

    return betweenness


def _rescale_e(betweenness, n, normalized=True, directed=False):
    """ Normalise by the size of the graph """
    if normalized is True:
        if n <= 1:
            scale = None
        else:
            scale = 1 / (n * (n-1))
    else:
        if not directed:
            scale = 1.0 / 2.0
        else:
            scale = None

    if scale is not None:
        for v in betweenness:
            betweenness[v] * scale

    return betweenness



#
# Callable functions
#
def gsn_centrality(G, normalized=True):
    """ Compute the Greedy Spatial Navigator centrality

    The GSN centrality is defined in [1]_
    There is a way (not implemented yet) to improve the computation time on this
    one. Indeed, going to t and starting from s, all nodes on the GSN path from
    s to t will also follow this path when going to t. 

    Parameter
    ---------

    G: Networkx graph

    normalized: bool
        If set to True, the betweenness values are renormalisez by the total
        number of paths between edges possibles.

    Output
    ------

    edges: dictionary
        Dictionary of edges with GSN betweenness as values

    References
    ----------


    .. [1] S.H. Lee and P. Holme
           Physical Review Letter 108:128701 (2012).
    """
    betweenness = dict.fromkeys(G, 0.0)
    for s,t in itertools.permutations(G, 2):
         L, d = gsn_path(G,s,t)
         betweenness = _accumulate(betweenness, L)

    betweenness = _rescale(betweenness,
                           len(G),
                           normalized,
                           directed=G.is_directed())

    return betweenness



def e_gsn_centrality(G, normalized=True):
    """ Compute the Greedy Spatial Navigator centrality

    The GSN centrality is defined in [1]_
    There is a way (not implemented yet) to improve the computation time on this
    one. Indeed, going to t and starting from s, all nodes on the GSN path from
    s to t will also follow this path when going to t. 
    
    Parameter
    ---------

    G: Networkx graph

    normalized: bool
        If set to True, the betweenness values are renormalisez by the total
        number of paths between edges possibles.

    Output
    ------

    edges: dictionary
        Dictionary of edges with GSN betweenness as values

    References
    ----------

    .. [1] S.H. Lee and P. Holme
           Physical Review Letter 108:128701 (2012).
    """
    betweenness = dict.fromkeys(G, 0.0) # b[v] = 0.0
    betweenness.update(dict.fromkeys(G.edges(), 0.0) # b[e] = 0.0
    for s,t in itertools.permutations(G, 2):
         L, d = gsn_path(G,s,t)
         betweenness = _accumulate_edges(betweenness, L)
    
    ## rescaling
    for n in G:
        del betweenness[n]
    betweenness = _rescale_e(betweenness,
                             len(G),
                             normalized,
                             directed=G.is_directed())

    return betweenness
