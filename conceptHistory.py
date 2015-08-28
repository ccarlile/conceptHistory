import networkx as nx

class ConceptHistory:
    #history keeps a cpoy of the graph as reference for what's been presented so far
    def __init__(self, callback):
        self._historyGraph = nx.DiGraph()
        self._historyRecord = []
        self._callback = callback

    def _addToHistory(self, user, action, node, **kwargs):
        #node is a string that can be either 'node' or 'edge'. I would have
        #called it 'type' but thats taken in python sooooo

        histObject = {}
        histObject['user'] = user
        histObject['action'] = action
        histObject['node'] = node
        attr=kwargs
        histObject['attr'] = attr

        if 'label' not in attr.keys(): raise TypeError('must have label')
        if node == 'edge':
            if 'source' not in attr.keys() or 'target' not in attr.keys():
                raise TypeError('Edge must have source and target')
            self._checkIfLegal(histObject)

        if node != 'node' and node != 'edge':
            raise TypeError('Node must be "node" or "edge"')

        self._historyRecord.append(histObject)

    def addNode(self, user, node):
        #Add node to historyGraph and historyRecord
        self._historyGraph.add_node(node)
        self._addToHistory(user, 'add', 'node',label=node)
        pass

    def addEdge(self, user, esource, etarget, elabel):
        #Add edge to historyGraph and historyRecord
        self._addToHistory(user, 'add', 'edge',label=elabel, source=esource,
                                target=etarget)
        self._historyGraph.add_edge(esource, etarget)

    def removeNode(self, user, node):
        #Remove node from historyGraph and log it in historyRecord
        self._historyGraph.remove_node(node)
        self._addToHistory(user, 'remove', 'node',label=node)

    def removeEdge(self, user, esource, etarget, elabel):
        #Remove edge from historyGraph and log it in historyRecord
        self._historyGraph.remove_edge(esource, etarget)
        self._addToHistory(user, 'remove', 'node',label=elabel, source=esource,
                                target=etarget)

    def _checkIfLegal(self, item):
        #Check if action is legal (i.e. does node we're trying to connect to
        #exist? I can't think of any other offending cases)
        edge = item['attr']
        graph = self._historyGraph.succ

        #either source or target not found
        if edge['source'] not in graph.keys() and edge['target'] not in graph.keys():
            #now we check if there exists a history object matching a deleted node
            for item in reversed(self._historyRecord):
                if (item['action'] == 'remove' and
                    item['node'] == 'node' and
                    (item['attr']['label'] == edge['source'] or
                        item['attr']['label'] == edge['target'])):

                    self.addNode('auto',item['attr']['label'])
                    #since we just added the offending node back, we can now
                    #see its generated history item by looking at the tail of
                    #historyRecord
                    self._callback(self._historyRecord[-1])
                    break

if __name__=='__main__':
    def callback(x): print x
    h = ConceptHistory(callback)
    h.addEdge('user','A', 'B', 'holla')
    h.addEdge('user','B', 'C', 'doot')
    h.removeNode('user','B')
    h.addEdge('user','B','D', 'doot')
