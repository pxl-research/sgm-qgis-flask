import os

from flask import Flask, jsonify, request, send_file

from forest import get_tree_rects, get_tree_img

app = Flask(__name__)


@app.route("/", methods=['GET'])
def route_root():
    return jsonify({'msg': 'Welcome to Flask!'})


@app.route('/tree_rects', methods=['POST', 'PUT'])
def tree_rects():
    print(request.files)

    uploaded_file = request.files['file']
    tmp_file_name = './tmp/' + uploaded_file.filename
    uploaded_file.save(tmp_file_name)

    result_df = get_tree_rects(tmp_file_name)  # perform some AI magic on this file
    result_dict = {}  # empty response

    if result_df is not None:
        result_dict = result_df.to_dict('records')

    os.remove(tmp_file_name)  # remove temporary file
    return jsonify(result_dict)  # return as JSON


@app.route('/tree_img', methods=['POST', 'PUT'])
def tree_img():
    print(request.files)

    uploaded_file = request.files['file']
    tmp_file_name = './tmp/' + uploaded_file.filename
    uploaded_file.save(tmp_file_name)

    result_file = get_tree_img(tmp_file_name)  # perform some AI magic on this file

    os.remove(tmp_file_name)  # remove temporary file
    return send_file(result_file, as_attachment=True)  # send annotated file back
