from flask import Flask,request,jsonify,send_from_directory
import json
import requests
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__,static_folder='build/')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/predict',methods=['POST'])
@cross_origin()
def api_call():
    API_KEY = "MpNZ7oHbK-90DbY_FBQQs2p7-kPNXgqRVo4nBG2itJjH"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
    API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]
    print(mltoken)
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
    payload_scoring = json.loads(bytes.decode(request.data))
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/44f494ed-fe58-40fa-8321-6f5028f23ed9/predictions?version=2021-05-01', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    return jsonify(response_scoring.json())

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@cross_origin()
def render_ui(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')



if __name__ == '__main__':
   app.run(host='0.0.0.0', port=2000,use_reloader=True,threaded=True)
