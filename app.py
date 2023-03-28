from flask import Flask, jsonify, request, send_file

from forest import get_tree_rects, get_tree_img

app = Flask(__name__)


@app.route("/", methods=['GET'])
def route_root():
    return jsonify({'msg': 'Welcome to Flask!'})


@app.route('/tree_rects', methods=['POST', 'PUT'])
def tree_rects():
    print(request.files)

    file = request.files['file']
    file_name = './tmp_store.bin'
    file.save(file_name)

    result_file = get_tree_rects(file_name)  # perform some AI magic on this file
    # return as JSON
    return send_file(result_file, as_attachment=True)  # send it back


@app.route('/tree_img', methods=['POST', 'PUT'])
def tree_img():
    print(request.files)

    file = request.files['file']
    file_name = './tmp_store.bin'
    file.save(file_name)

    result_file = get_tree_img(file_name)  # perform some AI magic on this file
    return send_file(result_file, as_attachment=True)  # send it back
