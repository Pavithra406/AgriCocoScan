# 🌴 AgriCocoScan – AI-Based Coconut Disease Detection System

AgriCocoScan is an AI-powered web application that detects diseases in coconut plants using deep learning and computer vision.
The system analyzes images of coconut leaves and predicts the disease type, helping farmers identify plant health issues early and apply proper treatments.

---

## 📌 Project Overview

Coconut trees are tall and diseases often go unnoticed until they spread widely.
AgriCocoScan solves this problem by using a Convolutional Neural Network (CNN) model to detect diseases from leaf images.

Users can upload a coconut leaf image through the web interface, and the system predicts the disease along with possible recommendations.

---

## 🎯 Key Features

* 🌿 Coconut leaf disease detection using deep learning
* 📷 Image upload interface for prediction
* 🧠 CNN-based image classification model
* 📊 Confidence score for predictions
* 💊 Treatment recommendations for detected diseases
* 🌐 Simple and user-friendly web interface

---

## 🧠 Diseases Detected

The model is trained to detect the following coconut leaf conditions:

* Healthy Leaves
* WCLWD Yellowing
* WCLWD Flaccidity
* WCLWD Drying of Leaflets
* CCI Leaflets
* CCI Caterpillars

---

## 🏗️ Project Architecture

User Upload Image
↓
Frontend (HTML / CSS / JavaScript)
↓
Flask Backend API
↓
Deep Learning Model (CNN)
↓
Disease Prediction
↓
Display Result + Recommendation

---

## ⚙️ Tech Stack

### Machine Learning

* Python
* TensorFlow / Keras
* OpenCV
* NumPy
* Matplotlib

### Backend

* Flask

### Frontend

* HTML
* CSS
* JavaScript

### Version Control

* Git
* GitHub

---

## 📂 Project Structure

```
AgriCocoScan
│
├── backend
│   └── app.py
│
├── frontend
│   ├── templates
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   └── auth.html
│   │
│   └── static
│       ├── style.css
│       └── script.js
│
├── train_model.py
├── predict.py
├── requirements.txt
└── README.md
```

---

## 📊 Dataset

The dataset consists of labeled coconut leaf images representing different disease categories.

Images were collected from:

* Agricultural research sources
* Public image datasets
* Web resources

Note: The dataset is not included in this repository due to size limitations.

---

## 🚀 How to Run the Project

### 1️⃣ Clone the repository

```
git clone https://github.com/Pavithra406/AgriCocoScan.git
```

### 2️⃣ Navigate to the project folder

```
cd AgriCocoScan
```

### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Train the model

```
python train_model.py
```

### 5️⃣ Run the application

```
python backend/app.py
```

### 6️⃣ Open in browser

```
http://localhost:5000
```

---

## 📸 Future Improvements

* Support for coconut fruit and stem disease detection
* Drone-based plant monitoring
* Mobile application for farmers
* Real-time disease monitoring dashboard

---

## 👩‍💻 Author

**Pavithra Thangadurai**
B.Tech Information Technology

GitHub:
https://github.com/Pavithra406

---

## ⭐ Acknowledgment

This project was developed as part of an academic initiative to explore the application of Artificial Intelligence in agriculture for early disease detection and smart farming.
