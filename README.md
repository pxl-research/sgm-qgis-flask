# DeepForest Web Service

### Info

This small package exposes **DeepForest** as a web service using Flask

DeepForest is a python package for airborne object detection and classification.
More info: https://deepforest.readthedocs.io/en/latest/landing.html

## Documentation

### Dependencies
- Python 3.x
- Flask
- Matplotlib
- PIL (Python Imaging Library)
- Torch
- Deep Forest

### Configuration
The application uses the following key settings, which can be configured:
- `patch_size`: Size of the patches the image is divided into for processing.
- `patch_overlap`: Overlap between patches.
- `thresh`: Threshold for object detection.
- `iou_threshold`: Intersection over Union threshold for object detection.

### API Endpoints
The Flask server exposes several API endpoints for image processing and settings management. The key functionalities include:
- Uploading and processing images using the Deep Forest model.
- Adjusting settings for image processing.

### Installation
To install the necessary dependencies, run:
```bash
pip install flask matplotlib torch Pillow deepforest
```

### How to use

To start the server, run:
```
python3 app.py
```

If you run this for the first time, please uncomment the following lines so the model is downloaded and stored
```
# df_model.use_release()
# torch.save(df_model.model.state_dict(), model_path)
```
