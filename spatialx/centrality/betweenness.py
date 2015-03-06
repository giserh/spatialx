# -*- coding: utf-8 -*-
"""betweenness.py

Algorithms to compute the (generalized) betweenness centrality.
We use networkx's algorithm as a base
"""
from heapq import heappush, heappop
from itertools import count
import random
import networkx as nx

import spatialx as sx


__all__ = ['betweenness_centrality', 
        'e_betweenness_centrality',
        'gbetweenness_centrality',
        'e_gbetweenness_centrality']


#
# Helper functions
#

## Betweenness

## Generalized Betweenness
def _single_source_shortest_path_basic(G, s):
    S = []
    P = {}
    for v in G:
        P[v] = []
    sigma = dict.fromkeys(G, 0.0)    # sigma[v]=0 for v in G
    D = {}
    sigma[s] = 1.0
    D[s] = 0
    Q = [s]
    while Q:   # use BFS to find shortest paths
        v = Q.pop(0)
        S.append(v)
        Dv = D[v]
        sigmav = sigma[v]
        for w in G[v]:
            if w not in D:
                Q.append(w)
                D[w] = Dv + 1
            if D[w] == Dv + 1:   # this is a shortest path, count paths
                sigma[w] += sigmav
                P[w].append(v)  # predecessors
    return S, P, sigma



def _single_source_dijkstra_path_basic(G, s, weight='length'):
    # modified from Eppstein
    S = []
    P = {}
    for v in G:
        P[v] = []
    sigma = dict.fromkeys(G, 0.0)    # sigma[v]=0 for v in G
    D = {}
    sigma[s] = 1.0
    push = heappush
    pop = heappop
    seen = {s: 0}
    c = count()
    Q = []   # use Q as heap with (distance,node id) tuples
    push(Q, (0, next(c), s, s))
    while Q:
        (dist, _, pred, v) = pop(Q)
        if v in D:
            continue  # already searched this node.
        sigma[v] += sigma[pred]  # count paths
        S.append(v)
        D[v] = dist
        for w, edgedata in G[v].items():
            vw_dist = dist + edgedata.get(weight, 1)
            if w not in D and (w not in seen or vw_dist < seen[w]):
                seen[w] = vw_dist
                push(Q, (vw_dist, next(c), v, w))
                sigma[w] = 0.0
                P[w] = [v]
            elif vw_dist == seen[w]:  # handle equal paths
                sigma[w] += sigma[v]
                P[w].append(v)
    return S, P, sigma


def _accumulate_generalized(betweenness, S, P, sigma, s, omega, G):
    delta = dict.fromkeys(S, 0)
    while S:
        w = S.pop()
        coeff = (omega(G,s,w) + delta[w]) / sigma[w]
        for v in P[w]:
            delta[v] += sigma[v] * coeff
        if w != s:
            betweenness[w] += delta[w]
    return betweenness


def _accumulate_edges_generalized(betweenness, S, P, sigma, s, omega, G):
    delta = dict.fromkeys(S, 0)
    while S:
        w = S.pop()
        coeff = (omega(G,s,w) + delta[w]) / sigma[w]
        for v in P[w]:
            c = sigma[v] * coeff
            if (v, w) not in betweenness:
                betweenness[(w, v)] += c
            else:
                betweenness[(v, w)] += c
            delta[v] += c
        if w != s:
            betweenness[w] += delta[w]
    return betweenness


def _rescale(betweenness, n, normalized, directed=False):
    if normalized is True:
        if n <= 2:
            scale = None  # no normalization b=0 for all nodes
        else:
            scale = 1.0 / ((n - 1) * (n - 2))
    else:  # rescale by 2 for undirected graphs
        if not directed:
            scale = 1.0 / 2.0
        else:
            scale = None
    if scale is not None:
        for v in betweenness:
            betweenness[v] *= scale
    return betweenness


