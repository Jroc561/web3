import graphene
import requests
import os
import json
import requests
import base58
import binascii

def query_subgraph(subgraph_url, query, variables=None): 
    request_json = {'query': query}
    if variables:
        request_json['variables'] = variables
    resp = requests.post(subgraph_url, json = request_json)
    data = json.loads(resp.text)
    return data['data']

def list_of_graphs():
    query = """
{
  subgraphs {
    displayName
    currentVersion {
      subgraphDeployment {
        id
        originalName
      }
    }
  }
}
            """
    queryEndpoint = "https://gateway-testnet.thegraph.com/network"
    graphIds = []
    deployedGraphs = []
    cmd = "graph indexer connect http://localhost:8000;graph indexer rules get all -o json | grep deployment | grep -v -e global"
    returned_value = os.popen(cmd)
    graphJson = returned_value.readlines()
    for i in graphJson:
      try:
        temp = (i.split()[1])
        if "," in temp:
          temp = temp.replace(",","")
        if "\"" in temp:
          temp = temp.replace("\"","")
        alphanumeric = [character for character in temp if character.isalnum()]
        hexstring="".join(alphanumeric)
        bytes_array = base58.b58decode(hexstring) 
        graphIds.append("0x"+binascii.hexlify(bytes_array[2:]).decode("utf-8"))
      except IndexError:
        print("[]")
    subgraphs = query_subgraph(queryEndpoint,query)
    for i in graphIds:
        for j in subgraphs['subgraphs']:
            try:
                if str(i) == j["currentVersion"]["subgraphDeployment"]["id"]:
                    temp = json.dumps({"id": j["currentVersion"]["subgraphDeployment"]["id"] , "displayName": j["currentVersion"]["subgraphDeployment"]["originalName"]})
                    deployedGraphs.append(temp)
            except TypeError:
                pass
    print(json.dumps({"subgraphs":deployedGraphs}))

def main():
    list_of_graphs()

if __name__ == '__main__':
    main()