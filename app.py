from flask import Flask, request, make_response
import os
from elasticsearch import Elasticsearch


app = Flask(__name__)
select = ''
for i in os.environ:
    if 'INDEX' in i:
        select += '<option>' +os.environ[i]+'</option>'

@app.route('/')
def hello_world():
    return '<form action=/data><select name=index>'+select+'</select><br>ID: <br><input name="id"></input><br>FILENAME:<br> <input name="filename"></input><input type="submit"></input></form>'


def get_url_params():
    id_param = request.args.get('id')
    filename = request.args.get('filename')
    index = request.args.get('index')
    return id_param, filename, index


@app.route('/data', methods=['GET'])
def get_query_string():
    id_search, filename,index = get_url_params()
   # try:
    es = Elasticsearch([{'host': os.environ['ELK'], 'port': 9200}])
    res = es.search(index=index, body={
        "query": {
            "terms": {
                "_id": [id_search]
            }
        }
    })
    for i in res['hits']['hits']:
        source = i['_source']
        delimeter = "#" * 50
        outstring = ''
        print(source)
        if '@timestamp' in source:
            outstring += '@timestamp:' + str(source['@timestamp']) + "\n" + delimeter + "\n"
        if 'api' in source:
            outstring += 'API:' + str(source['api']) + "\n" + delimeter + "\n"

        if 'User' in source:
            outstring += 'User:' + str(source['User']) + "\n" + delimeter + "\n"
        if 'request' in source:
            if 'url' in source['request']:
                outstring += 'Request URL:' + str(source['request']['url']) + "\n" + delimeter + "\n"
            if 'Host' in source['request']:
                outstring += 'Host:' + str(source['Host']) + "\n" + delimeter + "\n"
        if 'response' in source:
            if 'body' in source['response']:
                outstring += 'ResponseBody:' + str(source['response']['body']) + "\n" + delimeter + "\n"
            if 'statusCode' in source['response']:
                outstring += 'Response statusCode:' + str(source['response']['statusCode']) + "\n" + delimeter + "\n"
        if 'RequestBody' in source:
            outstring += 'RequestBody:' + str(source['RequestBody']) + "\n" + delimeter + "\n"
        if 'ResponseBody' in source:
            outstring += 'ResponseBody:' + str(source['ResponseBody']) + "\n" + delimeter + "\n"

        if 'message' in source:
            outstring += 'message:' + str(source['message']) + "\n" + delimeter + "\n"
        if 'exceptions' in source:
            outstring += 'exceptions:' + str(source['exceptions']) + "\n" + delimeter + "\n"
        if 'TraceId' in source:
            outstring += 'TraceId:' + str(source['TraceId']) + "\n" + delimeter + "\n"

   # except:
    #    outstring = 'Server is not resolved'

    try:
        resp = make_response(outstring)
    except UnboundLocalError:
        outstring = 'ID is not recognized'
        resp = make_response(outstring)
    resp.headers['Content-Type'] = 'text/plain'
    resp.headers['Content-Disposition'] = 'attachment;filename="' + filename + '.txt"'
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0')
