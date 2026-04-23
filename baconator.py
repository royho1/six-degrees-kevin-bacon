#!/usr/bin/env python3

import sys
import csv

# You are going to want to start with your homework4 graph.py file,
# but you will want to add/modify things to support the notion of
# multiple valid edges between two nodes.
import graph

# Needed for the "Gimme20" method
import json


class Baconator():

    def __init__(self, filename):
        """Filename is a .csv file, where the first column is the
        movie name and the subsequent columns are the actors.  There
        is NO header on the .csv file.
        """
        """initialize"""
        self.bacongraph = graph.Graph()
        """Given, but here just making/initializing a new graph since at the beginning we import graph
        which is just our graph code that was modified from earlier so that
        the notion of multiple valid edges between two nodes is supported - for actors and movies context."""
        # raise NotImplemented
        with open(filename, "r") as file:
            """Open the csv file and use 'r' so that we are only just reading it and using it
            with this format of with open(filename, "r") as file is easier because it opens but also closes the file."""
            """Note to self: from the past spell checker homework you could have just used with open(filename, "r") as file
            to simplify things instead of manually opening/reading it and then making more code to close it."""
            reader = csv.reader(file)
            """reader will let us iterate over each line in the moviedata.csv file to give us rows/lines from the csv"""
            for line in reader:
                """For loop, so for each line in the reader, for each line in the csv file the movie file."""
                movie = line[0]
                """The format of the moviedata.csv file, for each line is that the first index is the movie, and then that 
                is followed by all the actors from the movie. This is more clear when you open it in a google sheets actually 
                for visualization purposes. But pretty much for each line in the csv, the movie comes first (0 index), followed by
                all of the actors in the movie after that 0 index."""
                actors = line[1:]
                """Like mentioned before, the movie is the 0th index, followed by all the actors in the movie after that. So here
                we are just getting all the actors from each line/movie in the file."""
                for actor1 in actors:
                    """For loop, goes through all of the actors"""
                    if actor1 not in self.bacongraph:
                        """If actor1 is not in actors at all, not in the graph, then we will add it to 
                        the bacongraph:"""
                        self.bacongraph[actor1] = actor1
                        """Make the node / actor apart of the bacongraph, the actor's name."""
                    for actor2 in actors:
                        """Second actor iterating through all of the actors"""
                        if actor1 != actor2:
                            """As long as these two actors that we are looking into are not the same actor:"""
                            if actor2 not in self.bacongraph:
                                """If the second actor we just looked at is not part of the bacongraph
                                and is not a node:"""
                                self.bacongraph[actor2] = actor2
                                """Add the actor into the graph as a node with their name"""
                            self.bacongraph.connect(actor1, actor2, movie)
                            """Now that these two actors are added to the bacongraph,
                            connect them using the connect function from our graph.py, connect them
                            because they were in the same movie together."""
    """Actors are the nodes, movies act as the weight/edges"""

    def find_min_baconpath(self, actor):
        """Returns a minimum length baconpath between the named actor
        and "Kevin Bacon", or None if no such path exists or if the
        actor is not found.

        A baconpath is a python list of the form [actor, movie, actor,
        movie..] with the final actor being "Kevin Bacon", and for
        every movie the actor both before and after the movie title
        appeared in that movie.

        As an example, a minimum baconpath for the actor Zoe Saldana is:

        ['Zoe Saldana', 'Guardians of the Galaxy', 'Brendan Fehr', 'X-Men: First Class', 'Kevin Bacon']

        That is, Zoe Saldana appeared in Guardians of the Galaxy with
        Brendan Fehr, who appeared in X-Men: First Class with Kevin
        Bacon.

        The best way to discover a baconpath is a breadth first
        traversal, either starting from the targeted actor or Kevin
        Bacon and using the resulting path as the minimum baconpath.

        You are going to need to modify your graph.py file as well to
        support multiple edges, as two actors can be in multiple
        movies together, but the baconpath itself only includes one of
        the movies.

        """
        """Note, remember that for breadth first traversal, white = not visited yet, grey means we are visiting ATM """
        # return NotImplemented
        if actor not in self.bacongraph:
            """if the actor is not part of the graph, there will not be any type of path
            that we can find, no minimum bacon graph, so we will return None for that:"""
            return None
        """Return none if the actor is not in the bacon graph."""

        for actornode in self.bacongraph:
            """For each actor node in the bacon graph:"""
            actornode.color = "white"
            """set the color of the actor node to white, which in the context of breadth first traversals,
            means that we have not yet looked at that node yet / unvisited"""
            actornode.previous = None
            """There is no path before the starting node right now so set the actornode previous to None."""

        startnode = self.bacongraph[actor]
        """get the actor as the startnode for breadth first traversal"""
        """The actor that we want to use to start trying to find our bacon path, the base of this."""
        queue = [startnode]
        """Set queue to a list with only the startnode/actor in it to prepare for breadth first traversal"""
        startnode.color = "grey"
        """for breadth first traversal:"""
        while queue:
            """While the queue is not empty, meaning there are elements part of it so that
            we can actually do our breadth first traversal and look at the actors/nodes:"""
            current = queue.pop(0)
            """Set current to the first element in queue that is returned and removed as well"""
            for destnode, movie in current.all_edges():
                """iterate over all edges connected to the current node using all edges from the graph.py"""
                if destnode.color == "white":
                    """white means the node has not been visited yet"""
                    destnode.color = "grey"
                    """grey means that the node has been visited"""
                    destnode.previous = (current, movie)
                    """keep track of how we go to this dest node, which actor and which movie from before"""
                    queue.append(destnode)
                    """add the destination node to the queue"""
                    """Minor change right here, pretty much the old backwards function implemented here"""
                if destnode.name == "Kevin Bacon":
                    """if the last name and end node is kevin bacon"""
                    path = []
                    """The same as the backwards function, pretty much the idea is we start
                    at kevin bacon and go backwards"""
                    current = destnode
                    """set the current node to be the destination node, kevin bacon"""
                    while current.previous is not None:
                        """As long as there are previous nodes (actors and movies) before kevin bacon"""
                        previousactor = current.previous[0]
                        """the previous actor would be the first index of that tuple"""
                        movie = current.previous[1]
                        """The movie would be the second index of that tuple"""
                        path.append(current.name)
                        """We would then add the name of the actor to our path"""
                        path.append(movie)
                        """And also add the name of the movie to our path"""
                        current = previousactor
                        """Then set our current variable to previous actor and continue down the path of actors and movies"""
                    path.append(current.name)
                    """add the name to our list"""
                    return path[::-1]
                """reverse the path since we were going backwards."""
        return None
        """Return none if there is no path to kevin bacon found"""
        """we will go backwards using our backwards function if our last node is kevin bacon,
                    so that we can recreate the path from the starting actor to kevin bacon."""

    def backwards(self, bacon):
        """make a path from Kevin bacon node to the starting node 
        in regards to the breadth first traversal from before"""
        path = []
        """First make an empty list named path because we are finding the path"""
        kevinbacon = bacon
        """the kevinbacon node to be the current node, bacon."""

        while kevinbacon.previous is not None:
            """While we still have a previous node from our Kevin Bacon node since we are moving backwards from the kevinbacon node to 
            the starting node."""
            """If it is None, that means we are at the last and first node, we are at the start"""
            previousactor = kevinbacon.previous[0]
            """The previous actor would be the node before kevin bacon, and the 0th index of that tuple, which 
            should be actor followed by the movie."""
            movie = kevinbacon.previous[1]
            """Like mentioned before, we are setting movie to the movie of the actor that was right before kevin bacon
            . We use the 1st index for the tuple because it goes actor followed by movie."""
            path.append(kevinbacon.name)
            """While we are going backwards and finding the names of the actors before kevin bacon,
            we add each one to our empty list which we initialized at the start of the function."""
            path.append(movie)
            """And we do the same here with the movie, add that to the empty list which should be 
            after the name of the actor."""
            kevinbacon = previousactor
            """Set kevin bacon equal to previous actor so we can keep going back 
            in our steps to try and build the path that led up to kevin bacon in the first place"""

        path.append(kevinbacon.name)
        """Add the name to our empty list"""
        return path[::-1]
    """reverse the path since we went backwards."""

    def is_baconpath(self, path):
        """A check to see if something is a valid Baconpath, but not
        necessarily a minimal baconpath"""
       # return NotImplemented
        if not path:
            """To start it off, if the path is straight up empty, meaning its an empty list:"""
            return False
        """If the path is empty / empty list, then return false as this would mean that it is not a valid baconpath."""
        lastactor = path[-1]
        """Set lastactor to the lastactor in the path, which should be at index -1, the last element in the list."""
        if lastactor != "Kevin Bacon":
            """Check if that last actor is equal to kevin bacon, which the last actor should be since that is the
            whole point of the baconpath. If the last actor is not kevin bacon, return false"""
            return False
        """Return false if the last actor is not kevin bacon."""

        """Make sure that we are actually getting actor1 followed by a movie followed by actor2 who was also in that movie
         in that way they are connected"""
        for i in range(0, len(path) - 2, 2):
            """For loop, iterate starting from the first index of path and stopping at len(path) - 2 because we do not 
            want to go over the amount of indexes, and step by 2 because we are following the format which is actor, movie, actor"""
            actor1 = path[i]
            """This will give us the actor from the path list, which should be at index i, the current index."""
            movie1 = path[i + 1]
            """The movie that will be used between actor1 and actor 2 is accessed by index i+1, just one more
            than our current index which follows the format."""
            actor2 = path[i + 2]
            """And our second actor who was also in the movie is in index i + 2."""
            if actor1 not in self.bacongraph or actor2 not in self.bacongraph:
                """just condensed this for clarity reasons, here if the first or the second actor we are looking at
                are not in the bacongraph, we return false. """
                """if the first actor in the list is not in the bacongraph"""
                return False
            """Return false, this would be an invalid bacon path"""
            actor1node = self.bacongraph[actor1]
            """Set actor1node for the respective actor1"""
            actor2node = self.bacongraph[actor2]
            """Set the actor2node for the respective actor2"""
            if movie1 not in actor1node.edges.get(actor2node, set()) or movie1 not in actor2node.edges.get(actor1node, set()):
                """if the movie isnt an edge between these two actor nodes:"""
                return False
            """Return false - this would be invalid"""
        return True
    """return true if these statements pass, this means it is a baconpath"""

    def is_min_baconpath(self, path):
        """This should additionally check if a valid Baconpath is minimal"""
        # return NotImplemented
        if not self.is_baconpath(path):
            """First have to check if we are dealing with an actual bacon path , if not:"""
            return False
        """Return false if it is not a valid bacon path"""
        startactor = path[0]
        """Get the starting actor as the first index"""
        minimumpath = self.find_min_baconpath(startactor)
        """set the minimum path and find that min path from the starting actor
        to kevin bacon"""
        if minimumpath is None:
            """If there is no path to kevin bacon:"""
            return False
        """return false if there is no path - invalid"""
        return path == minimumpath
    """if the path we found is the same as the minimum path, set them equal"""

    def gimme_20(self):
        """This should return a string that is a JSON object for an
        entry in the tests list

        https://gradescope-autograders.readthedocs.io/en/latest/specs/

        that will be visible, and have a score of 20 and a max-score
        of 20, and be named 'gimme 20' """
        """Based on the gradescope requirements:"""
        """Make a dictionary testcase with the following key-value pairs as instructed by the gradescope link."""
        testcase = {
            "visibility": "visible",
            "score": 20,
            "max_score": 20,
            "name": "gimme 20"
        }
        return json.dumps(testcase)
    """Here we are just returning testcases but now as a JSON string as from the instructions."""
    """Use json.dumps to make testcase into the json string."""
    """For some reason if i add comments within the actual test case it does not pass the test so i got rid of them. """
    """Here is what i had before: pretty much just stating each part of the test, so visibility, score, max score, and the name of the test,
    then we use json.dumps to turn this into a json string."""


