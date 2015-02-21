# -*- coding: utf-8 -*-
"""Algorithms necessary for percolation of the street network"""




def percolate(G):
    """Percolate the nodes based on their relative network distance

    1. Simplify the network to eliminate k=2 nodes
    2. Iterate over edges in length order
    3. Union/Find algorithm to build clusters

    The algorithm is inspired by the works of [Tao2010]_, [Jiang2011]_ and
    [Masucci2013]_. 

    .. [Tao2010] Tao J. & Jiang B. (2010) Measuring urban sprawl based on
        massive street nodes and the concept of natural cities, Arxiv preprint,
        Arxiv:1010.0541.
    .. [Jiang2011] Jiang B. & Tao J. (2011) Zipf's law for all the natural
        cities in the United States: a geospatial perspective, International
        Journal of Geographical Information Science, 25(8):1269-1281.
    .. [Masucci2013] Masucci A.P., Stanilov K., Arcaute E., Hatna E., & Batty M.
        (2013) Ergodic Properties of Urban Street Networks in the UK, International
        Conference on SITIS, pp. 634-640. 
    """

    #
    # Simplify the network, remove degree 2 nodes
    #
    sG = rz.simplify(G)


    #
    # Initialise the Union/Find structure
    #

