from flask import Flask, request, make_response
import os
from elasticsearch import Elasticsearch
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<form action=/data><input name="id"></input><input type="submit"></input></form>'

def get_url_params():
    id_param = request.args.get('id')
    return id_param

@app.route('/data', methods=['GET'])
def get_query_string():
    id_search = get_url_params()
    try:
        es = Elasticsearch([{'host': os.environ['ELK'], 'port': 9200}])
        res = es.search(index=os.environ['INDEX'], body={
             "query": {
                 "terms": {
                     "_id": [id_search]
                 }
             }
        })
        for i in res['hits']['hits']:
            source = i['_source']
            delimeter = "#"*50
            outstring = ''
            if '@timestamp' in source:
                outstring += '@timestamp:' + str(source['@timestamp']) + "\n" + delimeter +"\n"
            if 'User' in source:
                outstring += 'User:'+ str(source['User']) +"\n" + delimeter +"\n"
            if 'RequestBody' in source:
                outstring += 'RequestBody:' + str(source['RequestBody'])+"\n" + delimeter +"\n"
            if 'ResponseBody' in source:
                outstring += 'ResponseBody:' + str(source['ResponseBody'])+"\n" + delimeter +"\n"
            if 'message' in source:
                outstring += 'message:' + str(source['message']) + "\n" + delimeter +"\n"
            if 'exceptions' in source:
                outstring += 'exceptions:' + str(source['exceptions']) + "\n" + delimeter +"\n"
            if 'TraceId' in source:
                outstring += 'TraceId:' + str(source['TraceId']) + "\n" + delimeter +"\n"
    except:
        outstring = 'Server is not resolved'

    try:
        resp = make_response(outstring)
    except UnboundLocalError:
        outstring = 'ID is not recognized'
        resp = make_response(outstring)
    resp.headers['Content-Type'] = 'text/plain'
    resp.headers['Content - Disposition'] = 'attachment;filename = "MyFileName.txt"'
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0')
