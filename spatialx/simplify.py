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