if __name__ == "__main__":
    baconator = None
    if len(sys.argv) > 1:
        baconator = Baconator(sys.argv[1])
    else:
        baconator = Baconator("moviedata.csv")

    # Some basic sanity tests, since Meg Ryan only appeared in one
    # movie with Kevin Bacon we know this is the only valid minimum
    # baconpath.
    path = baconator.find_min_baconpath("Meg Ryan")
    print(path)
    assert path == ['Meg Ryan', 'In the Cut', 'Kevin Bacon']

    assert baconator.is_baconpath(path)
    assert baconator.is_min_baconpath(path)

    assert not baconator.is_baconpath(['Meg Ryan'])
    assert baconator.is_baconpath(['Meg Ryan', "You've Got Mail",
                                   "Tom Hanks", "Apollo 13", 'Kevin Bacon'])
    assert not baconator.is_min_baconpath(['Meg Ryan', "You've Got Mail",
                                           "Tom Hanks", "Apollo 13",
                                           'Kevin Bacon'])

    path[1] = "bogus"
    assert not baconator.is_baconpath(path)

    """Tests!"""
    path = baconator.find_min_baconpath("Adam Scott")
    print(path)

    path = baconator.find_min_baconpath("Tom Hanks")
    print(path)

    """my favorite rapper, had to do it"""
    path = baconator.find_min_baconpath("Snoop Dogg")
    print(path)
    """Michael Scott"""
    path = baconator.find_min_baconpath("Steve Carell")
    print(path)

    path = baconator.find_min_baconpath("Kevin Bacon")
    print(path)

    path = baconator.find_min_baconpath("Nicholas Weaver")
    """Test for nick ego especially, I was not passing this earlier so lets check"""
    print(path)

    path = baconator.find_min_baconpath("Kevin Bacon")
    print(path)
