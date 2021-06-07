from catboost import CatBoostClassifier
import tensorflow as tf
import numpy as np
from preprocessing import pad_image_to_tile_multiple, split_image


def load_model(path):
    """Loads model from catboost binary format"""
    return CatBoostClassifier().load_model(path)


def classify_subtiles(subtiles, selector_model):
    """Classifies subtiles with given model"""
    tiles_np = tf.reshape(subtiles, (subtiles.shape[0], -1)).numpy()
    return selector_model.predict(tiles_np)


def pick_tiles(pred, tile_shape, subtiles_nums, subtile_shape, threshold=0.8):
    scaled_prediction = np.expand_dims(np.kron(pred.reshape(subtiles_nums).T, np.ones(subtile_shape)), axis=-1)
    padded_scaled_prediction = pad_image_to_tile_multiple(scaled_prediction, tile_shape)

    pixels_count = tile_shape[0] * tile_shape[1]
    prediction_tiles = np.squeeze(split_image(padded_scaled_prediction, tile_shape))
    tiles_rank = tf.math.reduce_sum(tf.math.reduce_sum(prediction_tiles, 1), 1) / pixels_count

    tiles_mask = tiles_rank > threshold

    padded_w, padded_h, _ = padded_scaled_prediction.shape
    padded_w //= tile_shape[0]
    padded_h //= tile_shape[1]

    return tiles_mask, padded_h, padded_w
