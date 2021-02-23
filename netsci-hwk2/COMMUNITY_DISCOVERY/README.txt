MODULARITY:
------------------------------------------------------------------------
The file is modularity.py. To calculate modularity of a network, run as:

python3 modularity.py graphfile.gml attribute

“attribute” is the name of the node attribute used to represent the graph partitioning.

Example:

python3 modularity.py lotr.gml ModularityClass


COMMUNITY DISCOVERY:
------------------------------------------------------------------------

The file is community_discovery.py. Should be used as:

python3 community_discovery.py graphfile.gml

Stores node's community as node attribute "CommunitiesGreedy"
Stores solution in graphfile_sol.gml
Stores plot showing modularity values in graphfile_plot.png



Both programs assume edge weights to be "value" attribute of edges.

