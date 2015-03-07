from nose.tools import *
import networkx as nx
import spatialx as sx

class TestBetweennessCentrality(object):

    def test_K5(self):
        """Betweenness centrality: K5"""
        G=nx.complete_graph(5)
        b=sx.betweenness_centrality(G,
                                    weight=None,
                                    normalized=False)
        b_answer={0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0}
        for n in sorted(G):
            assert_almost_equal(b[n],b_answer[n])


class TestWeightedBetweennessCentrality(object):

    def test_G(self):
        """Weighted betweenness centrality: G"""                   
        G = nx.Graph()
        G.add_weighted_edges_from([(0,2,2), (0,3,6), (0,4,4),
                                (1,3,5), (1,5,5), (2,4,1),
                                (3,4,2), (3,5,1), (4,5,4),
                                (0,1,3)])
        b_answer={0: 2.0, 1: 0.0, 2: 4.0, 3: 3.0, 4: 4.0, 5: 0.0}
        b=sx.betweenness_centrality(G,
                                    weight='weight',
                                    normalized=False)
        for n in sorted(G):
            assert_almost_equal(b[n],b_answer[n])
