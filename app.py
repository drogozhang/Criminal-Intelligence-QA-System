# coding=utf-8
from flask import Flask, jsonify, render_template
from py2neo import Graph, Node, Relationship

app = Flask(__name__)
graph = Graph("http://localhost:7474", username="neo4j", password='n123')
print(graph)


def buildNodes(nodeRecord):
    data = {"id": str(nodeRecord.n._id), "label": next(iter(nodeRecord.n.labels))}
    data.update(nodeRecord.n.properties)

    return {"data": data}


def buildEdges(relationRecord):
    data = {"source": str(relationRecord.r.start_node._id),
            "target": str(relationRecord.r.end_node._id),
            "relationship": relationRecord.r.rel.type}

    return {"data": data}


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
