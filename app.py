import os
import traceback

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import torch
from PIL import Image
from deepforest import main
from flask import Flask, jsonify, request, send_file, session

app = Flask(__name__)
app.secret_key = 'deep-forest-plugin'

# globals
setting_keys = ['patch_size', 'patch_overlap', 'thresh', 'iou_threshold']
setting_defaults = {'patch_size': 900,
                    'patch_overlap': 0.4,
                    'thresh': 0.5,
                    'iou_threshold': 0.5}

# load deepforest
model_path = './tmp/forest_model.pl'
# df_model = main.deepforest()
# df_model.use_release()
# torch.save(df_model.model.state_dict(), model_path)
print(' -- Loaded deepforest!')


@app.route("/", methods=['GET'])
def route_root():
    return jsonify({'msg': 'Welcome to Flask!'})


@app.route('/settings', methods=['POST', 'PUT'])
def store_settings():
    settings_json = request.get_json()
    print(settings_json)

    for key in setting_keys:
        if key in settings_json:
            session[key] = settings_json[key]
        else:
            if key in session:
                session.pop(key)
    print(dict(session.items()))
    return jsonify(dict(session.items()))


@app.route('/settings', methods=['GET'])
def view_settings():
    print(session.items())
    return jsonify(dict(session.items()))


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


def get_tree_rects(file_name):
    # load settings from session
    settings = {}
    for key in setting_keys:
        if key in session:
            settings[key] = session[key]
        else:
            settings[key] = setting_defaults[key]

    tree_predictions = []
    again = True
    attempts = 0
    while again:
        try:
            attempts = attempts + 1
            model = main.deepforest()
            model.model.load_state_dict(torch.load(model_path))
            model.config["score_thresh"] = settings['thresh']
            model.config["num_workers"] = 4
            Image.MAX_IMAGE_PIXELS = None
            tree_predictions = model.predict_tile(file_name,
                                                  return_plot=False,
                                                  patch_size=settings['patch_size'],
                                                  patch_overlap=settings['patch_overlap'],
                                                  iou_threshold=settings['iou_threshold'])
            again = False  # dangerous
        except ReferenceError as re:
            print('ReferenceError: ', re)
            traceback.print_exc()
            if attempts > 3:
                again = False  # put some limit to this madness

    if attempts > 1:
        print(' ** Problems occurred, we had to try this ', attempts, ' times...')

    return tree_predictions


def get_tree_img(file_name, patch_size=900, overlap=0.4, thresh=0.5):
    tree_predictions = get_tree_rects(file_name, patch_size, overlap, thresh)

    # render on an image
    img = Image.open(file_name)
    aspect = img.size[0] / img.size[1]
    w = 15  # inches
    h = w / aspect
    fig, ax = plt.subplots(figsize=(w, h))
    ax.imshow(img)

    count = 0
    if tree_predictions is not None:
        for row in tree_predictions.itertuples(index=False):
            x = row[0]
            y = row[1]
            w = row[2] - row[0]
            h = row[3] - row[1]
            color = (row[5], 1, row[5])
            rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor=color, facecolor='none')
            ax.add_patch(rect)
            count = count + 1

    filename_format = "dt_p{0}_o{1:n}_t{2:n}_n{3}.png"
    file_name = 'output/' + filename_format.format(patch_size, overlap * 100, thresh * 100, count)
    plt.savefig(file_name, bbox_inches='tight')

    print(file_name)
    return file_name
