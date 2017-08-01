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
    # return parser.parse_args(['-p',  r'C:\Temp\1217597582_00-pink_floyd.jpg', '-s', '0.5'])
    return parser.parse_args()


def get_img(path):
    return Image.open(path)


def get_resize_method(args):
    if args.scale and (args.height or args.width):
        raise ValueError('Either scale or width/height must be specified!')
    elif args.scale:
        return resize_by_scale
    elif args.height and args.width:
        return resize
    elif args.height:
        return resize_by_height
    elif args.width:
        return resize_by_width
    else:
        raise ValueError('Scale or width/height must be specified!')


def resize_by_scale(img, args):
    return img.resize([int(x * args.scale) for x in img.size])


def resize(img, args):
    if img.size[0] / img.size[1] != args.width / args.height:
        print('the proportions of the picture will be changed!')
    return img.resize((args.width, args.height))


def resize_by_height(img, args):
    coef = args.height / img.size[1]
    return img.resize((int(img.size[0] * coef), args.height))


def resize_by_width(img, args):
    coef = args.width / img.size[0]
    return img.resize((args.width, int(img.size[1] * coef)))


def save_img(img, args):
    if args.output:
        dir = args.output
    else:
        dir = os.path.dirname(args.path)
    prev_img_name = os.path.split(args.path)[1]
    image_name = '{}__{}.{}'.format(prev_img_name.split('.')[0],
                                    'x'.join(list(map(str, img.size))),
                                    prev_img_name.split('.')[1])
    image_path = os.path.join(dir, image_name)
    img.save(image_path)
    print('new image successfully saved at')
    print(image_path)

if __name__ == '__main__':
    args = get_args()
    resize_method = get_resize_method(args)
    img = get_img(args.path)
    new_img = resize_method(img, args)
    save_img(new_img, args)
