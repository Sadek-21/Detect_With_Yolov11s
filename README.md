

# US Uniform Detection Using YOLOv11s with ESP32-CAM

This project demonstrates how to detect US military uniforms using YOLOv11s, trained on a custom dataset, and deployed on an ESP32-CAM module. The model is trained using Google Colab and can be used for real-time object detection via a USB camera or laptop webcam.

---

## Table of Contents
1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Dataset Preparation](#dataset-preparation)
4. [Training the Model](#training-the-model)
5. [Testing the Model](#testing-the-model)
6. [Deploying the Model](#deploying-the-model)
7. [Running the Detection](#running-the-detection)
8. [References](#references)

---

## Overview
This project uses YOLOv11s to detect US military uniforms. The model is trained on a custom dataset labeled using Label Studio and deployed on an ESP32-CAM module for real-time detection. The training process is done in Google Colab, leveraging GPU acceleration for faster results.

---

## Requirements
Before starting, ensure you have the following:
- **Hardware**:
  - ESP32-CAM module
  - ESP32-WROOM module
  - USB camera or laptop webcam
- **Software**:
  - Anaconda (for Label Studio)
  - Google Colab (for training)
  - Python 3.x
  - Ultralytics YOLO library
  - Label Studio (for dataset labeling)
- **Dataset**:
  - 100–200 images of US military uniforms.

---

## Dataset Preparation
1. **Collect Images**:
   - Gather 100–200 images of US military uniforms.
   - Store them in a folder named `uniform_images/`.

2. **Label Images**:
   - Install Anaconda from [here](https://www.anaconda.com/download).
   - Create a new Python environment:
     ```bash
     conda create --name yolo-env1 python=3.12
     conda activate yolo-env1
     ```
   - Install Label Studio:
     ```bash
     pip install label-studio
     ```
   - Start Label Studio:
     ```bash
     label-studio start
     ```
   - Create a new project in Label Studio, import your images, and label them using bounding boxes. Export the labels in YOLO format.

3. **Prepare Dataset**:
   - After labeling, you’ll get a folder with `images/`, `labels/`, `classes.txt`, and `notes.json`.
   - Zip the folder and name it `data.zip`.

---

## Training the Model
1. **Open Google Colab**:
   - Use the [YOLO Training Notebook](https://colab.research.google.com/github/EdjeElectronics/Train-and-Deploy-YOLO-Models/blob/main/Train_YOLO_Models.ipynb).
   - Set the runtime type to **T4 GPU**.

2. **Upload Dataset**:
   - Drag and drop `data.zip` into the Colab file explorer.
   - Unzip the dataset:
     ```bash
     !unzip -q /content/data.zip -d /content/custom_data
     ```

3. **Split Dataset**:
   - Run the following commands to split the dataset into training and validation sets:
     ```bash
     !wget -O /content/train_val_split.py https://raw.githubusercontent.com/EdjeElectronics/Train-and-Deploy-YOLO-Models/refs/heads/main/utils/train_val_split.py
     !python train_val_split.py --datapath="/content/custom_data" --train_pct=0.9
     ```

4. **Install Dependencies**:
   - Install the Ultralytics library:
     ```bash
     !pip install ultralytics
     ```

5. **Create `data.yaml`**:
   - Run the following script to generate the configuration file:
     ```python
     import yaml
     import os

     def create_data_yaml(path_to_classes_txt, path_to_data_yaml):
         with open(path_to_classes_txt, 'r') as f:
             classes = [line.strip() for line in f.readlines() if line.strip()]
         data = {
             'path': '/content/data',
             'train': 'train/images',
             'val': 'validation/images',
             'nc': len(classes),
             'names': classes
         }
         with open(path_to_data_yaml, 'w') as f:
             yaml.dump(data, f, sort_keys=False)
         print(f'Created config file at {path_to_data_yaml}')

     create_data_yaml('/content/custom_data/classes.txt', '/content/data.yaml')
     ```

6. **Train the Model**:
   - Start training:
     ```bash
     !yolo detect train data=/content/data.yaml model=yolo11s.pt epochs=60 imgsz=640
     ```

---

## Testing the Model
1. **Run Predictions**:
   - Test the model on validation images:
     ```bash
     !yolo detect predict model=runs/detect/train/weights/best.pt source=data/validation/images save=True
     ```

2. **View Results**:
   - Display the predicted images:
     ```python
     import glob
     from IPython.display import Image, display
     for image_path in glob.glob(f'/content/runs/detect/predict/*.jpg')[:10]:
         display(Image(filename=image_path, height=400))
     ```

---

## Deploying the Model
1. **Download the Model**:
   - Zip and download the trained model:
     ```bash
     !mkdir /content/my_model
     !cp /content/runs/detect/train/weights/best.pt /content/my_model/my_model.pt
     !cp -r /content/runs/detect/train /content/my_model
     %cd my_model
     !zip /content/my_model.zip my_model.pt
     !zip -r /content/my_model.zip train
     %cd /content
     ```

2. **Install Dependencies Locally**:
   - Install the Ultralytics library:
     ```bash
     pip install ultralytics
     ```
   - Install PyTorch with CUDA (if you have an NVIDIA GPU):
     ```bash
     pip3 install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
     ```

---

## Running the Detection
1. **From USB Camera**:
   - Run the detection script:
     ```bash
     python yolo_detect.py --model my_model.pt --source usb0 --resolution 1280x720
     ```

2. **From Laptop Webcam**:
   - Run the detection script:
     ```bash
     python yolo_detect.py --model my_model.pt --source 0 --resolution 1280x720
     ```

---

## References
- [YOLOv11s Training Tutorial](https://www.youtube.com/watch?v=r0RspiLG260)
- [Label Studio](https://labelstud.io/)
- [Ultralytics YOLO Documentation](https://docs.ultralytics.com/)

---
