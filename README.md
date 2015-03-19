# SpatialX

Library (based on NetworkX) to analyse spatial networks. Please contribute!

## Beware!

This code does not have any test suite (yet!). Please consider the results of
the algorithms with extreme care, or better, help us by writing tests!

## Dependencies

* NetworkX
* Fiona (for shapefile imports)
* Numpy

## Use

import spatialx as sx 

## Ackowledgements

If you find this library useful in your own work, please cite the following paper:

    @article{Louf2014,
    title={A typology of street patterns},
    author={Louf, R{\'e}mi and Barthelemy, Marc},
    journal={Journal of The Royal Society Interface},
    volume={11},
    number={101},
    pages={20140924},
    year={2014},
    publisher={The Royal Society}
    }


## Features

### I/O

+ Import Line shapefiles into a spatial network [tested]
+ Export spatial network to Shapefile [tested]
    It is easier to visualise large networks in GIS softwares.

### Statistics of paths

#### Paths


#### Centralities

+ Betweenness centrality
    + Usual betweenness centrality (nodes and edges)
    + Generalized betweenness centrality (nodes and edges)

+ Random walk centrality (nodes and edges)

+ Greedy Navigator Centrality (nodes and edges)

### Faces and dual network

+ Extraction of faces

+ Extraction of dual networkx

### Information representation

+ Extraction of lines  
    * Intersection Continuation Negotiation algorithm

### Other features

+ Simplification of spatial networks to speed up calculations


## Authors and License

License: GPL v2  
Author: Rémi Louf <remilouf@sciti.es>  
Website: [Scities](http://www.sciti.es)
