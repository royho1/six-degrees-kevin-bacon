#!/usr/bin/env python3

from collections import deque


class GraphNode():
    def __init__(self, name, data=None):
        """Initialization for the node itself.

        This is for a more efficient implementation: Instead of having
        a set of edges, this one should use a dictionary with a key
        for each destination node and the value being the weight for
        the edge.

        This will allow connected() and disconnect() to operate in
        linear time.

        Functions you need to implement in the new version will raise
        NotImplemented exceptions until you update the code.

        """

        self.data = data
        self.name = name
        # This is the new represntation of a dictionary mapping
        # nodes to edge weights
        self.edges = {}

        # We also maintain a set of backward edges from dest->source
        # so we can go backwards even though it is a directed graph.
        self.back_edges = {}

        # Parameters generated during traversals.  We initialize them
        # here for error checking purposes
        self.color = "none-set"
        self.previous = None
        self.distance = float('inf')

    def connect(self, dest_node, movie):
        """Connects this node to another node.

        Important notes: It assumes a directed graph, and you need to
        connect the other way if you want an undirected graph.  It
        also does NOT allow multiple connections to the same
        destination, and enforces this with an assertion.
        """
        """Connect used to make an edge/connection between two nodes within the graph"""
        """Weight is set to 1 if not provided"""
        if dest_node not in self.edges:
            """make sure that the dest node is not in the dictionary of edges already"""
            self.edges[dest_node] = set()
            """add it to an empty set if not in the dictionary already"""
            dest_node.back_edges[self] = set()
            """add the back edges too"""
        self.edges[dest_node].add(movie)
        """add the movie as an edge between our nodes/actors now"""
        dest_node.back_edges[self].add(movie)
        """make sure the structure is kept by doing the same with the back edges."""

    def connected(self, dest_node):
        """A connectivity check.

        You will need to update this for the new version."""
        return dest_node in self.edges

    def disconnect(self, dest_node, movie=None):
        if not self.connected(dest_node):
            """This is a check to see if the current node we are looking at is already not connected to the destination node:"""
            raise Exception("No edge exists between {} and {}".format(
                self.name, dest_node.name))
        """Raises an Exception if there is no edge/connection from the current node to the destination node - Boolean"""
        # RaiseNotImplementedError
        if self.connected(dest_node):
            """If the current node is connected/does have an edge connected to the destination node:"""
            del self.edges[dest_node]
            """If there is a connection/edge, we delete the connection from the node to the destination node"""
            del dest_node.back_edges[self]
            """And we do the same here with the back edge, delete that as well if there is a connection established and we know that."""

    def __bool__(self):
        """Needed to keep python from getting too smart because we
        may also have __len__ defined"""
        return True

    def _check_structure(self):
        """A sanity check function that makes sure that every edge is well
        formed.

        """
        """Tests to make sure proper edge/connection is formed between nodes"""
        # Raise NotImplementedError
        for dest_node, weight in self.edges.items():
            """For loop, will iterate over self.edges (all of the edges) the the current node were are looking at
            as."""
            """This loop goes through all of the edges that the current node has, and then gets the destination node from that edge
            as well as the weight which is specified."""
            if self not in dest_node.back_edges:
                """If the current node self is not in the destination node's back edges, so if it is not in the back edges,
                this means that the back edge is missing, so we have to raise an exception / error"""
                raise Exception("Edge from {} to {} is not well formed".format(
                    self.name, dest_node.name))
            """Raise exception error if the current node is not in the destination node's back edges, meaning that the edge is not 
            well formed, and it will specify which node that edge is not well formed between."""
            if dest_node.back_edges[self] != weight:
                """If the weight of the destination node's back edge does not equal the weight of the forward edge:"""
                raise Exception("Edge from {} to {} is not well formed".format(
                    self.name, dest_node.name))
            """We have to raise exception error again like before, specifying which node that the edge is not well formed
            between."""
        for source, weight in self.back_edges.items():
            """Similar to our first for loop, but this time iterating over all of the back edges,
            and then gets the source node as well as the weight that is specified."""
            if self not in source.edges:
                """if the current node we are looking at does not have an edge with the source node, there is a problem 
                so we have to raise an exception error"""
                raise Exception("Back edge from {} to {} is not well formed".format(
                    source.name, self.name))
            """Like mentioned before, we would have to raise an exception error because if the condition is true it means
            that an edge is not well formed, and then specify between which node's that edge is not formed between"""
            if source.edges[self] != weight:
                """if the weight of the edge is not equal to what we think it should be:"""
                raise Exception("Back edge from {} to {} is not well formed".format(
                    source.name, self.name))
            """Same thing here as before, raise an exception error and then specify between which nodes that problem
            occurs between."""

    def __repr__(self):
        """A sensible repr function"""
        return ("( {}/{} [".format(self.name, self.data) +
                ", ".join(
                    map(
                        lambda x: "{}->{}".format(x[1],
                                                  x[0].name),
                        self.all_edges()))
                + "])")

    def __str__(self):
        return "Name: {}".format(self.name)

    def all_edges(self):
        """This iterates over all nodes it is connected TO in
        unspecified order, returning a tuple of (destination-node,
        edge-weight)
        """
        # raise NotImplementedError
        for dest_node, movies in self.edges.items():
            """iterate over everything in items"""
            for movie in movies:
                """iterate over each movie connected through the actor"""
                yield (dest_node, movie)
                """then yield the tuple we have been following and using"""

    def del_all_edges(self):
        """This deletes all edges TO and FROM the graph...

        An important note on dictionaries: You can NOT delete from a
        dictionary from within a loop over the dictionary.
        """
        # Raise NotImplementedError
        dest_nodes = list(self.edges.keys())
        """This creates a list of all of the destination nodes to which the current node 
        we are looking at has connection/edges to."""
        for node in dest_nodes:
            """For node in destination nodes. For loop that goes over each node within destination nodes
            meaning that they have an edge with the current node we are looking at."""
            self.disconnect(node)
            """This is the actual act of disconnecting and getting rid of any edges and connections so that
            proper deletion of all edges is made."""


