# -*- coding: utf-8 -*-
"""faces.py

Algorithms to extract the faces (loops) in a planar network.
"""
import networkx as nx

__all__ = []


#
# Helper functions
#




#
# Callable functions
#
def extract_faces(G):
	""" Extracts the faces of a planar graph

	Parameter
	---------

	G: Networkx graph, pruned

	Returns
	-------

	faces = [[edges in f] for f in faces]
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


