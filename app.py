from flask import Flask, jsonify, render_template, redirect
from py2neo import Graph
from flask import request
import json
import re
from text_classifier._test import predict
import config as cfg

app = Flask(__name__)
graph = Graph("http://localhost:7474/db/data/", user="neo4j", password="n123")
app.jinja_env.variable_start_string = '{{ '
app.jinja_env.variable_end_string = ' }}'


def nodesClassify(n):
    """return data"""
    if str(n.labels()) == "SetView({'People'})":
        data = {"label": re.findall(r"'(.+?)'", str(n.labels()))[0],
                "id": str(n.get("person_id")), "name": str(n.get("name"))
                }
    elif str(n.labels()) == "SetView({'Penalty'})":
        data = {"label": re.findall(r"'(.+?)'", str(n.labels()))[0]
            , "id": str(n.get("penalty_id")), "name": str(n.get("name"))
            , "sentence": str(n.get("sentence"))
            , "sentence_years": str(n.get("sentence_years"))
            , "property_penalty_type": str(n.get("property_penalty_type"))
            , "property_penalty_amount": str(n.get("property_penalty_amount"))}
    elif str(n.labels()) == "SetView({'Drugs'})":
        data = {"label": re.findall(r"'(.+?)'", str(n.labels()))[0]
            , "id": str(n.get("drug_id")), "name": str(n.get("name"))
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
            , "location": str(n.get("location"))
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
    if re.findall(r":(.+?) ", a)[0] == "appear":
        data = {"target": re.findall(r":(.[0-9]*),", a)[0],
                "source": re.findall(r":(.[0-9]*)}", a)[0],
                "relationship": re.findall(r":(.+?) ", a)[0]}
    elif re.findall(r":(.+?) ", a)[0] == "contain":
        data = {"target": re.findall(r":(.[0-9]*),", a)[0],
                "source": re.findall(r":(.[0-9]*)}", a)[0],
                "relationship": re.findall(r":(.+?) ", a)[0]}
    elif re.findall(r":(.+?) ", a)[0] == "involve":
        data = {"target": re.findall(r":(.[0-9]*),", a)[0],
                "source": re.findall(r":(.[0-9]*)}", a)[0],
                "relationship": re.findall(r":(.+?) ", a)[0]}
    elif re.findall(r":(.+?) ", a)[0] == "involved_in":
        data = {"target": re.findall(r":(.[0-9]*),", a)[0],
                "source": re.findall(r":(.[0-9]*)}", a)[0],
                "relationship": re.findall(r":(.+?) ", a)[0]}
    elif re.findall(r":(.+?) ", a)[0] == "judge":
        data = {"target": re.findall(r":(.[0-9]*),", a)[0],
                "source": re.findall(r":(.[0-9]*)}", a)[0],
                "relationship": re.findall(r":(.+?) ", a)[0]}
    elif re.findall(r":(.+?) ", a)[0] == "judged_by":
        data = {"target": re.findall(r":(.[0-9]*),", a)[0],
                "source": re.findall(r":(.[0-9]*)}", a)[0],
                "relationship": re.findall(r":(.+?) ", a)[0]}
    elif re.findall(r":(.+?) ", a)[0] == "punishe":
        data = {"target": re.findall(r":(.[0-9]*),", a)[0],
                "source": re.findall(r":(.[0-9]*)}", a)[0],
                "relationship": re.findall(r":(.+?) ", a)[0]}
    elif re.findall(r":(.+?) ", a)[0] == "punished_by":
        data = {"target": re.findall(r":(.[0-9]*),", a)[0],
                "source": re.findall(r":(.[0-9]*)}", a)[0],
                "relationship": re.findall(r":(.+?) ", a)[0]}
    else:
        print("213")
    return {"data": data}


@app.route('/')
def index():
    return render_template('index.html', search_sentence="")
    # return render_template('index1.html', result=None)


@app.route('/<string:search_sentence>')
def index_(search_sentence):
    return render_template('index.html', search_sentence=search_sentence)


# @app.route('/graph/<string:search_sentence>')
# def index_(search_sentence):
#     predict_result = get_graph(search_sentence)
#     print(predict_result)
#     print(type(predict_result))
#     print(predict_result['nodes'][0]['data']['label'])
#     return render_template('index1.html', result=predict_result)


def neo4jstr(original_str):
    return "\"" + original_str + "\""


@app.route('/graph/<string:search_sentence>')
def get_graph(search_sentence):
    if search_sentence == "":
        return
    print(search_sentence)
    advanced_problem, problem_type, keyword_ls = predict(search_sentence)
    if advanced_problem:
        print("Problem Type", cfg.ADVANCED_PROBLEM_TYPE[problem_type])
        print("Catched Named Entity", keyword_ls)
    if advanced_problem:  # people related.
        if problem_type == 0:
            if len(keyword_ls) != 1:
                raise KeyError("Key words number for search is wrong!")
            person_name = neo4jstr(keyword_ls[0])
            people_nodes = list(map(buildNodes, list(
                graph.run(
                    "Match (n:People{name: " + str(person_name) + "})-[:involved_in]->(end:Cases) return n").data())))
            case_nodes = list(map(buildNodes, list(
                graph.run(
                    "Match (n:People{name: " + str(person_name) + "})-[:involved_in]->(end:Cases) return end").data())))
            nodes = people_nodes + case_nodes
            count = str("'count(n)': 0")
            edges = list(map(buildEdges, list(
                graph.run(
                    "Match (n:People{name: " + str(person_name) + "})-[r:involved_in]->(end:Cases) return r").data())))
            return jsonify(elements={"nodes": nodes, "edges": edges, "count": count})
        if problem_type == 1:
            if len(keyword_ls) != 2:
                raise KeyError("Key words number for search is wrong!")
            try:
                year, court_name = str(int(keyword_ls[0])), neo4jstr(keyword_ls[1])
            except:
                year, court_name = str(int(keyword_ls[1])), neo4jstr(keyword_ls[0])
            nodes = list(map(buildNodes, list(
                graph.run("Match (n:Cases{court_name: " + court_name + ",year: " + year + "})return n").data())))
            edges = {}
            count = str(
                graph.run("Match (n:Cases{court_name: " + court_name + ",year: " + year + "})return count(n)").data()[
                    0])
            return jsonify(elements={"nodes": nodes, "edges": edges, "count": count})
        if problem_type == 2:
            if len(keyword_ls) != 2:
                raise KeyError("Key words number for search is wrong!")
            court_name, drugs_name = neo4jstr(keyword_ls[0]), neo4jstr(keyword_ls[1])
            case_nodes_1 = list(map(buildNodes, list(graph.run(
                "Match (n:Cases{court_name: " + court_name + "})-[:contain]->(end:Drugs{name:" + drugs_name + "}) return n").data())))
            drug_nodes_1 = list(map(buildNodes, list(graph.run(
                "Match (n:Cases{court_name: " + court_name + "})-[:contain]->(end:Drugs{name:" + drugs_name + "}) return end").data())))
            edges = list(map(buildEdges, list(graph.run(
                "Match (n:Cases{court_name: " + court_name + "})-[r:contain]->(end:Drugs{name:" + drugs_name + "}) return r").data())))
            quantity_count = graph.run(  # bug here
                "Match (end:Cases{court_name: " + court_name + "})-[:contain]->(n:Drugs{name:" + drugs_name + "}) return sum(n.drug_quantity)").data()[
                0]['sum(n.drug_quantity)']

            nodes = case_nodes_1 + drug_nodes_1
            if drugs_name == '"冰毒"':
                case_nodes_2 = list(map(buildNodes, list(graph.run(
                    "Match (n:Cases{court_name: " + court_name + "})-[:contain]->(end:Drugs{name:'甲基苯丙胺'}) return n").data())))
                drug_nodes_2 = list(map(buildNodes, list(graph.run(
                    "Match (n:Cases{court_name: " + court_name + "})-[:contain]->(end:Drugs{name:'甲基苯丙胺'}) return end").data())))
                edges2 = list(map(buildEdges, list(graph.run(
                    "Match (n:Cases{court_name: " + court_name + "})-[r:contain]->(end:Drugs{name:'甲基苯丙胺'}) return r").data())))
                nodes += case_nodes_2 + drug_nodes_2
                edges += edges2
                quantity_count += graph.run(
                    "Match (end:Cases{court_name: " + court_name + "})-[:contain]->(n:Drugs{name:'甲基苯丙胺'}) return sum(n.drug_quantity)").data()[
                    0]['sum(n.drug_quantity)']
            return jsonify(elements={"nodes": nodes, "edges": edges, "count": str(quantity_count)})
        if problem_type == 3:  # avg drug price
            if len(keyword_ls) != 2:
                raise KeyError("Key words number for search is wrong!")
            court_name, drugs_name = neo4jstr(keyword_ls[0]), neo4jstr(keyword_ls[1])
            case_nodes_1 = list(map(buildNodes, list(graph.run(
                "Match (n:Cases{court_name: " + court_name + "})-[:contain]->(end:Drugs{name:" + drugs_name + "}) return n").data())))
            drug_nodes_1 = list(map(buildNodes, list(graph.run(
                "Match (n:Cases{court_name: " + court_name + "})-[:contain]->(end:Drugs{name:" + drugs_name + "}) return end").data())))
            edges1 = list(map(buildEdges, list(graph.run(
                "Match (n:Cases{court_name: " + court_name + "})-[r:contain]->(end:Drugs{name:" + drugs_name + "}) return r").data())))
            nodes = case_nodes_1 + drug_nodes_1
            edges = edges1
            price_count = graph.run(
                "Match (end:Cases{court_name: " + court_name + "})-[:contain]->(n:Drugs{name:" + drugs_name + "}) where n.drug_unit=\"克\" return avg(n.drug_price)").data()[
                0]
            if drugs_name == '"冰毒"':
                case_nodes_2 = list(map(buildNodes, list(graph.run(
                    "Match (n:Cases{court_name: " + court_name + "})-[:contain]->(end:Drugs{name:'甲基苯丙胺'}) return n").data())))
                drug_nodes_2 = list(map(buildNodes, list(graph.run(
                    "Match (n:Cases{court_name: " + court_name + "})-[:contain]->(end:Drugs{name:'甲基苯丙胺'}) return end").data())))
                edges2 = list(map(buildEdges, list(graph.run(
                    "Match (n:Cases{court_name: " + court_name + "})-[r:contain]->(end:Drugs{name:'甲基苯丙胺'}) return r").data())))
                nodes = case_nodes_1 + drug_nodes_2 + case_nodes_2 + drug_nodes_1
                edges = edges1 + edges2
                price_count1 = graph.run(  # need rectify  '冰毒' or '甲基苯丙胺'
                    "Match (end:Cases{court_name: " + court_name + "})-[:contain]->(n:Drugs{name:" + drugs_name + "}) where n.drug_unit=\"克\" return avg(n.drug_price)").data()[
                    0]['avg(n.drug_price)']
                price_count2 = graph.run(  # need rectify  '冰毒' or '甲基苯丙胺'
                    "Match (end:Cases{court_name: " + court_name + "})-[:contain]->(n:Drugs{name: '甲基苯丙胺'}) where n.drug_unit=\"克\" return avg(n.drug_price)").data()[
                    0]['avg(n.drug_price)']
                price_count = price_count1 + price_count2
            return jsonify(elements={"nodes": nodes, "edges": edges, "count": price_count})
        if problem_type == 4:
            if len(keyword_ls) != 1:
                raise KeyError("Key words number for search is wrong!")
            court_name = neo4jstr(keyword_ls[0])
            nodes = list(map(buildNodes, list(graph.run(
                "Match (n:Cases{court_name: " + court_name + "}) where n.min_age >18 and n.min_age <25 return n").data())))
            edges = {}
            young_number = str((graph.run(
                "Match (n:Cases{court_name: " + court_name + "}) where n.min_age >18 and n.min_age <25 return count(n)").data()))
            all_people_number = str((graph.run(
                "Match (n:Cases{court_name: " + court_name + "}) return count(n)").data()))
            count = "Proportion(n) = " + str(re.findall(r"\d+\.?\d*", young_number)) + "/" + str(
                re.findall(r"\d+\.?\d*", all_people_number))
            return jsonify(elements={"nodes": nodes, "edges": edges, "count": count})
        if problem_type == 5:
            if len(keyword_ls) != 1:
                raise KeyError("Key words number for search is wrong!")
            court_name = neo4jstr(keyword_ls[0])
            nodes = list(map(buildNodes, list(graph.run(
                "Match (n:Cases{court_name: " + court_name + "}) where n.people_involved_num >2 return n").data())))
            edges = {}
            team_crime_num = str((graph.run(
                "Match (n:Cases{court_name: " + court_name + "}) where n.people_involved_num >2 return count(n)").data()))
            all_crime_num = str((graph.run(
                "Match (n:Cases{court_name: " + court_name + "}) return count(n)").data()))
            count = "Proportion(n) = " + str(re.findall(r"\d+\.?\d*", team_crime_num)) + "/" + str(
                re.findall(r"\d+\.?\d*", all_crime_num))
            return jsonify(elements={"nodes": nodes, "edges": edges, "count": count})
        if problem_type == 6:
            if len(keyword_ls) != 1:
                raise KeyError("Key words number for search is wrong!")
            court_name = neo4jstr(keyword_ls[0])
            court_nodes = list(map(buildNodes, list(graph.run(
                "Match (n:Cases{court_name: " + court_name + "}) return n").data())))
            penalty_nodes = list(map(buildNodes, list(graph.run(
                "Match (n:Penalty)-[:punished_by]->(end:Cases{court_name: " + court_name + "}) return n").data())))
            nodes = court_nodes + penalty_nodes
            edges = list(map(buildEdges, list(graph.run(
                "Match (n:Penalty)-[r:punished_by]->(end:Cases{court_name: " + court_name + "}) return r").data())))
            b = str(graph.run(
                "Match (n:Penalty)-[:punished_by]->(end:Cases{court_name: " + court_name + "}) return avg(n.sentence_years)").data()[
                        0])
            count = "avg = " + b + "年"
            print(count)
            return jsonify(elements={"nodes": nodes, "edges": edges, "count": count})
    else:
        if len(keyword_ls) != 1:
            raise KeyError("Key words number for search is wrong!")
        # get_base_graph()
        # todo


# @app.route('/search')
# def search():
#     # 获取提出的问题
#     keyword = request.args.get("query_word")
#     print(keyword)
#     return keyword


@app.route("/mockservice")
def mockservice():
    original_sentence = request.args['query_word']
    print(original_sentence)
    return redirect("/" + original_sentence)


if __name__ == '__main__':
    app.run(debug=True)
