from flask import Flask

from mock_graph_data import edges
from mem_graph import Graph
import sys
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "<p>Graph search demo with OpenSearch</p>"

@app.route('/paths/<start_id>|<end_id>/<int:distance>')
# e.g. http://localhost:5001/paths/dbb1c6a5-cf52-4374-aeb0-19715f3f5c7c|4628:18/2
def paths(start_id, end_id, distance):
    print(f'Requests path from {start_id} to {end_id} with distance = {distance}')
    paths, time_elapsed = graph.get_all_paths(start_id, end_id, distance)
    json_paths = json.loads(paths)
    result = {
        '_data_source': graph.repo_type,
        '_search_details': f'Find path between {start_id} and {end_id} with distance = {distance}',
        '_search_performance': f'Searched {graph.opensearch.size()} nodes in {time_elapsed} seconds.',
        'paths_found': len(json_paths),
        'valid_paths': json_paths
    }
    return result

@app.route('/radial/<node_id>/<int:degree>')
# e.g. http://localhost:5001/radial/dbb1c6a5-cf52-4374-aeb0-19715f3f5c7c/3
def radial(node_id, degree):
    print(f'Requests radial graph from {node_id} within 3 degree(s)')
    node_radial, time_elapsed = graph.get_radial_data(node_id, 3)
    result = {
        '_data_source': graph.repo_type,
        '_search_details': f'Find node {node_id} neighborhood within {degree} degree(s)',
        '_search_performance': f'Searched {graph.opensearch.size()} nodes in {time_elapsed} seconds.',
        'node_radial': json.loads(node_radial),
    }
    return result


if __name__ == "__main__":
    global graph
    data_source = sys.argv[1]
    max_radial_degree = int(sys.argv[2])
    graph = Graph(max_radial_degree, data_source)
    app.run(host='0.0.0.0', port=5001, debug=True)
