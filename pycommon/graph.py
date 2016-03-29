from itertools import groupby
from pycommon import get0, get1

def iter_bidirectional(edges):
    '''
    Iterate through each (source, target) tuple in edges, yielding it along with
    its reverse.

    Args:
        edges: an iterable of tuples of (source, target).

    Returns:
        An iterator over (source, target) and (target, source) edges.
    '''
    for source, target in edges:
        yield source, target
        yield target, source

def graph_map(edges):
    '''
    Group all (source, target) tuples in edges by source, and convert the list
    of targets to a set.

    Args:
        edges: an iterable of tuples of (source, target), where source and
            target are hashable values representing nodes.

    Returns:
        A dict mapping each node to a set of all the nodes it links to.
    '''
    source_edge_groups_iterable = groupby(sorted(edges, key=get0), get0)
    return dict((source, set(map(get1, edge_group))) for source, edge_group in source_edge_groups_iterable)

def get_component(graph, source_id):
    '''
    Find the set of all nodes connected to source_id within graph, including source_id.

    Args:
        graph: a dict mapping from nodes to sets of nodes, like the output of
            graph_map(...)
        source_id: the node to find all the neighbors of

    Returns:
        A set of nodes (generally, hashable values representing nodes)
    '''
    processed_ids = set()
    unprocessed_ids = set([source_id])
    while len(unprocessed_ids) > 0:
        unprocessed_id = unprocessed_ids.pop()
        processed_ids.add(unprocessed_id)
        # doesn't work due to redefinition in more limited scope:
        # unprocessed_ids |= graph[unprocessed_id] - processed_ids
        unprocessed_ids.update(graph[unprocessed_id] - processed_ids)
    return processed_ids

def get_all_components(graph):
    '''
    Run get_component(...) on the given graph until all nodes have been assigned
    to a component. Uses graph.keys() to create a queue of nodes, then calls
    get_component(...) on each node in that queue until the queue is exhausted.

    Args:
        graph: a dict mapping from nodes to sets of nodes, like the output of
            graph_map(...)

    Returns:
        An iterator over sets of nodes. The sets comprise a partition of the
        input graph.
    '''
    queue_ids = set(graph.keys())
    while len(queue_ids) > 0:
        # grab a random starting point id from the queue
        next_id = queue_ids.pop()
        component = get_component(graph, next_id)
        queue_ids -= component
        yield component
