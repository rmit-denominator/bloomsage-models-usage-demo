import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.engine.training import Model
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
from fastapi import UploadFile


from machine_learning.util import TARGET_IMG_SIZE
from machine_learning.util import CLASS_LABELS
import machine_learning.util.input_processing as input_manip


def classify(
    image: UploadFile,
    classifier_path: str,
    verbose: bool = False,
    return_original: bool = True
) -> tuple:
    """
    Uses a trained machine learning model to classify an image loaded from disk.

    :param image_path: Path to the image to be classified.
    :param classifier_path: Path to the classifier model to be used.
    :param verbose: Verbose output.
    :param return_original: Whether to return the original image or the processed image.
    :return: The original/processed image (PIL.image) and its classification (str).
    """

    im_original = Image.open(image.file)
    im_processed = input_manip.remove_transparency(im_original)
    im_processed = input_manip.resize_crop(im_processed, TARGET_IMG_SIZE, TARGET_IMG_SIZE)
    im_processed = input_manip.normalize_pixels(im_processed)
    im_processed = tf.expand_dims(im_processed, axis=0)

    model: Model = tf.keras.models.load_model(classifier_path)
    pred = model.predict(im_processed, verbose=1 if verbose else 0)

    pred_class_idx = tf.argmax(pred, axis=1).numpy()[0]
    pred_class_label = CLASS_LABELS[pred_class_idx]

    if return_original:
        return im_original, pred_class_label
    else:
        return im_processed, pred_class_label


def recommend(
        ref_image: UploadFile,
        num_recommendations: int,
        data_path: str,
        clf_path: str,
        fe_path: str,
        clu_path: str,
) -> dict:
    """
    Recommends similar images based on a reference image.

    :param ref_path: Path to the reference image.
    :param num_recommendations: Number of recommended images to return.
    :param data_path: Path to the .csv data file containing recommender database image feature vectors. This file must be generated using the same feature extractor specified in fe_path.
    :param clf_path: Path to the classifier model file.
    :param fe_path: Path to the feature extraction model file.
    :param clu_path: Path to the clustering model file.
    :return: Dictionary containing paths to recommended images as keys and their cosine similarity scores as values.
    """
    if num_recommendations < 1:
        raise ValueError('Number of recommendations cannot be smaller than 1.')

    df_rec = pd.read_csv(data_path)
    fe = tf.keras.models.load_model(fe_path)
    clu = joblib.load(clu_path)
    clu.set_params(n_clusters=int(np.sqrt(len(df_rec) / num_recommendations)))

    ref_processed, ref_class = classify(ref_image, classifier_path=clf_path, return_original=False, verbose=False)
    recommendations = df_rec[df_rec['Class'] == ref_class]

    # Extract reference image feature vector
    ref_processed = np.squeeze(ref_processed)
    ref_feature_vector = fe.predict(
        tf.expand_dims(ref_processed, axis=0),
        verbose=0
    )
    ref_feature_vector = ref_feature_vector.astype(float)
    ref_feature_vector = ref_feature_vector.reshape(1, -1)

    # Cluster reference image
    clu.fit(recommendations.drop(['ImgPath', 'Class'], axis='columns').values)
    ref_cluster = clu.predict(ref_feature_vector)
    ref_cluster_indices = np.where(clu.labels_ == ref_cluster)[0]
    recommendations = recommendations.iloc[ref_cluster_indices]

    # Rank cluster and produce top cosine similarity recommendations
    cosine_similarities = cosine_similarity(
        ref_feature_vector,
        recommendations.drop(['ImgPath', 'Class'], axis='columns')
    )
    sorted_ref_cluster_indices = np.argsort(-cosine_similarities.flatten())
    if num_recommendations > len(sorted_ref_cluster_indices):
        raise ValueError('Number of recommendations too large. Insufficient database size.')
    top_ref_cluster_indices = sorted_ref_cluster_indices[:num_recommendations]
    recommendations = recommendations.iloc[top_ref_cluster_indices]

    # Retrieve paths and cosine similarities
    recommended_paths = recommendations['ImgPath'].tolist()
    cosine_sim_scores = cosine_similarities[0, top_ref_cluster_indices].tolist()

    # Create a dictionary with paths and their cosine similarity scores
    result_dict = { path: score for path, score in zip(recommended_paths, cosine_sim_scores) }

    return result_dict
