from collections import defaultdict
import sys
from itertools import combinations

def try_adj_tiles(sample, belongs_to_node_or_edge, rows, columns, i, j):
    if (i,j) in belongs_to_node_or_edge:
        belongs_to_node_or_edge.remove((i,j))
        merge_adj_tiles(sample,belongs_to_node_or_edge,rows,columns,i,j)
    

def merge_adj_tiles(sample, belongs_to_node_or_edge, rows, columns, i, j):
    if (i,j) in sample:
        return
    sample.add((i,j))
    if (i > 0) and (i-1,j) not in sample:
        try_adj_tiles(sample, belongs_to_node_or_edge, rows, columns, i-1, j)
    if (j > 0) and (i,j-1) not in sample:
        try_adj_tiles(sample, belongs_to_node_or_edge, rows, columns, i, j-1)
    if i < rows-1 and (i+1,j) not in sample:
        try_adj_tiles(sample, belongs_to_node_or_edge, rows, columns, i+1, j)
    if j < columns-1 and (i,j+1) not in sample:
        try_adj_tiles(sample, belongs_to_node_or_edge, rows, columns, i, j+1)
    
def traverse_adj_tiles(adj_edge_tiles,visited,coordinates,rows,columns,tiles_in_node,edges_dic):
    if coordinates in visited:
        return
    
    visited.append(coordinates)
    
    if coordinates in edges_dic:
        adj_edge_tiles.add(coordinates)
        return
    
    if coordinates in tiles_in_node:
        traverse_adj_tiles(adj_edge_tiles,visited,(coordinates[0]-1,coordinates[1]),rows,columns,tiles_in_node,edges_dic)
        traverse_adj_tiles(adj_edge_tiles,visited,(coordinates[0]+1,coordinates[1]),rows,columns,tiles_in_node,edges_dic)
        traverse_adj_tiles(adj_edge_tiles,visited,(coordinates[0],coordinates[1]-1),rows,columns,tiles_in_node,edges_dic)
        traverse_adj_tiles(adj_edge_tiles,visited,(coordinates[0],coordinates[1]+1),rows,columns,tiles_in_node,edges_dic)
        return
        
    
def get_list_of_adj_edges(coordinates,rows,columns,tiles_in_node,edges_dic):
    adj_edge_tiles = set()
    visited = []
    traverse_adj_tiles(adj_edge_tiles,visited,coordinates,rows,columns,tiles_in_node,edges_dic)
    result = set()
    for tile in adj_edge_tiles:
        result.add(edges_dic[tile])
    return result

def create_graph(rows,columns,map_description):
    ''' separate tiles into nodes and edges '''
    belongs_to_node = set()
    belongs_to_edge = set()
    for i in range(rows):
        for j in range(columns):
            if map_description[i][j] == '~':
                belongs_to_node.add((i, j))
            else:
                belongs_to_edge.add((i, j))
                
    ''' group tiles into sets of tiles that represent one node, etc. '''
    num_nodes = 0
    nodes = []
    nodes_dic = {}
    while len(belongs_to_node):
        sample = set()
        i,j = belongs_to_node.pop()
        num_nodes += 1
        merge_adj_tiles(sample, belongs_to_node, rows, columns, i, j)
        for item in sample:
            nodes_dic[item] = len(nodes)
        nodes.append(sample)
    #print(num_nodes)
    #print(nodes_dic)
    #print(nodes)
        
    num_edges = 0
    edges = []
    edges_dic = {}
    while len(belongs_to_edge):
        sample = set()
        i,j = belongs_to_edge.pop()
        num_edges += 1
        merge_adj_tiles(sample, belongs_to_edge, rows, columns, i, j)
        for item in sample:
            edges_dic[item] = len(edges)
        edges.append(sample)
    
    '''
    print(num_edges)
    print(edges_dic)
    print(edges)
    '''
    
    
    ''' now figure out which nodes are connected to which edges  '''
    list_of_adj_edges_per_nodes = {}
    for i in range(len(nodes)):
        list_of_edges = get_list_of_adj_edges(next(iter(nodes[i])),rows,columns,nodes[i],edges_dic)
        list_of_adj_edges_per_nodes[i] = list_of_edges

    list_of_adj_nodes_per_edges = defaultdict(set)
    for key, value in list_of_adj_edges_per_nodes.items():
        for edge in value:
            list_of_adj_nodes_per_edges[edge].add(key)
    
    graph = defaultdict(set)
    for set_of_connected_nodes in list_of_adj_nodes_per_edges.values():
        for set_of_2 in combinations(set_of_connected_nodes,2):
            graph[set_of_2[0]].add(set_of_2[1])
            graph[set_of_2[1]].add(set_of_2[0])
    return graph, nodes_dic
    
def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))
if __name__ == "__main__":
    #sys.setrecursionlimit(10000000)
    rows, columns, numPath = input().split()
    rows = int(rows)
    columns = int(columns)
    numPath = int(numPath)
    map_description = []
    for i in range(rows):
        map_description.append(input())

    '''Create graph here'''
    graph, nodes_dic = create_graph(rows,columns,map_description)

    for i in range(numPath):
        query = input().split()
        coord_0 = (int(query[0])-1,int(query[1])-1)
        coord_1 = (int(query[2])-1,int(query[3])-1)
        try:
            print(len(next(bfs_paths(graph, nodes_dic[coord_0], nodes_dic[coord_1])))-1)
        except:
            print(0)
