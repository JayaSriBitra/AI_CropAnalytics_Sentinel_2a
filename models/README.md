
# U-Net Model – AI Crop Analytics

## 1. Overview
U-Net is a deep learning architecture used for
semantic image segmentation.

In this project, U-Net is planned to identify
and segment land-cover regions from Sentinel-2A
satellite imagery.

## 2. Proposed Model Architecture
The model follows an encoder-decoder architecture.

- Encoder: Extracts image features.
- Bottleneck: Learns deeper representations.
- Decoder: Reconstructs the segmentation output.
- Skip Connections: Preserve spatial information.

## 3. Proposed Input Configuration
- Input channels: 3
- Input dimensions: 256 × 256
- Input format: Satellite image patches

These are the configuration values described
in the current project README.

## 4. Proposed Output
- Output classes: 8
- Output dimensions: 8 × 256 × 256
- Task: Pixel-wise land-cover segmentation

## 5. Current Development Status
The repository currently contains a placeholder
in the models directory. The U-Net source code
and model training implementation are pending.

## 6. Planned Work
- Implement the U-Net architecture.
- Prepare the training pipeline.
- Connect satellite image datasets.
- Train and validate the model.
- Evaluate segmentation performance.
