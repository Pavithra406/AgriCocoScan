from __future__ import annotations

import imghdr
import os
import sqlite3
import sys
import uuid
from functools import wraps
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

# Allow importing predict.py from project root.
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from predict import CoconutDiseasePredictor  # noqa: E402


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "webp"}
UPLOAD_DIR = ROOT_DIR / "uploads"
MODEL_PATH = ROOT_DIR / "model" / "coconut_disease_model.h5"
DB_PATH = ROOT_DIR / "backend" / "users.db"

app = Flask(
    __name__,
    template_folder=str(ROOT_DIR / "frontend" / "templates"),
    static_folder=str(ROOT_DIR / "frontend" / "static"),
)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

predictor: CoconutDiseasePredictor | None = None


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login_page"))
        return view_func(*args, **kwargs)

    return wrapped_view


def is_allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_image_file(file_path: Path) -> bool:
    image_type = imghdr.what(file_path)
    return image_type in {"jpeg", "png", "bmp", "webp"}


def save_upload(file_storage) -> Path:
    original_name = secure_filename(file_storage.filename)
    ext = original_name.rsplit(".", 1)[1].lower()
    saved_name = f"{uuid.uuid4().hex}.{ext}"
    save_path = UPLOAD_DIR / saved_name
    file_storage.save(save_path)

    if not validate_image_file(save_path):
        save_path.unlink(missing_ok=True)
        raise ValueError("Invalid image file. Please upload a valid image.")

    return save_path


def get_predictor() -> CoconutDiseasePredictor:
    global predictor
    if predictor is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError("Model file not found. Please run train_model.py first.")
        predictor = CoconutDiseasePredictor(model_path=MODEL_PATH)
    return predictor


@app.route("/", methods=["GET"])
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login_page"))


@app.route("/login", methods=["GET"])
def login_page():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/signup", methods=["GET"])
def signup_page():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("signup.html")


@app.route("/auth", methods=["GET"])
def auth_page():
    return redirect(url_for("login_page"))


@app.route("/signup", methods=["POST"])
def signup():
    name = (request.form.get("name") or "").strip()
    user_id = (request.form.get("user_id") or "").strip()
    password = request.form.get("password") or ""

    if not name or not user_id or not password:
        return render_template("signup.html", error="Name, ID, and password are required.")

    password_hash = generate_password_hash(password)
    try:
        with get_db_connection() as conn:
            conn.execute(
                "INSERT INTO users (user_id, name, password_hash) VALUES (?, ?, ?)",
                (user_id, name, password_hash),
            )
            conn.commit()
    except sqlite3.IntegrityError:
        return render_template("signup.html", error="That ID is already registered.")

    session["user_id"] = user_id
    session["name"] = name
    return redirect(url_for("index"))


@app.route("/login", methods=["POST"])
def login():
    user_id = (request.form.get("user_id") or "").strip()
    password = request.form.get("password") or ""

    if not user_id or not password:
        return render_template("login.html", error="ID and password are required.")

    with get_db_connection() as conn:
        user = conn.execute(
            "SELECT user_id, name, password_hash FROM users WHERE user_id = ?",
            (user_id,),
        ).fetchone()

    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid ID or password.")

    session["user_id"] = user["user_id"]
    session["name"] = user["name"]
    return redirect(url_for("index"))


@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template("index.html", user_name=session.get("name", "User"))


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login_page"))


@app.route("/upload", methods=["POST"])
@login_required
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided."}), 400

    image_file = request.files["image"]

    if image_file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not is_allowed_file(image_file.filename):
        return jsonify({"error": "Unsupported file type."}), 400

    try:
        saved_path = save_upload(image_file)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Failed to upload file."}), 500

    return jsonify(
        {
            "message": "File uploaded successfully.",
            "filename": saved_path.name,
            "file_path": str(saved_path),
        }
    )


@app.route("/predict", methods=["POST"])
@login_required
def predict_disease():
    try:
        # Option 1: Predict from freshly uploaded file in same request.
        if "image" in request.files and request.files["image"].filename:
            image_file = request.files["image"]
            if not is_allowed_file(image_file.filename):
                return jsonify({"error": "Unsupported file type."}), 400
            image_path = save_upload(image_file)
        else:
            # Option 2: Predict from file already uploaded via /upload.
            payload = request.get_json(silent=True) or {}
            filename = payload.get("filename") or request.form.get("filename")

            if not filename:
                return jsonify({"error": "No image or filename provided."}), 400

            image_path = UPLOAD_DIR / os.path.basename(filename)
            if not image_path.exists():
                return jsonify({"error": "Uploaded file not found."}), 404

        result = get_predictor().predict(image_path)

        return jsonify(
            {
                "disease": result["disease"],
                "confidence": result["confidence_pct"],
                "solution": result["solution"],
            }
        )
    except FileNotFoundError as exc:
        return jsonify({"error": str(exc)}), 503
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Prediction failed. Please try again."}), 500


@app.errorhandler(413)
def too_large(_error):
    return jsonify({"error": "File is too large. Maximum size is 10 MB."}), 413


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
