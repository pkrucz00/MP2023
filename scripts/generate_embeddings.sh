#!/usr/bin/env bash

source venv/bin/activate
DATASETS_DIRS=("data/real_faces_dataset" "data/lfw_dataset" "data/ck_faces_dataset")

# facenet
for DATASET_DIR in "${DATASETS_DIRS[@]}"; do
    python scripts/generate_embeddings.py \
        --dataset_dir "$DATASET_DIR" \
        --out "$DATASET_DIR"_embeddings \
        --model_type "facenet"
done

# insight face models 
for DATASET_DIR in "${DATASETS_DIRS[@]}"; do
    python scripts/generate_embeddings.py \
        --dataset_dir "$DATASET_DIR" \
        --out "$DATASET_DIR"_embeddings \
        --model_type "insightface" \
        --weights "thirdparty/recognition/weights" 
done
