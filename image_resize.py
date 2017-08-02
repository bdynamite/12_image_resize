import argparse
import os

from PIL import Image


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', required=True, help='path to image', type=str)
    parser.add_argument('-w', '--width', help='result width', type=int)
    parser.add_argument('-H', '--height', help='result height', type=int)
    parser.add_argument('-s', '--scale', help='resize coefficient', type=float)
    parser.add_argument('-o', '--output', help='output directory', type=str)
    return parser.parse_args()


def get_img(path):
    return Image.open(path)


def get_resize_method(params):
    if params.scale and (params.height or params.width):
        raise_exception(ValueError, 'Either scale or width/height must be specified!')
    elif params.scale:
        return resize_by_scale
    elif params.height and params.width:
        return resize_by_height_and_width
    elif params.height:
        return resize_by_height
    elif params.width:
        return resize_by_width
    else:
        raise_exception(ValueError, 'Scale or width/height must be specified!')


def raise_exception(exception, text):
    raise exception(text)


def print_msg(msg):
    print(msg)


def resize_by_scale(img, params):
    return img.resize([int(x * params.scale) for x in img.size])


def resize_by_height_and_width(img, params):
    if img.size[0] / img.size[1] != params.width / params.height:
        print_msg('the proportions of the picture will be changed!')
    return img.resize((params.width, params.height))


def resize_by_height(img, params):
    coef = params.height / img.size[1]
    return img.resize((int(img.size[0] * coef), params.height))


def resize_by_width(img, params):
    coef = params.width / img.size[0]
    return img.resize((params.width, int(img.size[1] * coef)))


def save_img(img, params):
    if params.output:
        dir = params.output
    else:
        dir = os.path.dirname(params.path)
    prev_img_name = os.path.split(params.path)[1]
    image_name = '{}__{}.{}'.format(prev_img_name.split('.')[0],
                                    'x'.join(list(map(str, img.size))),
                                    prev_img_name.split('.')[1])
    image_path = os.path.join(dir, image_name)
    img.save(image_path)
    print_msg('\n'.join(['new image successfully saved at', image_path]))

if __name__ == '__main__':
    params = get_args()
    resize_method = get_resize_method(params)
    img = get_img(params.path)
    new_img = resize_method(img, params)
    save_img(new_img, params)