def _rescale_e(betweenness, n, normalized, directed=False):
    if normalized is True:
        if n <= 1:
            scale = None  # no normalization b=0 for all nodes
        else:
            scale = 1.0 / (n * (n - 1))
    else:  # rescale by 2 for undirected graphs
        if not directed:
            scale = 1.0 / 2.0
        else:
            scale = None
    if scale is not None:
        for v in betweenness:
            betweenness[v] *= scale
    return betweenness

#
# Callable functions
#


############################
## Betweenness centrality ##
############################

def betweenness_centrality(G, normalized=True):
    """ Script to compute the betweenness centrality

    We use directly Networkx' algorithm.

    Returns
    -------

    nodes: dictionary
        Dictionary of nodes with betweenness centrality as value
    """
    return nx.betweenness_centrality(G, None, normalized, 'length')
    


def e_betweenness_centrality(G, normalized=True):
    """ Script to compute the edge betweenness centrality

    We directly use Networkx's algorithms.

    Returns
    -------

    edges: dictionnary
        Dictionary of edges with edge betweenness centrality as value
    """
    return nx.edge_betweenness_centrality(G, normalized, 'length')




########################################
## Generalized betweenness centrality ##
########################################

def gbetweenness_centrality(G, normalized=True):
    r""" Script to compute the generalized betweenness centrality

    Parameters
    ----------
    G : graph
      A NetworkX graph

    normalized : bool, optional
      If True the betweenness values are normalized by `2/((n-1)(n-2))`
      for graphs, and `1/((n-1)(n-2))` for directed graphs where `n`
      is the number of nodes in G.

    Returns
    -------

    nodes : dictionary
       Dictionary of nodes with betweenness centrality as the value.

    Notes
    -----

    The algorithm is from Ulrik Brandes.
    """
    weight = 'length' # Keep as variable, more flexible

    betweenness = dict.fromkeys(G, 0.0)  # b[v]=0 for v in G
    nodes = G
    for s in nodes:
        # single source shortest paths
        S, P, sigma = _single_source_dijkstra_path_basic(G, s, weight)
        # accumulation
        betweenness = _accumulate_generalized(betweenness, S, P, sigma, s, omega, G)

    # rescaling
    betweenness = _rescale(betweenness, len(G),
                           normalized=normalized,
                           directed=G.is_directed())
    return betweenness




def e_gbetweenness_centrality(G, omega, normalized=False):
    """ Script to compute the generalised edge betweenness centrality

    .. math::

       c_B(v) =\sum_{s,t \in V} \frac{\sigma(s, t|e)}{\sigma(s, t)} \omega_{st}

    where `\sigma(s,t)` is the number of shortest paths between `s` and `t`, `\omega_{st}` is the weight 
    of the shortest path between `s` and `t`.

    Parameters
    ----------

    G: Networkx graph
    
    omega : function
      Takes two nodes as an input and returns the weight associated with the
      pair of nodes `s` and `t`.
    
    normalized : bool, optional
      If True the betweenness values are normalized by `2/(n(n-1))`
      for graphs, and `1/(n(n-1))` for directed graphs where `n`
      is the number of nodes in G.

    Returns
    -------
    edges : dictionary
       Dictionary of edges with betweenness centrality as the value.


    Notes
    ------

    Original algorithm by Ulrik Brandes, adapted for our own use.
    """
    weight = 'length' # Keep as variable if design changes in future

    betweenness = dict.fromkeys(G, 0.0)  # b[v]=0 for v in G
    # b[e]=0 for e in G.edges()
    betweenness.update(dict.fromkeys(G.edges(), 0.0))
    for s in G:
        # single source shortest paths
        S, P, sigma = _single_source_dijkstra_path_basic(G, s, weight)
        # accumulation
        betweenness = _accumulate_edges_generalized(betweenness, S, P, sigma, s, omega, G)

    # rescaling
    for n in G:  # remove nodes to only return edges
        del betweenness[n]
    betweenness = _rescale_e(betweenness, len(G),
                             normalized=normalized,
                             directed=G.is_directed())
    return betweenness


