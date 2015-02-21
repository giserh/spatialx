# -*- coding: utf-8 -*-
"""simplify.py

Algorithms to simplify spatial networks. Indeed, many networks contains many
degree 2 nodes which are topologically redondant, but are needed to respect the
geometry. Most of the time, these nodes are not necessary for the measures we
perform---we usually only needs the distance between degree != 2 nodes--- and
only make the computation slower. 

Simplifying the network allows for substantial performance improvement, even
when including the simplification/restitution process (linear in the number of
nodes).
"""
import networkx as nx


__authors__ = """\n""".join(["Rémi Louf <remilouf@sciti.es>"])


__all__ = ["simplify",
           "restitute"]


#
# Callable functions
#

def simplify(G):
    ''' Returns a simplified version of the graph comprising
            * The stations
            * The nodes with degree > 2
            * The nodes with degree 1
    Linked by edges whose length is equal to the sum of the lengths of the edges they replace.
    The simplified graph is topologically equivalent (same loops, edge weights) but lighter and makes
    computations easier.

    Input
    -----
        * G : NetworkX graph

    Returns
    -------
        * S : Networkx graph
            nodes = nodes of the original graph of degree 1 or > 2
            edges = "super edges" contains as a property 'in_edges' = [ordered list of the edges contained in this super-edge]
    '''

    S = G.copy()

    ## Iterate over the graph's nodes
    for n,data in F.nodes_iter(data=True):
        if (F.degree(n)==2 and data['insee'] == ''): # If k=2 and not a station, delete
            old_edges = F.edges(n,data=True)

            for e in old_edges: #remove edges from the graph
                F.remove_edge(e[0],e[1])

            nodes = [e[i] for i in range(2) for e in old_edges if e[i]!=n]	
            s_edge = (nodes[0],nodes[1],{'in_edges': []})

            ## Three cases: no edge is a super-edge, one is a super edge, both are.
            for e in old_edges:
                if 'in_edges' not in e[2]:
                    s_edge[2]['in_edges'].append(e)
                else:
                    s_edge[2]['in_edges'] += e[2]['in_edges']

            F.add_edge(s_edge[0],s_edge[1],in_edges = s_edge[2]['in_edges'])

    return S



def restitute(S):
    pass
