import tensorflow as tf
import tensorflow.math as tfm


def pad_image_to_tile_multiple(image, tile_size, padding="CONSTANT"):
    """Pads image to make it a multiple of tile size"""
    imagesize = tf.shape(image)[0:2]
    padding_ = tf.cast(tfm.ceil(imagesize / tile_size), tf.int32) * tile_size - imagesize
    return tf.pad(image, [[0, padding_[0]], [0, padding_[1]], [0, 0]], padding)


def split_image(image, tile_size):
    """Cuts image into tiles"""
    image_shape = tf.shape(image)
    tile_rows = tf.reshape(image, [image_shape[0], -1, tile_size[1], image_shape[2]])
    serial_tiles = tf.transpose(tile_rows, [1, 0, 2, 3])
    return tf.reshape(serial_tiles, [-1, tile_size[1], tile_size[0], image_shape[2]])


def make_tiles(padded_img, tile_shape):
    """Makes tiles from image

    Arguments:
    padded_img -- numpy representation of the image in channels last format
    tile_shape -- tuple with tile width and height
    """
    tiles = split_image(padded_img, tile_shape)

    rows, cols, channels_num = padded_img.shape

    return tiles, rows // tile_shape[0], cols // tile_shape[1]


def unsplit_image(tiles, image_shape):
    """Assembles image from tiles"""
    tile_width = tf.shape(tiles)[1]
    serialized_tiles = tf.reshape(tiles, [-1, image_shape[0], tile_width, image_shape[2]])
    rowwise_tiles = tf.transpose(serialized_tiles, [1, 0, 2, 3])
    return tf.reshape(rowwise_tiles, [image_shape[0], image_shape[1], image_shape[2]])
