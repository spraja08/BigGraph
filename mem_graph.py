from collections import deque
from csv import DictReader
from functools import partial, wraps
from pickle import NONE
import time
from memory_profiler import profile
from mem_repo import mem_repo
from mock_graph_data import edges

class Graph:

    def timeit(func):
        @wraps(func)
        def timeit_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            total_time_str = f'{total_time:.4f}'
            print(f'Function {func.__name__}{args} {kwargs} Took {total_time_str} seconds')
            return result, total_time_str
        return timeit_wrapper

    def __init__(self, data_src=None, verbose=False):
        # First load data into mem db
        self.repo = mem_repo()
        self.load_graph_data(data_src)
    
    def get_leaf(self, radial_graph: dict, paths: list[str]):
        for path in paths:
            leaf = radial_graph[path]
            radial_graph = leaf
        return leaf

    @timeit
    def load_graph_data(self, path: str):
        if path is None:
            raise ValueError("Invalid path for graph data source")
        with open(path, 'r') as read_obj:
            csv_reader = DictReader(read_obj)
            header = next(csv_reader)
            if header is not None:
                size = 0
                for row in csv_reader:
                    size += 1
                    self.repo.index(row['entity_from_guid'], row['entity_to_guid'], row['relationship_type'])
                    self.repo.index(row['entity_to_guid'], row['entity_from_guid'], row['relationship_type'])
                    if size % 100000 == 0:
                        print(f"read {size} lines of data")    
                print(f"read {size} lines of data")
                self.repo_size = size
        print("loaded {} entries".format(self.repo.size()))

    def get_all_connections(self, node: str):
        return self.repo.get(node)

    def printpath(self, path: list[int]) -> None:
        size = len(path)
        for i in range(size):
            print(path[i], end=" ")
        print()

    @timeit
    def compute_radial_data(self, source: str, degrees: int):
        source = self.repo.getCompressed( source )
        queue = deque()
        visitedNodes = set()
        result = []
        visitedNodes.add(source)
        #What is in the queue is an array - source, destination, reltype, level
        queue.append([source, source, "source", 1])

        while queue:
            currentNode = queue.popleft()
            result.append(currentNode)
            if currentNode[3] == degrees:
                continue

            connections = self.get_all_connections(currentNode[1])
            if connections:
                for connection in connections:
                    split = connection.split(":")
                    child = split[0]
                    childRel = split[1]
                    if child not in visitedNodes :
                        visitedNodes.add(child)
                        queue.append( [currentNode[1], child, childRel, currentNode[3] + 1 ] )
        print( len(result) )
        return result

    @timeit
    def get_radial_data(self, source: str, degrees: int):
        return self.opensearch.get(f"radial{degrees}-{source}")

    @timeit
    def get_all_paths(self, source: str, destination: str, degrees: int) -> list[list[str]]:
        return self.opensearch.get(f"path{degrees}-{source}|{destination}")
    

def main() :
    print( "In the main method" )
    graph = Graph(data_src='/Users/rspamzn/Downloads/combined-files.csv')
    comp = graph.repo.getCompressed('C3FDE0D9-4128-450A-A3B1-4FC08C228B8D')
    print( comp )
    print( graph.repo.compressedToUUID.get(comp))
    #print( graph.repo.adj_matrix.get(comp) )
    #print( len( graph.repo.adj_matrix.get(comp) ) )

    result = graph.compute_radial_data('C3FDE0D9-4128-450A-A3B1-4FC08C228B8D', 3)
    result = graph.compute_radial_data('C3FDE0D9-4128-450A-A3B1-4FC08C228B8D', 6)
    result = graph.compute_radial_data('C3FDE0D9-4128-450A-A3B1-4FC08C228B8D', 8)

if __name__ == '__main__' :
         main()
