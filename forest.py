import matplotlib.patches as patches
import matplotlib.pyplot as plt
from PIL import Image
from deepforest import main


def detect_trees(file_name, patch_size=900, overlap=0.4, thresh=0.5):
    model = main.deepforest()
    model.use_release()
    model.config["score_thresh"] = thresh
    Image.MAX_IMAGE_PIXELS = None

    filename_format = "dt_p{0}_o{1:n}_t{2:n}_n{3}.png"
    tree_predictions = model.predict_tile(file_name, return_plot=False, patch_size=patch_size, patch_overlap=overlap)

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

    file_name = 'output/' + filename_format.format(patch_size, overlap * 100, thresh * 100, count)
    plt.savefig(file_name, bbox_inches='tight')

    print(file_name)
    return file_name
