from typing import List
from image_utils import read_as_numpy_array, write_as_image
from models.tile_prediction import load_model as load_tile_prediction_model, classify_subtiles, pick_tiles
from models.foliage_recognition import load_model as load_recognizer_model
from preprocessing import pad_image_to_tile_multiple, make_tiles
import numpy as np


class ImageRecognitionPipeline:
    _sub_tile_selector = load_tile_prediction_model('models/subtile_selector')
    _foliage_recognizer = load_recognizer_model('models/foliage_recognizer')

    TILE_DIMS = [32, 32]
    SUBTILE_DIMS = [4, 4]
    RECOGNIZER_THRESHOLD = 0.5

    UNINTERESTING_TILE_CLASS = 0
    FOLIAGE_TILE_CLASS = 1
    CAMOUFLAGE_TILE_CLASS = 2

    def generate_tile_selection_mask(self, padded_image):
        # subtile, number of subtile rows, cols
        subtiles, st_rows, st_cols = make_tiles(padded_image, self.SUBTILE_DIMS)

        pred = classify_subtiles(subtiles, self._sub_tile_selector)

        t, h, w = pick_tiles(pred, self.TILE_DIMS, (st_cols, st_rows), self.SUBTILE_DIMS, 0.5)
        selected_tiles_mask = np.nonzero(t.numpy())
        return selected_tiles_mask

    def recognize(self, raw_images: List[bytes]):
        image_matrices = list(map(read_as_numpy_array, raw_images))
        spectral_cube = np.stack(image_matrices, axis=-1) / 255
        padded_cube = pad_image_to_tile_multiple(spectral_cube, self.TILE_DIMS)

        # tiles that contains foliage or camouflage
        interesting_tiles_indexes = self.generate_tile_selection_mask(padded_cube)
        tiles, t_rows, t_cols = make_tiles(padded_cube, self.TILE_DIMS)
        interesting_tiles = np.squeeze(np.take(tiles, interesting_tiles_indexes, axis=0))
        recognition_result = self._foliage_recognizer.predict(interesting_tiles) > self.RECOGNIZER_THRESHOLD

        result = np.zeros(t_rows * t_cols) - 1
        np.put(result, interesting_tiles_indexes, recognition_result)
        result += 1

        # 0 - uninteresting tile
        # 1 - foliage
        # 2 - camouflage
        result = result.reshape(t_cols, t_rows).T

        return result

    def to_json(self, result):
        res = {"tile_size": self.TILE_DIMS, "tiles": []}

        interesting_tiles = result.nonzero()
        for tile in zip(*interesting_tiles):
            [y, x] = tile
            res["tiles"].append({
                "x": int(x),
                "y": int(y),
                "val": result[y, x]
            })

        return res

    def to_image(self, result):
        result_img = np.uint8(np.kron(result / 2.0 * 255, np.ones(self.TILE_DIMS)))
        return write_as_image(result_img)
