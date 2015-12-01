Concept History Tool
====================

Designed to be used alongside ConceptDraw. Keeps a log of additions and deletions to
a concept map and send messages back to the drawing application when it corrects an error
(namely, when the agent tries to draw an edge to a node that the user has deleted, however
it should be fairly straightforawrd to add more exceptions.

This module communicates with the drawing application using a callback function which the
user must define

Requirements
------------

Requires networkx. Designed to work with conceptDraw.py.

Usage
-----

```
from conceptHistory import ConceptHistory
def callback(x) : print x
h = ConceptHistory(callback)
h.addEdge('user','A', 'B', 'holla')
h.addEdge('user','B', 'C', 'doot')
h.removeNode('user','B')
h.addEdge('user','B','D', 'doot')
```

The callback will be triggered at the last, offending action.

Acknowledgments
---------------

This work was supported by the National Science Foundation under Award No. 1352207. Any Opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect those of the National Science Foundation."

