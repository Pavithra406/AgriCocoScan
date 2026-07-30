<div align="center">

<!-- Animated Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=2d6a4f,40916c,52b788&height=200&section=header&text=AgriCocoScan&fontSize=60&fontColor=ffffff&fontAlignY=38&desc=AI-Powered%20Coconut%20Disease%20Detection&descAlignY=60&descColor=d8f3dc&animation=fadeIn" width="100%"/>

<!-- Badges Row -->
<p>
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/TensorFlow-2.x-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/Deep%20Learning-CNN-blueviolet?style=for-the-badge&logo=keras&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
</p>

<p>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square"/>
  <img src="https://img.shields.io/badge/PRs-Welcome-blue?style=flat-square"/>
  <img src="https://img.shields.io/github/stars/Pavithra406/AgriCocoScan?style=flat-square&color=yellow"/>
  <img src="https://img.shields.io/github/forks/Pavithra406/AgriCocoScan?style=flat-square&color=orange"/>
</p>

<br/>

> 🌴 **Empowering farmers with AI** — detect coconut leaf diseases early, get recommendations instantly.

</div>

---

## 📖 Table of Contents

<div align="center">

| Section | Link |
|---|---|
| 🌟 Overview | [What is AgriCocoScan?](#-overview) |
| ✨ Features | [Key Capabilities](#-key-features) |
| 🦠 Diseases | [What it Detects](#-diseases-detected) |
| 🏗️ Architecture | [System Design](#-architecture) |
| ⚙️ Tech Stack | [Tools & Libraries](#-tech-stack) |
| 📂 Structure | [Project Layout](#-project-structure) |
| 🚀 Setup | [How to Run](#-getting-started) |
| 📊 Dataset | [Data Info](#-dataset) |
| 🔮 Roadmap | [Future Plans](#-future-improvements) |
| 👩‍💻 Author | [About Me](#-author) |

</div>

---

## 🌟 Overview

<table>
<tr>
<td width="60%">

Coconut trees are tall — and diseases often go unnoticed until they've already spread. **AgriCocoScan** bridges that gap using AI.

Upload a photo of a coconut leaf and the system instantly:
- 🔍 **Identifies** the disease using a trained CNN model
- 📊 **Shows** confidence scores for the prediction
- 💊 **Recommends** treatment for the detected condition

Built for farmers, researchers, and agricultural professionals who need fast, reliable plant health diagnostics — no expertise required.

</td>
<td width="40%" align="center">

```
🌱 Upload Leaf Image
        ↓
🧠 CNN Analyzes Image
        ↓
🔬 Disease Predicted
        ↓
💊 Recommendation Shown
        ↓
✅ Farmer Takes Action
```

</td>
</tr>
</table>

---

## ✨ Key Features

<div align="center">

| Feature | Description |
|---|---|
| 🌿 **Disease Detection** | CNN model trained on coconut leaf images |
| 📷 **Image Upload** | Simple drag-and-drop or file upload UI |
| 📊 **Confidence Score** | Prediction reliability shown as a percentage |
| 💊 **Treatment Guide** | Actionable recommendations per disease |
| 🌐 **Web Interface** | Clean, responsive UI accessible from any browser |
| ⚡ **Fast Inference** | Real-time prediction with low latency |

</div>

---

## 🦠 Diseases Detected

The model classifies coconut leaf images into **6 categories**:

<div align="center">

| # | Condition | Type | Description |
|---|---|---|---|
| 1 | 🟢 **Healthy Leaves** | Normal | No signs of disease |
| 2 | 🟡 **WCLWD – Yellowing** | Disease | Wilt caused by phytoplasma |
| 3 | 🟠 **WCLWD – Flaccidity** | Disease | Loss of leaf firmness |
| 4 | 🔴 **WCLWD – Drying of Leaflets** | Disease | Advanced wilt stage |
| 5 | 🟣 **CCI – Leaflets** | Pest | Coconut caterpillar infestation |
| 6 | 🔵 **CCI – Caterpillars** | Pest | Visible caterpillar damage |

</div>

> **WCLWD** = Wilt & Crown Leaf Wilt Disease &nbsp;|&nbsp; **CCI** = Coconut Caterpillar Infestation

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                    AgriCocoScan                     │
│                                                     │
│   👤 User                                           │
│    │                                                │
│    ▼                                                │
│  ┌──────────────────────────────────┐              │
│  │       Frontend (HTML/CSS/JS)     │              │
│  │  • Upload image                  │              │
│  │  • Display result & score        │              │
│  └──────────────┬───────────────────┘              │
│                 │  HTTP POST (image)                │
│                 ▼                                   │
│  ┌──────────────────────────────────┐              │
│  │        Flask Backend API         │              │
│  │  • Receive & preprocess image    │              │
│  │  • Load trained CNN model        │              │
│  └──────────────┬───────────────────┘              │
│                 │                                   │
│                 ▼                                   │
│  ┌──────────────────────────────────┐              │
│  │   Deep Learning Model (CNN)      │              │
│  │  • TensorFlow / Keras            │              │
│  │  • Image classification          │              │
│  └──────────────┬───────────────────┘              │
│                 │                                   │
│                 ▼                                   │
│  ┌──────────────────────────────────┐              │
│  │     Prediction + Recommendation  │              │
│  │  • Disease label                 │              │
│  │  • Confidence %                  │              │
│  │  • Treatment advice              │              │
│  └──────────────────────────────────┘              │
└─────────────────────────────────────────────────────┘
```

---

## ⚙️ Tech Stack

<details>
<summary><b>🧠 Machine Learning</b> (click to expand)</summary>

<br/>

| Tool | Purpose |
|---|---|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | Core programming language |
| ![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat&logo=tensorflow&logoColor=white) | Deep learning framework |
| ![Keras](https://img.shields.io/badge/Keras-D00000?style=flat&logo=keras&logoColor=white) | High-level neural network API |
| ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white) | Image preprocessing |
| ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white) | Numerical computation |
| ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat) | Visualization and plotting |

</details>

<details>
<summary><b>🌐 Backend</b> (click to expand)</summary>

<br/>

| Tool | Purpose |
|---|---|
| ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) | REST API & web server |

</details>

<details>
<summary><b>🎨 Frontend</b> (click to expand)</summary>

<br/>

| Tool | Purpose |
|---|---|
| ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) | Page structure |
| ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white) | Styling & layout |
| ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) | Interactivity & API calls |

</details>

<details>
<summary><b>🔧 Dev Tools</b> (click to expand)</summary>

<br/>

| Tool | Purpose |
|---|---|
| ![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white) | Version control |
| ![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white) | Code hosting |

</details>

---

## 📂 Project Structure

```
AgriCocoScan/
│
├── 📁 backend/
│   └── app.py               ← Flask API server
│
├── 📁 frontend/
│   ├── 📁 templates/
│   │   ├── index.html        ← Main upload page
│   │   ├── login.html        ← Login screen
│   │   ├── signup.html       ← Registration screen
│   │   └── auth.html         ← Auth handler
│   │
│   └── 📁 static/
│       ├── style.css         ← Stylesheet
│       └── script.js         ← Frontend logic
│
├── train_model.py            ← CNN training script
├── predict.py                ← Standalone prediction script
├── requirements.txt          ← Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have **Python 3.8+** installed.

```bash
python --version
```

---

### Step-by-Step Setup

**1. Clone the repository**
```bash
git clone https://github.com/Pavithra406/AgriCocoScan.git
cd AgriCocoScan
```

**2. Create a virtual environment** *(recommended)*
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Train the model**
```bash
python train_model.py
```
> ⏳ This may take a few minutes depending on your hardware.

**5. Run the application**
```bash
python backend/app.py
```

**6. Open in your browser**
```
http://localhost:5000
```

---

## 📊 Dataset

<details>
<summary><b>Dataset Details</b> (click to expand)</summary>

<br/>

The training dataset consists of labeled coconut leaf images across **6 disease/health categories**.

**Image sources include:**
- 🌾 Agricultural research institutions
- 🌐 Public plant disease image databases
- 📸 Web-collected and manually labeled images

> ⚠️ **Note:** The dataset is not included in this repository due to file size constraints. You'll need to source or prepare your own dataset before training.

**Recommended dataset structure:**
```
dataset/
├── Healthy/
├── WCLWD_Yellowing/
├── WCLWD_Flaccidity/
├── WCLWD_Drying/
├── CCI_Leaflets/
└── CCI_Caterpillars/
```

</details>

---

## 🔮 Future Improvements

<div align="center">

| Priority | Feature |
|---|---|
| 🔴 High | 📱 Mobile app for farmers (Android/iOS) |
| 🟡 Medium | 🌴 Support for fruit and stem disease detection |
| 🟡 Medium | 📡 Drone-based aerial plant monitoring |
| 🟢 Low | 📊 Real-time disease monitoring dashboard |
| 🟢 Low | 🌍 Multi-language support for rural accessibility |

</div>

---

## 👩‍💻 Author

<div align="center">

<img src="https://github.com/Pavithra406.png" width="100" style="border-radius: 50%"/>

### **Pavithra Thangadurai**
*B.Tech – Information Technology*

[![GitHub](https://img.shields.io/badge/GitHub-Pavithra406-181717?style=for-the-badge&logo=github)](https://github.com/Pavithra406)

</div>

---

## ⭐ Acknowledgment

<div align="center">

This project was developed as part of an **academic initiative** to explore the application of Artificial Intelligence in agriculture — enabling early disease detection and supporting smart farming practices.

*If this project helped you, consider giving it a ⭐ star on GitHub!*

</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=2d6a4f,40916c,52b788&height=100&section=footer" width="100%"/>

**Made with 💚 for smarter, healthier agriculture**

</div>
