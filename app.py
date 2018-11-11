from flask import Flask, jsonify, render_template
from py2neo import Graph, Node
from flask import request
import re

app = Flask(__name__)
graph = Graph("http://localhost:7474/db/data/", user="neo4j",  password="123456")

def nodesClassify(n):
    """return data"""
    if str(n.labels()) == "SetView({'People'})":
        data = {"label": re.findall(r"'(.+?)'",str(n.labels()))[0],
                "id": str(n.get("person_id")), "name": str(n.get("name"))
                }
    elif str(n.labels()) == "SetView({'Penalty'})":
        data = {"label": re.findall(r"'(.+?)'", str(n.labels()))[0]
            ,"id": str(n.get("penalty_id")), "name": str(n.get("name"))
            ,"sentence" : str(n.get("sentence"))
            , "sentence_years": str(n.get("sentence_years"))
            , "property_penalty_type": str(n.get("property_penalty_type"))
            , "property_penalty_amount": str(n.get("property_penalty_amount"))}
    elif str(n.labels()) == "SetView({'Drugs'})":
        data = {"label": re.findall(r"'(.+?)'", str(n.labels()))[0]
            ,"id": str(n.get("drug_id")), "name": str(n.get("name"))
            , "drug_quantity": str(n.get("drug_quantity"))
            , "drug_unit": str(n.get("drug_unit"))
            , "drug_price": str(n.get("drug_price"))
            , "drug_amount": str(n.get("drug_amount"))}
    elif str(n.labels()) == "SetView({'Crime'})":
        data = {"label": re.findall(r"'(.+?)'", str(n.labels()))[0]
            , "id": str(n.get("crime_id")), "name": str(n.get("name"))}
    elif str(n.labels()) == "SetView({'Cases'})":
        data = {"label": re.findall(r"'(.+?)'", str(n.labels()))[0]
            , "id": str(n.get("case_id")), "name": str(n.get("name"))
            ,"location": str(n.get("location"))
            , "court_name": str(n.get("court_name"))
            , "min_birth": str(n.get("min_birth"))
            , "min_age": str(n.get("min_age"))
            , "people_involved_num": str(n.get("people_involved_num"))
            , "year": str(n.get("year"))}
    return data


def buildNodes(nodeRecord):
    if nodeRecord.get("n"):
        n = nodeRecord.get("n")
        data = nodesClassify(n)
        return {"data": data}
    else:
        n = nodeRecord.get("end")
        data = nodesClassify(n)
        return {"data": data}


