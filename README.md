# 🌾 Crop Analytics Dashboard — U-Net Segmentation + Full-Stack Web App

A GPU-optimised deep learning project for **semantic segmentation** of Sentinel-2 satellite imagery, wrapped in a professional **React + FastAPI** dashboard with real-time analytics, NDVI analysis, yield estimation, AI-powered insights, and a rule-based help chatbot.

---

## 📋 Table of Contents

* [Overview](#-overview)
* [Features](#-features)
* [Tech Stack](#-tech-stack)
* [Project Structure](#-project-structure)
* [Installation](#-installation)
* [Usage](#-usage)
* [API Endpoints](#-api-endpoints)
* [Frontend Pages](#-frontend-pages)
* [Model Architecture](#-model-architecture)
* [GPU Optimisations](#-gpu-optimisations)
* [Database](#-database)
* [Configuration](#-configuration)
* [Results](#-results)
* [License](#-license)

---

## 🎯 Overview

This project implements an **end-to-end crop analysis pipeline**:

1. **Upload** a Sentinel-2 satellite GeoTIFF image.
2. A **U-Net model** segments each pixel into one of 8 land-cover classes.
3. The **dashboard** displays: crop map, class statistics, NDVI value, yield estimation, and AI-generated insights.
4. A floating **AI Chatbot** provides interface guidance.

---

## ✨ Features

| Category | Feature |
|----------|---------|
| **Deep Learning** | U-Net from scratch · 8-class segmentation · 17.2 M params |
| **Training** | Mixed-precision (AMP) · cuDNN benchmark · Dice + CE loss |
| **Backend** | FastAPI · CORS · Auto-generated Swagger docs · Static file serving |
| **Frontend** | React 18 · Tailwind CSS · recharts · Dark mode (class-based) |
| **Analytics** | NDVI analysis · Yield estimation (tons/ha) · Crop statistics charts |
| **AI** | LLM Insights page (Mistral-7B ready) · Rule-based help chatbot |
| **Database** | PostgreSQL 16 + PostGIS 3.4 (models ready, connection deferred) |
| **DevOps** | Production build served from FastAPI · Single-port deployment |

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 18.2, Tailwind CSS, recharts 2.10.4, Lucide React, Axios |
| **Backend** | Python 3.12, FastAPI, Uvicorn, PyTorch, NumPy, Pillow |
| **Database** | PostgreSQL 16, PostGIS 3.4, SQLAlchemy, GeoAlchemy2 |
| **GPU** | CUDA, cuDNN, torch.cuda.amp (mixed precision) |
| **Model** | U-Net (encoder-decoder with skip connections) |

---

## 📁 Project Structure

```
crop_llm_full/
│
├── backend/                    # 🔧 Backend (FastAPI + ML)
│   ├── app.py                  #   Main FastAPI server — all API endpoints
│   ├── model.py                #   U-Net architecture definition
│   ├── dataset.py              #   PyTorch Dataset class for Sentinel-2
│   ├── utils.py                #   Utility functions (metrics, visualisation)
│   ├── train.py                #   Model training script
│   ├── test.py                 #   Model testing / evaluation
│   ├── evaluate.py             #   Detailed evaluation & metrics
│   ├── predict.py              #   Standalone prediction script
│   ├── check_bands.py          #   Raster band inspection
│   ├── check_bands_detailed.py #   Detailed band inspection
│   └── requirements.txt        #   Python dependencies
│
├── frontend/                   # 🖥 Frontend (React + Tailwind)
│   ├── public/
│   ├── src/
│   │   ├── App.jsx             #   Main app — routing, state, dark mode
│   │   ├── index.js            #   React entry point
│   │   ├── styles/
│   │   │   └── index.css       #   Global CSS + dark mode overrides
│   │   ├── components/
│   │   │   ├── Header.jsx          # Top navigation bar
│   │   │   ├── Sidebar.jsx         # Left navigation sidebar
│   │   │   ├── UploadCard.jsx      # Image upload + demo loader
│   │   │   ├── CropMapPanel.jsx    # Segmented crop map display
│   │   │   ├── StatisticsPanel.jsx # Crop statistics & charts
│   │   │   ├── NDVIAnalysis.jsx    # NDVI value, scale, classification
│   │   │   ├── YieldEstimation.jsx # Yield metric cards
│   │   │   ├── LLMInsights.jsx     # AI-generated crop insights
│   │   │   ├── ChatBot.jsx         # Floating help chatbot
│   │   │   ├── ReportsPanel.jsx    # Reports page
│   │   │   ├── CropInsights.jsx    # Crop insights component
│   │   │   ├── SegmentationView.jsx# Segmentation visualisation
│   │   │   ├── NotificationDropdown.jsx
│   │   │   ├── ProfileDropdown.jsx
│   │   │   └── SettingsModal.jsx   # Settings (dark mode toggle)
│   │   └── utils/
│   │       └── downloadHelpers.js  # Download/export utilities
│   ├── tailwind.config.js
│   └── package.json
│
├── database/                   # 🗄 Database (PostgreSQL + PostGIS)
│   ├── database.py             #   SQLAlchemy engine, session factory, init_db()
│   └── models.py               #   ORM models (CropPrediction table)
│
├── analytics/                  # 📊 Analytics scripts
│   ├── ndvi.py                 #   NDVI computation
│   └── crop_health_report.py   #   Crop health report generation
│
├── outputs/                    # 📦 Model weights & runtime outputs
│   ├── best_model.pth          #   Best trained model checkpoint
│   ├── uploads/                #   Uploaded images
│   └── predictions/            #   Predicted masks
│
├── logs/                       # 📝 Log files
│   ├── training.log
│   ├── training_live.log
│   └── server.log
│
├── SEN-2 LULC/                 # 🛰 Sentinel-2 dataset
│   ├── train_images/
│   ├── train_masks/
│   ├── val_images/
│   ├── val_masks/
│   ├── test_images/
│   └── test_masks/
│
├── evaluation_report/          # Evaluation outputs
├── test_results/               # Test prediction outputs
├── .env                        # Environment variables (not tracked by git)
├── .gitignore
└── README.md
```

---

## 🔧 Installation

### Prerequisites

* Python 3.8+
* Node.js 18+ & npm
* CUDA-capable GPU (recommended)
* PostgreSQL 16 + PostGIS 3.4 (optional — DB not yet connected)

### Backend Setup

```bash
cd crop_llm_full

# Create virtual environment (optional)
python -m venv venv && source venv/bin/activate

# Install PyTorch with CUDA
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Install dependencies
pip install -r backend/requirements.txt

# Verify GPU
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

### Frontend Setup

```bash
cd crop_llm_full/frontend

# Install Node dependencies
npm install

# Build production bundle
npm run build
```

### Database Setup (optional)

```bash
# Create PostgreSQL database & user
sudo -u postgres psql -c "CREATE USER your_username WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "CREATE DATABASE your_database_name OWNER your_username;"
sudo -u postgres psql -d your_database_name -c "CREATE EXTENSION IF NOT EXISTS postgis;"
```

Create a `.env` file in the project root (see `.env.example` for the required variables). **Never commit real credentials to git.**

---

## 🚀 Usage

### Start the Dashboard (Backend + Frontend)

```bash
cd ~/crop_llm_full && python backend/app.py
```

Open **http://localhost:5000/dashboard** in your browser.

### Frontend Dev Server (hot-reload, development only)

```bash
cd ~/crop_llm_full/frontend && npm start
```

Access at **http://localhost:3000** (API calls proxy to port 5000).

### Rebuild Frontend (after React changes)

```bash
cd ~/crop_llm_full/frontend && npm run build
```

### Train the Model

```bash
python backend/train.py \
    --data_root "SEN-2 LULC" \
    --batch_size 16 \
    --epochs 100 \
    --learning_rate 0.0001 \
    --model_type unet \
    --loss_type combined \
    --use_amp
```

### Test the Model

```bash
python backend/test.py \
    --data_root "SEN-2 LULC" \
    --model_path outputs/best_model.pth \
    --batch_size 8 \
    --visualize
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check — model status & device |
| `GET` | `/classes` | Land-cover class names & colours |
| `POST` | `/predict` | Upload image → segmentation mask + insights |
| `GET` | `/predict/demo` | Demo prediction with sample data |
| `GET` | `/predictions` | List all stored predictions |
| `POST` | `/llm-insight/{id}` | Generate AI insight for a prediction |
| `GET` | `/docs` | Swagger UI (auto-generated) |
| `GET` | `/redoc` | ReDoc API documentation |
| `GET` | `/{path}` | Serve React frontend (catch-all) |

---

## 🖥 Frontend Pages

| Page | Sidebar Icon | Description |
|------|-------------|-------------|
| **Dashboard** | Home | Overview with key metrics |
| **Upload Image** | Upload | Upload GeoTIFF or load demo data |
| **Crop Map** | Map | Segmented crop map with class legend |
| **NDVI Analysis** | LineChart | NDVI value, colour scale, classification |
| **Crop Statistics** | BarChart | Class distribution pie/bar charts |
| **Yield Estimation** | Wheat | 4 metric cards (yield, area, per-ha, confidence) |
| **LLM Insights** | Sparkles | AI-generated crop analysis & recommendations |
| **Reports** | FileText | Exportable reports |
| **Help & Support** | HelpCircle | Documentation & support |
| **Chatbot** | Floating | Rule-based AI Interface Assistant (bottom-right) |

### Dark Mode

Toggle via **Settings** (gear icon in header). Preference saved to `localStorage`.

---

## 🏗 Model Architecture

### U-Net (17.2 M parameters)

```
Input (3, 256, 256)
       │
   DoubleConv (64)  ─────────────────────┐
       │                                  │
   Encoder1 (128)  ──────────────────┐   │
       │                              │   │
   Encoder2 (256)  ─────────────┐    │   │
       │                         │    │   │
   Encoder3 (512)  ────────┐    │    │   │
       │                    │    │    │   │
   Bottleneck (1024)        │    │    │   │
       │                    │    │    │   │
   Decoder1 (512)  ←────────┘    │    │   │
       │                         │    │   │
   Decoder2 (256)  ←─────────────┘    │   │
       │                              │   │
   Decoder3 (128)  ←──────────────────┘   │
       │                                  │
   Decoder4 (64)   ←──────────────────────┘
       │
   OutConv (8 classes)
       │
Output (8, 256, 256)
```

### Land-Cover Classes

| ID | Class | Colour |
|----|-------|--------|
| 0 | Water | 🔵 Blue |
| 1 | Trees | 🟢 Dark Green |
| 2 | Grass | 🟩 Light Green |
| 3 | Flooded Vegetation | 🟣 Teal |
| 4 | Crops | 🟡 Yellow |
| 5 | Scrub / Shrub | 🟠 Orange |
| 6 | Built Area | 🔴 Red |
| 7 | Bare Ground | 🟤 Brown |

---

## ⚡ GPU Optimisations

| Optimisation | Code | Benefit |
|-------------|------|---------|
| cuDNN Benchmark | `torch.backends.cudnn.benchmark = True` | Auto-selects fastest conv algorithm |
| Mixed Precision | `torch.cuda.amp.autocast()` | ~2× faster with FP16 |
| Pin Memory | `DataLoader(pin_memory=True)` | Faster CPU → GPU transfer |
| Non-blocking | `.to(device, non_blocking=True)` | Overlaps transfer & compute |
| Efficient Grad Zero | `zero_grad(set_to_none=True)` | Lower memory usage |

---

## 🗄 Database

**Status:** Schema defined, connection deferred.

* **Engine:** PostgreSQL 16 + PostGIS 3.4
* **ORM:** SQLAlchemy + GeoAlchemy2
* **Table:** `crop_predictions` — stores image name, crop type, NDVI, confidence, class distribution, geometry, insight text
* **Current behaviour:** Predictions stored in-memory (`_prediction_store` dict in `app.py`)

Files: `database/database.py` (engine + session), `database/models.py` (ORM model).



## ⚙ Configuration

### Training Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--data_root` | `SEN-2 LULC` | Dataset root directory |
| `--batch_size` | 8 | Batch size |
| `--epochs` | 50 | Number of epochs |
| `--learning_rate` | 1e-4 | Initial learning rate |
| `--model_type` | unet | `unet` or `unet_small` |
| `--loss_type` | combined | `ce` or `combined` (Dice + CE) |
| `--use_amp` | True | Mixed precision training |
| `--scheduler` | plateau | `plateau`, `cosine`, or `none` |
| `--output_dir` | outputs | Output directory |

### Environment Variables (`.env`)

Create a `.env` file in the project root with the following keys:

| Variable | Description |
|----------|-------------|
| `DB_HOST` | PostgreSQL host |
| `DB_PORT` | PostgreSQL port |
| `DB_NAME` | Database name |
| `DB_USER` | Database user |
| `DB_PASSWORD` | Database password |

> **Note:** The `.env` file is listed in `.gitignore` and is never pushed to the repository.

---

## 📈 Results

**Training outputs** → `outputs/`
* `best_model.pth` — Best checkpoint (65.85 MB)
* `training_history.png` — Loss & metric curves

**Test results** → `test_results/`
* `test_metrics.txt` — IoU & Dice scores per class
* `visualizations/` — Input / GT / Prediction comparisons

**Evaluation** → `evaluation_report/`
* Detailed per-class metrics and confusion matrix

---

## 📄 License

This project is for educational and research purposes.

---

**Author:** Crop Analytics Project  
**Date:** 2026  
**Stack:** FastAPI · React · PyTorch · PostgreSQL · Tailwind CSS
