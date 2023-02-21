# Graph Algorithms using OpenSearch as Repo

## About

This repository is a reference implementation of efficiently storing and querying graph data with a Python Flask API and OpenSearch.
This project is containerised so both `docker-compose` and `docker` commands would work. 

The source code indexes relationship data on OpenSearch and implements the following 2 algorithms

1. Given a start node, retrieve the Graph of connected nodes with 3 degrees. 
   - The radial search is currently optimised for 3 degrees. But the system is easily extensible to other number of degrees.
2. Given a start and destination node, retrive all paths with n degrees of separation

The implementation for radial graph generation is mainly based on BFS, while path search from radial data is implemented with DFS algorithm.
Relationship type of graph edges are also cached in the resulting radial graph.

The pre-processing is currently being triggered at initiation of the Flask API web app. 

## Getting started locally (docker-compose)

OpenSearch nodes and OpenSearch Dashboards will run in a docker container. While the Flask API app and the pre-processing module will run together in a separate container.

1. Clone the repo
2. `docker-compose up -d`
3. `Usage - Radial search: http://localhost:5001/radial/dbb1c6a5-cf52-4374-aeb0-19715f3f5c7c/3`
        /radial/<start_node_id>/<int:degree>
4. `Usage - Find all the Paths: http://localhost:5001/paths/dbb1c6a5-cf52-4374-aeb0-19715f3f5c7c|4628:18/2`
        /paths/<start_id>|<end_id>/<int:distance>

## Getting started when OpenSearch is deployed remotely (docker)

1. Clone the repo
2. Spin up your OpenSearch cluster
3. Modify `opensearch_repo.py` to connect to your OpenSearch cluster

4. Build and start:
- `docker build -t py-opensearch-graph . `
- `docker run -d -p 5001:5001 --name=opensearch-graph -t py-opensearch-graph`
- `docker logs -f --tail 5 opensearch-graph`

5. Terminate:
- `docker stop opensearch-graph`
- `docker rm opensearch-graph`

## More Documentation will follow....