class Graph():
    """This is effectively the graph code from the lecture.  Thanks to
    the abstractions for nodes, the code works with your new version
    as well
    """

    def __init__(self, dictionary=None):
        """Initializes a graph"""

        self.nodes = {}
        if dictionary:
            for key in dictionary:
                self[key] = dictionary[value]

    def __getitem__(self, name):
        """This returns the NODE itself, not the data in the node.

        We do this as returning the node because there are many things
        we want to do with nodes.
        """
        if name not in self.nodes:
            raise IndexError("Unable to find {}".format(name))
        return self.nodes[name]

    def __setitem__(self, name, data):
        if name in self.nodes:
            self.nodes[name].data = data
        else:
            self.nodes[name] = GraphNode(name, data)

    def __delitem__(self, name):
        """For deleting nodes, we delete all the edges involved in a
        node first..."""
        if name not in self.nodes:
            raise IndexError("Unable to find {}".format(name))
        self.nodes[name].del_all_edges()
        del self.nodes[name]

    def __contains__(self, name):
        return name in self.nodes

    def __iter__(self):
        for name in self.nodes:
            yield self.nodes[name]

    def connect(self, source_name, dest_name, weight=1):
        """This will implicitly raise errors if nodes don't exist..."""
        source = self[source_name]
        dest = self[dest_name]
        source.connect(dest, weight)

    def addedge(self, source_name, dest_name, weight=1):
        if source_name not in self.nodes:
            self[source_name] = None
        if dest_name not in self.nodes:
            self[dest_name] = None
        self.connect(source_name, dest_name, weight)

    def disconnect(self, source_name, dest_name):
        source = self[source_name]
        dest = self[dest_name]
        source.disconnect(dest)

    def connected(self, source_name, dest_name):
        source = self[source_name]
        dest = self[dest_name]
        return source.connected(dest)

    def check_structure(self):
        """Will raise an assertion failure if it is not well formed"""
        for node in self.nodes:
            self.nodes[node]._check_structure()
        return True

    def dijkstra_traversal(self, node_name):
        """This traversal is the shortest path traversal starting from
        the node.

        Note that it will return all nodes, even those who are not
        reachable from the starting node, but such nodes will have no
        "previous" value."""

        start = self.nodes[node_name]
        unvisited = set()
        for n in self.nodes:
            self.nodes[n].distance = float('inf')
            self.nodes[n].previous = None
            unvisited.add(self.nodes[n])
            for (dest, weight) in self.nodes[n].all_edges():
                assert weight >= 0
        start.distance = 0
        while len(unvisited) > 0:
            min_node = None
            for node in unvisited:
                if min_node == None:
                    min_node = node
                if node.distance < min_node.distance:
                    min_node = node

            unvisited.remove(min_node)
            for (dest, weight) in min_node.all_edges():
                if (dest in unvisited and
                        min_node.distance + weight < dest.distance):
                    dest.distance = min_node.distance + weight
                    dest.previous = min_node
            yield min_node

    def bfs_traversal(self, node_name):
        """Does an iterative breadth first search traversal"""
        for n in self.nodes:
            self.nodes[n].color = "white"
            self.nodes[n].previous = None
        start_node = self[node_name]
        queue = deque()
        start_node.color = "gray"
        queue.appendleft(start_node)
        while len(queue) != 0:
            node = queue.pop()
            for (dest, weight) in node.all_edges():
                if dest.color == "white":
                    dest.color = "gray"
                    dest.previous = node
                    queue.appendleft(dest)
            node.color = "black"
            yield node

    def dfs_iterative_traversal(self, node_name):
        """Does an iterative depth first search traversal"""
        for n in self.nodes:
            self.nodes[n].color = "white"
            self.nodes[n].previous = None
        start_node = self[node_name]
        queue = []
        queue.append(start_node)
        start_node.color = "gray"
        while len(queue) != 0:
            node = queue[len(queue)-1]
            appended = False
            for (dest, weight) in node.all_edges():
                if dest.color == "white":
                    dest.color = "gray"
                    dest.previous = node
                    queue.append(dest)
                    appended = True
            if not appended:
                node = queue.pop()
                node.color = "black"
                yield node

    def dfs_traversal(self, node_name):
        """Does a depth first search traversal recursively.  Note that
        this can sometimes blow out the python stack, so the iterative
        one is perferred in practice"""
        def dfs_internal(at):
            at.color = "gray"
            for (dest, edge) in at.all_edges():
                if dest.color == "white":
                    dest.previous = at
                    yield from dfs_internal(dest)
            at.color = "black"
            yield at
        for n in self.nodes:
            self.nodes[n].color = "white"
            self.nodes[n].previous = None
        yield from dfs_internal(self.nodes[node_name])

    def __len__(self):
        return len(self.nodes)

    def __repr__(self):

        return "{ " + ", ".join(map(lambda x: repr(self.nodes[x]),
                                    self.nodes)) + "}"


def make_star():
    """A basic test graph of a star"""
    g = Graph()
    nums = "01234"
    for i in range(5):
        g[i] = "Node{}".format(i)
    for i in range(5):
        g.connect(i, (i+2) % 5)
        g.connect(i, (i-2) % 5)
    return g


def samplegraph():
    """The basic test graph used in class"""
    g = Graph()
    connections = [(0, 1, 1), (0, 5, 5),
                   (1, 2, 20), (1, 3, 3), (1, 4, 4),
                   (2, 0, 2), (3, 4, 4),
                   (4, 2, 4)]
    for i in range(6):
        g[i] = "Node{}".format(i)
    for source, dest, weight in connections:
        g.connect(source, dest, weight)
    return g
