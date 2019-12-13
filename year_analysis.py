import networkx as nx
from genderize import Genderize
import gender_guesser.detector as gender
d = gender.Detector()

f = open('edges_with_year.csv', 'r', encoding = 'utf-8')
tmpf = f.readlines()

year_dict = dict()
for item in tmpf:
    tmp = item.strip(' \n').split(',')
    author1 = tmp[0]
    author2 = tmp[1]
    if author1 == '' and author2 == '':
        continue
    year = int(tmp[2].strip(' '))
    if year not in year_dict:
        year_dict[year] = []
        year_dict[year].append([author1, author2])
    else:
        year_dict[year].append([author1, author2])
        
result_dict = dict()

for year in year_dict:
    
    year_edges = year_dict[year]
    G = nx.Graph(year_edges)

    # remove self-loop edge
    loops = list(G.selfloop_edges())
    # print(loops)
    G.remove_edges_from(loops)

    for n in G.nodes():
        first = n.split(' ', 1)[0]
        G.nodes[n]['gender'] = d.get_gender(first)
        
    #removing unknown or andy
    nodes = []
    nodes = G.nodes()
    delNodes = []
    print(G.number_of_nodes())
    for n in nodes:
        if str(G.nodes[n]['gender']) == "andy" :
            delNodes.append(n)
        elif str(G.nodes[n]['gender']) == "unknown":
            delNodes.append(n)

    G.remove_nodes_from(delNodes)
    print(G.number_of_nodes())
    
    mix_cnt = 0
    for edge in G.edges:
        node1 = edge[0]
        node2 = edge[1]
        if (str(G.nodes[node1]['gender']) == "female" and str(G.nodes[node2]['gender']) == "male") or (str(G.nodes[node1]['gender']) == "male" and str(G.nodes[node2]['gender']) == "female"):
            mix_cnt += 1

    # calculate total number of male and female, their sum degree
    male_degree, female_degree = 0, 0
    male_cnt, female_cnt = 0, 0
    for n in G.nodes():
        if (str(G.nodes[n]['gender']) == "female"):
            female_degree += G.degree[n]
            female_cnt += 1
        else:
            male_degree += G.degree[n]
            male_cnt += 1
    # calculate total number of edges
    edges2 = 2 * len(list(G.edges))
    result_dict[year] = [male_degree, female_degree, male_cnt, female_cnt, edges2, mix_cnt]
    
f = open('result_1.csv', 'w')
for res in result_dict:
    tmp = result_dict[res]
    f.write(str(res)+','+str(tmp[0])+','+str(tmp[1])+','+str(tmp[2])+','+str(tmp[3])+','+str(tmp[4])+','+str(tmp[5])+'\n')
f.close()