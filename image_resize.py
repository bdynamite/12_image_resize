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


def get_resize_method(options):
    if options.scale and (options.height or options.width):
        raise_exception(ValueError, 'Either scale or width/height must be specified!')
    elif options.scale:
        return resize_by_scale
    elif options.height and options.width:
        return resize_by_height_and_width
    elif options.height:
        return resize_by_height
    elif options.width:
        return resize_by_width
    else:
        raise_exception(ValueError, 'Scale or width/height must be specified!')


def raise_exception(exception, text):
    raise exception(text)


def resize_by_scale(image, options):
    return image.resize([int(x * options.scale) for x in image.size])


def resize_by_height_and_width(image, options):
    return image.resize((options.width, options.height))


def resize_by_height(image, options):
    coef = options.height / image.size[1]
    return image.resize((int(image.size[0] * coef), options.height))


def resize_by_width(image, options):
    coefficient = options.width / image.size[0]
    return image.resize((options.width, int(image.size[1] * coefficient)))


def get_new_img_path(options):
    if options.output:
        folder = options.output
    else:
        folder = os.path.dirname(options.path)
    prev_img_name = os.path.split(options.path)[1]
    image_name = '{}__{}.{}'.format(prev_img_name.split('.')[0],
                                    'x'.join(list(map(str, img.size))),
                                    prev_img_name.split('.')[1])
    return os.path.join(folder, image_name)

if __name__ == '__main__':
    params = get_args()
    resize_method = get_resize_method(params)
    img = Image.open(params.path)
    new_img = resize_method(img, params)
    if img.size[0] / img.size[1] != new_img.size[0] / new_img.size[1]:
        print('the proportions of the picture will be changed!')
    new_img_path = get_new_img_path(params)
    new_img.save(new_img_path)
    print('\n'.join(['new image successfully saved at', new_img_path]))
