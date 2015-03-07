# -*- coding: utf-8 -*-
"""faces.py

Algorithms to extract the faces (loops) in a planar network.
"""
from __future__ import division
import numpy as np
import networkx as nx

from spatialx.simplify import simplify


__authors__ = """\n""".join(["Rémi Louf <remilouf@sciti.es"])

__all__ = ["prune", 
           "extract_faces", 
           "to_dual"]




#
# Helper functions
#
def find_most_clockwise(previous,current, choices):
    """Returns the most clockwise edge coming from previous to current

    Input
    -----
        * previous : vertex (with position) from which we come
        * current: vertex (with position) at which we are
        * choices : list of possible next vertices (with position) 
    
    Returns
    -------
        * edge : most clockwise edge
    """
    v = np.array([current[1][0] - previous[1][0],
                  current[1][1] - previous[1][1],
                  0])
    v = v / np.linalg.norm(v)

    m = []
    l = []
    for p in choice:
        vp = np.array([p[1][0] - current[1][0],
                       p[1][1] - current[1][1],
                       0])
        vp = vp / np.linalg.norm(vp)

        m.append( np.cross(vp,v)[2] )
        l.append( np.dot(vp,v) )

    if len(choice) == 1:
        return (current[0], choice[0][0])
    else:
        negatives = [i for i,val in enumerate(m) if val<0]

        if len(negatives) > 0:
            return (current[0], choice[l.index(min([val for i,val in enumerate(l) if m[i]<0]))][0])
        else:
            return (current[0], choice[l.index(max(l))][0])



def center_of_gravity(G,nodes):
    """Returns the center of gravity of a list of nodes

    Input
    -----
        * G: Networkx graph containing nodes with their position
        * nodes: List of nodes id

    Returns
    -------
        * x,y: position of the center of gravity of all the nodes (with equal weight on each node)
    """
    x = sum([G.node[n]['x'] for n in nodes])/len(nodes)
    y = sum([G.node[n]['y'] for n in nodes])/len(nodes)
    return x,y






#
# Callable functions
#


def prune(G):
    """ Burns the branches from the graph

    Input
    ----
        * G : NetworkX graph

    Returns
    -------
        * S : Networkx graph which only contains the loops in G (no node of degree 1)
    """
    F = G.copy()

    ## Identify degree 1 nodes, burn the graph from there
    for n in F.nodes_iter():

        if F.degree(n) == 1:
            n0 = n
            for e in list(nx.dfs_edges(F,n)): ## Using the list because iterator does not like graph changing?
                F.remove_edge(e[0],e[1])

                # Find the next node
                if e[0] != n0:
                    n1 = e[0]
                else:
                    n1 = e[1]
                
                # if next node is of degree > 1 after edge removal, stop
                if F.degree(n1) > 1:
                    break
                n0 = n1


    ## Remove the degree 0 nodes
    deg = F.degree()
    to_remove = [n for n in deg if deg[n]==0]
    F.remove_nodes_from(to_remove)

    return F





def extract_faces(G):
    """Extracts the faces of a planar, pruned graph

    Input
    -----
        * G: Networkx graph, pruned

    Returns
    -------
        * faces = [[edges in f] for f in faces]
    """
    # First we need a dictionary recording visited edges
    visited = {e:0 for e in G.edges_iter()}

    faces = []
    for e in G.edges_iter():
        if visited[e]==0: # If the edge has not been visited, start exploration from there
            temp_loops = [e]
            n_prev = e[0]
            n_curr = e[1]

            looped = False
            while not looped:
                ## explore following clockwise until next edge already in current_loops
                neighbours = [( n, (G.node[n]['x'], G.node[n]['y']) ) 
                              for n in G.neighbors(n_curr) 
                              if n!=n_prev]
            
                next_e = find_most_clockwise((n_prev, (G.node[n_prev]['x'],G.node[n_prev]['y'])),
                                             (n_curr,(G.node[n_curr]['x'],G.node[n_curr]['y'])),
                                             neighbours)

                if next_e in temp_loops: # If the next move is an edge already visited, we have a loop
                    loops.append(temp_loops)
                    looped = True
                else: # Else we continue to move
                    visited[next_e] = 1
                    temp_loops.append(next_e)

                n_prev = n_curr
                if next_e[0] != n_curr:
                    n_curr = next_e[0]
                else:
                    n_curr = next_e[1]

    return faces




def to_dual(G):
    """ Extracts the dual of a planar graph

    Input
    -----
        * G: Networkx graph

    Returns
    -------
        * faces: List of Networkx graphs - G's faces
        * dual: Networkx Graph - dual graph of G, nodes are G's faces, edges indicate neighbouring relation

    """
   
    #
    # Graph preparation and extraction
    #

    # Simplify the graph
    simplified = simplify(G)
    # Prune the graph
    pruned = prune(G)
    # Extract faces
    faces = extract_faces(pruned)
    faces = sorted(faces,key=lambda x:len(x),reverse=1)[1:] # The longest face separates outside/inside
    

    #
    # Build faces and add as nodes to dual network
    #
    dual = nx.Graph()

    ## Build faces and add as nodes to dual graph
    faces_graphs = []
    for i,face in enumerate(faces):
        face_g = nx.Graph()		

        ## Rebuild (de-simplify) the faces
        edges_face = []
        for se in face:
            if 'in_edge' in pruned[se[0]][se[1]]:
                edges_face += [(e[0],e[1]) for e in e in pruned[se[0]][se[1]]['in_edges']]
            else:
                edges_face.append(se)
        nodes_face = list(set([e[0] for e in edges_face]+[e[1] for e in edges_face]))

        ## Build graph
        for n in nodes_face:
            face_g.add_nodes_from([(n,G.node[n])])
        for n1,n2 in edges_face:
            face_g.add_edge(n1,n2)	
        faces_graphs.append(face_g)

        ## Add face to graph
        x,y = center_of_gravity(G,nodes_face) 
        dual.add_node(i, x=x, y=y)


    #
    # Build dual network adjacency matrix 
    #
    for i,face1 in enumerate(faces):
        for j,face2 in enumerate(faces):
            if i!=j:
                ## Compare edge by edge
                for e1 in face1:
                    for e2 in face2:
                        if e1 == e2 or e1[::-1] ==e2:
                            if not dual.has_edge(i,j):
                                dual.add_edge(i,j)
                                continue # link found, explore other pairs

    return faces_graphs,dual
