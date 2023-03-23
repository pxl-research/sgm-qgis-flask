from flask import Flask, jsonify, request, send_file

from forest import detect_trees

app = Flask(__name__)


@app.route("/", methods=['GET'])
def route_root():
    return jsonify({'msg': 'Welcome to Flask!'})


@app.route('/store', methods=['POST', 'PUT'])
def store_data():
    print(request.files)

    file = request.files['file']
    file_name = './tmp_store.bin'
    file.save(file_name)

    result_file = detect_trees(file_name)  # perform some AI magic on this file
    return send_file(result_file, as_attachment=True)  # send it back