def buildEdges(relationRecord):
    a = str(relationRecord.get("r"));
    if re.findall(r":(.+?) ",a)[0] == "appear":
        data = {"target": re.findall(r":(.[0-9]*),",a)[0],
                "source": re.findall(r":(.[0-9]*)}",a)[0],
                "relationship": re.findall(r":(.+?) ",a)[0] }
    elif re.findall(r":(.+?) ",a)[0] == "contain":
        data = {"target": re.findall(r":(.[0-9]*),", a)[0],
                "source": re.findall(r":(.[0-9]*)}", a)[0],
                "relationship": re.findall(r":(.+?) ", a)[0]}
    elif re.findall(r":(.+?) ",a)[0] == "involve":
        data = {"target": re.findall(r":(.[0-9]*),", a)[0],
                "source": re.findall(r":(.[0-9]*)}", a)[0],
                "relationship": re.findall(r":(.+?) ", a)[0]}
    elif re.findall(r":(.+?) ",a)[0] == "involved_in":
        data = {"target": re.findall(r":(.[0-9]*),", a)[0],
                "source": re.findall(r":(.[0-9]*)}", a)[0],
                "relationship": re.findall(r":(.+?) ", a)[0]}
    elif re.findall(r":(.+?) ",a)[0] == "judge":
        data = {"target": re.findall(r":(.[0-9]*),", a)[0],
                "source": re.findall(r":(.[0-9]*)}", a)[0],
                "relationship": re.findall(r":(.+?) ", a)[0]}
    elif re.findall(r":(.+?) ",a)[0] == "judged_by":
        data = {"target": re.findall(r":(.[0-9]*),", a)[0],
                "source": re.findall(r":(.[0-9]*)}", a)[0],
                "relationship": re.findall(r":(.+?) ", a)[0]}
    elif re.findall(r":(.+?) ",a)[0] == "punishe":
        data = {"target": re.findall(r":(.[0-9]*),", a)[0],
                "source": re.findall(r":(.[0-9]*)}", a)[0],
                "relationship": re.findall(r":(.+?) ", a)[0]}
    elif re.findall(r":(.+?) ",a)[0] == "punished_by":
        data = {"target": re.findall(r":(.[0-9]*),", a)[0],
                "source": re.findall(r":(.[0-9]*)}", a)[0],
                "relationship": re.findall(r":(.+?) ", a)[0]}
    else:
        print("213")
    return {"data": data}
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graph')
def get_graph():

    #question_1
    # name = str("'周爱美'")
    # nodes1= list(map(buildNodes,list(graph.run("Match (n:People{name: "+str(name)+"})-[:involved_in]->(end:Cases) return n").data())))
    # nodes2 = list(map(buildNodes, list(graph.run("Match (n:People{name: " + str(name) + "})-[:involved_in]->(end:Cases) return end").data())))
    # nodes = nodes1 + nodes2
    # count = str("'count(n)': 0")
    # edges = list(map(buildEdges, list(graph.run("Match (n:People{name: " + str(name) + "})-[r:involved_in]->(end:Cases) return r").data())))

    #question_2
    # court_name = str("'温州市龙湾区'")
    # year = "2017"
    # nodes= list(map(buildNodes,list(graph.run("Match (n:Cases{court_name: "+court_name+",year: "+year+"})return n").data())))
    # edges ={}
    # count = str(graph.run("Match (n:Cases{court_name: "+court_name+",year: "+year+"})return count(n)").data()[0])
    # return jsonify(elements={"nodes": nodes, "edges": edges,"count":count})

    # # question_3
    # court_name = str("'温州市龙湾区'")
    # drugs_name = "'海洛因'"
    # if (drugs_name == "'冰毒'"):
    #     nodes1 = list(map(buildNodes, list(graph.run(
    #         "Match (n:Cases{court_name: " + court_name + "})-[:contain]->(end:Drugs{name:" + drugs_name + "}) return n").data())))
    #     nodes2 = list(map(buildNodes, list(graph.run(
    #         "Match (n:Cases{court_name: " + court_name + "})-[:contain]->(end:Drugs{name:'甲基苯丙胺'}) return n").data())))
    #     nodes3 = list(map(buildNodes, list(graph.run(
    #         "Match (n:Cases{court_name: " + court_name + "})-[:contain]->(end:Drugs{name:" + drugs_name + "}) return end").data())))
    #     nodes4 = list(map(buildNodes, list(graph.run(
    #         "Match (n:Cases{court_name: " + court_name + "})-[:contain]->(end:Drugs{name:'甲基苯丙胺'}) return end").data())))
    #     nodes = nodes1 + nodes2 + nodes3 + nodes4
    #     edges1 = list(map(buildEdges, list(graph.run(
    #         "Match (n:Cases{court_name: " + court_name + "})-[r:contain]->(end:Drugs{name:" + drugs_name + "}) return r").data())))
    #     edges2 = list(map(buildEdges, list(graph.run(
    #         "Match (n:Cases{court_name: " + court_name + "})-[r:contain]->(end:Drugs{name:'甲基苯丙胺'}) return r").data())))
    #     edges = edges1 + edges2
    #     count = str(graph.run(
    #         "Match (end:Cases{court_name: "+court_name+"})-[:contain]->(n:Drugs{name:"+drugs_name+"}) return sum(n.drug_quantity)").data()[0])
    # else:
    #     nodes1 = list(map(buildNodes, list(graph.run(
    #         "Match (n:Cases{court_name: " + court_name + "})-[:contain]->(end:Drugs{name:" + drugs_name + "}) return n").data())))
    #     nodes2 = list(map(buildNodes, list(graph.run(
    #         "Match (n:Cases{court_name: " + court_name + "})-[:contain]->(end:Drugs{name:" + drugs_name + "}) return end").data())))
    #     nodes  = nodes1 + nodes2
    #     edges = list(map(buildEdges, list(graph.run(
    #         "Match (n:Cases{court_name: " + court_name + "})-[r:contain]->(end:Drugs{name:" + drugs_name + "}) return r").data())))
    #     count = str(graph.run(
    #         "Match (end:Cases{court_name: " + court_name + "})-[:contain]->(n:Drugs{name:" + drugs_name + "}) return sum(n.drug_quantity)").data()[0])
    # return jsonify(elements={"nodes": nodes, "edges": edges,"count":count})

    # question_4
    # court_name = str("'温州市龙湾区'")
    # drugs_name = "'海洛因'"
    # if (drugs_name == "'冰毒'"):
    #     nodes1 = list(map(buildNodes, list(graph.run(
    #         "Match (n:Cases{court_name: " + court_name + "})-[:contain]->(end:Drugs{name:" + drugs_name + "}) return n").data())))
    #     nodes2 = list(map(buildNodes, list(graph.run(
    #         "Match (n:Cases{court_name: " + court_name + "})-[:contain]->(end:Drugs{name:'甲基苯丙胺'}) return n").data())))
    #     nodes3 = list(map(buildNodes, list(graph.run(
    #         "Match (n:Cases{court_name: " + court_name + "})-[:contain]->(end:Drugs{name:" + drugs_name + "}) return end").data())))
    #     nodes4 = list(map(buildNodes, list(graph.run(
    #         "Match (n:Cases{court_name: " + court_name + "})-[:contain]->(end:Drugs{name:'甲基苯丙胺'}) return end").data())))
    #     nodes = nodes1 + nodes2 + nodes3 + nodes4
    #     edges1 = list(map(buildEdges, list(graph.run(
    #         "Match (n:Cases{court_name: " + court_name + "})-[r:contain]->(end:Drugs{name:" + drugs_name + "}) return r").data())))
    #     edges2 = list(map(buildEdges, list(graph.run(
    #         "Match (n:Cases{court_name: " + court_name + "})-[r:contain]->(end:Drugs{name:'甲基苯丙胺'}) return r").data())))
    #     edges = edges1 + edges2
    #     count = str(graph.run(
    #         "Match (end:Cases{court_name: " + court_name + "})-[:contain]->(n:Drugs{name:" + drugs_name + "}) where n.drug_unit=\"克\" return avg(n.drug_price)").data()[0])
    # else:
    #     nodes1 = list(map(buildNodes, list(graph.run(
    #         "Match (n:Cases{court_name: " + court_name + "})-[:contain]->(end:Drugs{name:" + drugs_name + "}) return n").data())))
    #     nodes2 = list(map(buildNodes, list(graph.run(
    #         "Match (n:Cases{court_name: " + court_name + "})-[:contain]->(end:Drugs{name:" + drugs_name + "}) return end").data())))
    #     nodes  = nodes1 + nodes2
    #     edges = list(map(buildEdges, list(graph.run(
    #         "Match (n:Cases{court_name: " + court_name + "})-[r:contain]->(end:Drugs{name:" + drugs_name + "}) return r").data())))
    #     count = str(graph.run(
    #         "Match (end:Cases{court_name: " + court_name + "})-[:contain]->(n:Drugs{name:" + drugs_name + "}) where n.drug_unit=\"克\" return avg(n.drug_price)").data()[0])
    # return jsonify(elements={"nodes": nodes, "edges": edges,"count":count})

    # # question_5
    # court_name = str("'温州市龙湾区'")
    # nodes = list(map(buildNodes, list(graph.run(
    #     "Match (n:Cases{court_name: "+court_name+"}) where n.min_age >18 and n.min_age <25 return n").data())))
    # edges = {}
    # a= str((graph.run(
    #     "Match (n:Cases{court_name: "+court_name+"}) where n.min_age >18 and n.min_age <25 return count(n)").data()))
    # b = str((graph.run(
    #     "Match (n:Cases{court_name: " + court_name + "}) return count(n)").data()))
    # count = "Proportion(n) = " + str(re.findall(r"\d+\.?\d*",a))+"/"+str(re.findall(r"\d+\.?\d*",b))
    # return jsonify(elements={"nodes": nodes, "edges": edges,"count":count})

    # # question_6
    # court_name = str("'温州市龙湾区'")
    # nodes = list(map(buildNodes, list(graph.run(
    #     "Match (n:Cases{court_name: "+court_name+"}) where n.people_involved_num >2 return n").data())))
    # edges = {}
    # a= str((graph.run(
    #     "Match (n:Cases{court_name: "+court_name+"}) where n.people_involved_num >2 return count(n)").data()))
    # b = str((graph.run(
    #     "Match (n:Cases{court_name: " + court_name + "}) return count(n)").data()))
    # count = "Proportion(n) = " + str(re.findall(r"\d+\.?\d*",a))+"/"+str(re.findall(r"\d+\.?\d*",b))
    # return jsonify(elements={"nodes": nodes, "edges": edges,"count":count})

    # question_7
    court_name = str("'温州市龙湾区'")
    nodes1 = list(map(buildNodes, list(graph.run(
        "Match (n:Cases{court_name: "+court_name+"}) return n").data())))
    nodes2 = list(map(buildNodes, list(graph.run(
        "Match (n:Penalty)-[:punished_by]->(end:Cases{court_name: "+court_name+"}) return n").data())))
    nodes = nodes1 +nodes2
    edges = list(map(buildEdges, list(graph.run(
        "Match (n:Penalty)-[r:punished_by]->(end:Cases{court_name: " + court_name + "}) return r").data())))
    b = str(graph.run(
        "Match (n:Penalty)-[:punished_by]->(end:Cases{court_name: "+court_name+"}) return avg(n.sentence_years)").data()[0])
    count = "avg = " + b + "年"
    print(count)
    return jsonify(elements={"nodes": nodes, "edges": edges,"count":count})

@app.route('/search')
def search():
    # 获取提出的问题
    keyword = request.args.get("wd")
    print(keyword)

if __name__ == '__main__':
    app.run(debug=True)

