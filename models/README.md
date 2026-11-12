
# U-Net Model – AI Crop Analytics

## 1. Overview
U-Net is a deep learning architecture used for semantic image segmentation.

In this project, U-Net is designed to segment land-cover regions from Sentinel-2A satellite imagery.

## 2. Model Architecture
The proposed U-Net architecture consists of:

- Encoder: Extracts important features from satellite images.
- Bottleneck: Learns deeper image representations.
- Decoder: Generates the segmentation output.
- Skip Connections: Preserve spatial information between encoder and decoder layers.

## 3. Input Configuration
- Input channels: 3
- Input image size: 256 × 256 pixels
- Input data: Sentinel-2A satellite image patches.

## 4. Output Configuration
- Number of output classes: 8
- Output: Pixel-wise segmentation mask.
- Output size: 256 × 256 pixels.

## 5. Technologies
- Python
- Deep Learning
- U-Net Architecture
- Sentinel-2A Satellite Data

## 6. Planned Implementation
- Develop the U-Net model.
- Prepare training and validation datasets.
- Train the model using satellite imagery.
- Generate segmentation masks.
- Evaluate model performance.

## 7. Expected Outcome
A segmentation model capable of identifying and mapping different land-cover classes from satellite images.
