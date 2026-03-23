import json
from pathlib import Path

import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator


IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 12
SEED = 42
DATASET_ROOT = Path("dataset")
MODEL_DIR = Path("model")
MODEL_PATH = MODEL_DIR / "coconut_disease_model.h5"
CLASS_MAP_PATH = MODEL_DIR / "class_map.json"
PLOT_PATH = MODEL_DIR / "training_plot.png"

CLASS_NAMES = [
    "WCLWD_Yellowing",
    "WCLWD_Flaccidity",
    "WCLWD_DryingofLeaflets",
    "Healthy_Leaves",
    "CCI_Leaflets",
    "CCI_Caterpillars",
]


def resolve_dataset_dirs() -> tuple[Path, Path | None, bool]:
    """
    Returns:
        train_dir: directory containing training class folders
        val_dir: directory containing validation class folders (optional)
        use_split: whether to use validation_split from one directory
    """
    train_candidate = DATASET_ROOT / "train"
    val_candidate = DATASET_ROOT / "val"

    if train_candidate.exists() and train_candidate.is_dir():
        val_dir = val_candidate if val_candidate.exists() and val_candidate.is_dir() else None
        return train_candidate, val_dir, val_dir is None

    return DATASET_ROOT, None, True


def build_model(num_classes: int) -> tf.keras.Model:
    model = Sequential(
        [
            Conv2D(32, (3, 3), activation="relu", input_shape=(224, 224, 3)),
            MaxPooling2D(pool_size=(2, 2)),
            Conv2D(64, (3, 3), activation="relu"),
            MaxPooling2D(pool_size=(2, 2)),
            Conv2D(128, (3, 3), activation="relu"),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.3),
            Flatten(),
            Dense(256, activation="relu"),
            Dropout(0.4),
            Dense(num_classes, activation="softmax"),
        ]
    )

    model.compile(
        loss="categorical_crossentropy",
        optimizer=Adam(learning_rate=1e-4),
        metrics=["accuracy"],
    )
    return model


def make_generators() -> tuple[tf.keras.preprocessing.image.DirectoryIterator, tf.keras.preprocessing.image.DirectoryIterator]:
    train_dir, val_dir, use_split = resolve_dataset_dirs()

    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=25,
        width_shift_range=0.15,
        height_shift_range=0.15,
        shear_range=0.15,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode="nearest",
        validation_split=0.2 if use_split else 0.0,
    )

    if use_split:
        train_gen = train_datagen.flow_from_directory(
            str(train_dir),
            target_size=IMAGE_SIZE,
            batch_size=BATCH_SIZE,
            classes=CLASS_NAMES,
            class_mode="categorical",
            subset="training",
            shuffle=True,
            seed=SEED,
        )

        val_gen = train_datagen.flow_from_directory(
            str(train_dir),
            target_size=IMAGE_SIZE,
            batch_size=BATCH_SIZE,
            classes=CLASS_NAMES,
            class_mode="categorical",
            subset="validation",
            shuffle=False,
            seed=SEED,
        )
    else:
        val_datagen = ImageDataGenerator(rescale=1.0 / 255)

        train_gen = train_datagen.flow_from_directory(
            str(train_dir),
            target_size=IMAGE_SIZE,
            batch_size=BATCH_SIZE,
            classes=CLASS_NAMES,
            class_mode="categorical",
            shuffle=True,
            seed=SEED,
        )

        val_gen = val_datagen.flow_from_directory(
            str(val_dir),
            target_size=IMAGE_SIZE,
            batch_size=BATCH_SIZE,
            classes=CLASS_NAMES,
            class_mode="categorical",
            shuffle=False,
            seed=SEED,
        )

    return train_gen, val_gen


def save_training_plot(history: tf.keras.callbacks.History) -> None:
    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.plot(history.history["accuracy"], label="Train Accuracy")
    plt.plot(history.history["val_accuracy"], label="Val Accuracy")
    plt.title("Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history.history["loss"], label="Train Loss")
    plt.plot(history.history["val_loss"], label="Val Loss")
    plt.title("Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()

    plt.tight_layout()
    plt.savefig(PLOT_PATH, dpi=150)
    plt.close()


def main() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    train_gen, val_gen = make_generators()

    model = build_model(num_classes=len(CLASS_NAMES))

    callbacks = [
        EarlyStopping(monitor="val_loss", patience=3, restore_best_weights=True),
        ModelCheckpoint(filepath=str(MODEL_PATH), monitor="val_accuracy", save_best_only=True),
    ]

    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=EPOCHS,
        callbacks=callbacks,
    )

    # Save final model explicitly as requested.
    model.save(MODEL_PATH)

    with CLASS_MAP_PATH.open("w", encoding="utf-8") as f:
        json.dump({"classes": CLASS_NAMES, "class_indices": train_gen.class_indices}, f, indent=2)

    save_training_plot(history)

    print(f"Model saved to: {MODEL_PATH}")
    print(f"Class map saved to: {CLASS_MAP_PATH}")
    print(f"Training plot saved to: {PLOT_PATH}")


if __name__ == "__main__":
    main()
