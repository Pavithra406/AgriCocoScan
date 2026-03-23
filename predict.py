from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from tensorflow.keras.models import load_model


CLASS_NAMES = [
    "WCLWD_Yellowing",
    "WCLWD_Flaccidity",
    "WCLWD_DryingofLeaflets",
    "Healthy_Leaves",
    "CCI_Leaflets",
    "CCI_Caterpillars",
]

TREATMENT_RECOMMENDATIONS = {
    "WCLWD_Yellowing": "Apply micronutrient spray and improve soil drainage.",
    "WCLWD_Flaccidity": "Apply organic fertilizer and ensure proper irrigation.",
    "WCLWD_DryingofLeaflets": "Remove infected leaves and apply fungicide.",
    "CCI_Leaflets": "Use appropriate insecticide treatment and monitor spread.",
    "CCI_Caterpillars": "Apply biological pest control or neem oil treatment.",
    "Healthy_Leaves": "No treatment needed. Maintain regular coconut tree care.",
}

MODEL_PATH = Path("model") / "coconut_disease_model.h5"


class CoconutDiseasePredictor:
    def __init__(self, model_path: Path | str = MODEL_PATH):
        self.model_path = Path(model_path)
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found at: {self.model_path}")
        self.model = load_model(self.model_path)

    @staticmethod
    def preprocess_image(image_path: Path | str) -> np.ndarray:
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError("Unable to read image. Please provide a valid image file.")

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        image = image.astype("float32") / 255.0
        image = np.expand_dims(image, axis=0)
        return image

    def predict(self, image_path: Path | str) -> dict[str, Any]:
        processed = self.preprocess_image(image_path)
        probabilities = self.model.predict(processed, verbose=0)[0]

        predicted_idx = int(np.argmax(probabilities))
        confidence = float(probabilities[predicted_idx])
        disease = CLASS_NAMES[predicted_idx]

        return {
            "disease": disease,
            "confidence": confidence,
            "confidence_pct": f"{confidence * 100:.2f}%",
            "solution": TREATMENT_RECOMMENDATIONS[disease],
        }


def predict_image(image_path: Path | str, model_path: Path | str = MODEL_PATH) -> dict[str, Any]:
    predictor = CoconutDiseasePredictor(model_path=model_path)
    return predictor.predict(image_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Predict coconut leaf disease from an image")
    parser.add_argument("image_path", type=str, help="Path to input image")
    parser.add_argument(
        "--model-path",
        type=str,
        default=str(MODEL_PATH),
        help="Path to trained Keras model",
    )
    args = parser.parse_args()

    result = predict_image(args.image_path, args.model_path)
    print(f"Disease: {result['disease']}")
    print(f"Confidence: {result['confidence_pct']}")
    print(f"Recommendation: {result['solution']}")


if __name__ == "__main__":
    main()
