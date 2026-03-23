# AI-Based Coconut Tree Disease Detection and Recommendation System

This project is an end-to-end deep learning web app to detect coconut leaf diseases and recommend treatments.

## Project Structure

```text
coconut-disease-detection/
|-- dataset/
|-- model/
|-- train_model.py
|-- predict.py
|-- backend/
|   `-- app.py
|-- frontend/
|   |-- templates/
|   |   `-- index.html
|   `-- static/
|       |-- style.css
|       `-- script.js
|-- uploads/
|-- requirements.txt
`-- README.md
```

## Supported Classes

- WCLWD_Yellowing
- WCLWD_Flaccidity
- WCLWD_DryingofLeaflets
- Healthy_Leaves
- CCI_Leaflets
- CCI_Caterpillars

## Treatment Recommendations

- `WCLWD_Yellowing`: Apply micronutrient spray and improve soil drainage.
- `WCLWD_Flaccidity`: Apply organic fertilizer and ensure proper irrigation.
- `WCLWD_DryingofLeaflets`: Remove infected leaves and apply fungicide.
- `CCI_Leaflets`: Use appropriate insecticide treatment and monitor spread.
- `CCI_Caterpillars`: Apply biological pest control or neem oil treatment.
- `Healthy_Leaves`: No treatment needed. Maintain regular coconut tree care.

## Setup

1. Create and activate a Python virtual environment.

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Ensure dataset directory exists as one of these formats:

```text
dataset/
  <class_1>/
  <class_2>/
  ...
```

or

```text
dataset/
  train/
    <class_1>/
    ...
  val/
    <class_1>/
    ...
```

If only `dataset/train` exists, `train_model.py` automatically creates validation split from train data.

## Train the Model

```bash
python train_model.py
```

Outputs:
- `model/coconut_disease_model.h5`
- `model/class_map.json`
- `model/training_plot.png`

## Run Inference from CLI

```bash
python predict.py path/to/image.jpg
```

## Run Web App

```bash
python backend/app.py
```

Open browser:
- `http://127.0.0.1:5000`

## API Endpoints

### `POST /upload`
Upload image file using multipart form-data key: `image`.

Sample response:

```json
{
  "message": "File uploaded successfully.",
  "filename": "uuid.jpg",
  "file_path": ".../uploads/uuid.jpg"
}
```

### `POST /predict`
Two options:
1. Send multipart image directly with key `image`.
2. Send JSON body with uploaded filename:

```json
{
  "filename": "uuid.jpg"
}
```

Sample response:

```json
{
  "disease": "WCLWD_Yellowing",
  "confidence": "94.12%",
  "solution": "Apply micronutrient spray and improve soil drainage."
}
```

## Notes

- Input images are resized to `224x224` and normalized to `[0,1]`.
- Training uses data augmentation with `ImageDataGenerator`.
- Max upload size is 10 MB.
- Invalid/non-image files are rejected with proper error messages.
