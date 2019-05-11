import os
import json
import cv2
import PIL
import math
import numpy as np
from time import sleep
import matplotlib.pyplot as plt
from skimage.measure import compare_ssim as ssim
from imutils import grab_contours


class ImageDiff:
    def __init__(self, grayscale=True):
        self.images = {}
        self.grayscale = grayscale
        self.color = 'BGR'
        self.loader = False

    def mse(self, imageA, imageB):
        """
        The 'Mean Squared Error' between the two images is the
        sum of the squared difference between the two images
        ```
        return the MSE, the lower the error, the more "similar" images are
        ```
        """
        imageA, imageB = self._get_same_sized(imageA, imageB)
        err = np.sum((imageA.astype("float") - imageB.astype("float"))**2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        return err

    def ssim(self, imageA, imageB, full=False):
        """
        The 'Structural Similarity' between the two images is the perception-based
        index for measuring the similarity between two images.
        ```
        return the SSIM: tuple(score, diff) if full or just score,
        the higher is better
        ```
        """
        imageA, imageB = self._get_same_sized(imageA, imageB)
        S = ssim(imageA, imageB, multichannel=(not self.grayscale), full=full)
        if isinstance(S, tuple):
            sdiff = (S[1] * 255).astype("uint8")
            return S[0], sdiff
        if not isinstance(S, np.float64):
            return S
        return S, None        

    def psnr(self, imageA, imageB):
        """
        The 'Peak Signal-to-Noise Ratio' between the two images is the 20log10(255/sqrt(MSE))
        ```
        return the PSNR in decibels, 30-50 dB - typical for compression
        ```
        """
        mse = self.mse(imageA, imageB)
        if mse:
            return 20 * math.log10(255.0 / math.sqrt(mse))
        return 100

    def _get_same_sized(self, imageA, imageB):
        if len(imageA) != len(imageB):
            print('Images dimensions differ, converting to 2 dim', imageA.shape, '!=', imageB.shape)
            if len(imageA) == 3:
                imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
            if len(imageB) == 3:
                imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
        if imageA.shape[0] != imageB.shape[0] or imageA.shape[1] != imageB.shape[1]:
            h,w = min(imageA.shape[0], imageB.shape[0]), min(imageA.shape[1], imageB.shape[1])
            print(f'Images size are diffeerent: {imageA.shape} != {imageB.shape} | Crop: ({h},{w})')
            imageA = imageA[:h,:w,...].copy()
            imageB = imageB[:h,:w,...].copy()
        return imageA, imageB

    def get_diff(self, imageA, imageB):
        imageA, imageB = self._get_same_sized(imageA, imageB)
        return cv2.subtract(imageA, imageB)

    def get_threshold(self, imageA, imageB, rgb=False):
        _, diff = self.ssim(imageA, imageB, full=True)
        if not self.grayscale:
            t = cv2.inRange(diff, np.array([0, 125, 0]), np.array([255, 200, 255]), diff)
        else:
            t = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        if rgb:
            t = self._rgb(t)
        return t

    def get_contours(self, imageA, imageB):
        t = self.get_threshold(imageA, imageB)
        contours = cv2.findContours(t.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return grab_contours(contours)

    def draw_boxes(self, imageA, imageB):
        for c in self.get_contours(imageA, imageB):
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 1)

    def get_absdiff(self, imageA, imageB):
        imageA, imageB = self._get_same_sized(imageA, imageB)
        return cv2.absdiff(imageA, imageB)

    def is_equal(self, imageA, imageB):
        imageA, imageB = self._get_same_sized(imageA, imageB)
        diff = cv2.subtract(imageA, imageB)
        return not np.any(diff)

    def compare_images(self, imageA, imageB, interactive=False, title='Compare'):
        m = self.mse(imageA, imageB)
        p = self.psnr(imageA, imageB)
        s, sd = self.ssim(imageA, imageB, full=interactive)
        is_equal = self.is_equal(imageA, imageB)
        if is_equal:
            msg = "The images are the same"
        else:
            msg = "The images are different"

        if interactive:
            print(f"Title: {title} MSE: {m:.2f}, SSIM: {s:.6}, msg: {msg}")
            d = self.get_diff(imageA, imageB)
            a = self.get_absdiff(imageA, imageB)
            t = self.get_threshold(imageA, imageB, rgb=(not self.grayscale))
            self.draw_boxes(imageA, imageB)
            c = self.get_concated(imageA, imageB, d, a, sd, t, to_rgb=False)
            self.show_image(c, title=f"{self.color}: in, out, diff, abs, ssim, thresh", wait=True)
            c = self.get_concated(imageA, imageB, d, a, sd, t, to_rgb=True)
            self.show_image(c, title=f"{self.color}: in, out, diff, abs, ssim, thresh", wait=True)
            self.show_cmp_plot(imageA, imageB, m, s, title, msg)

        return m, p, s, msg

    def compare_all(self, interactive=False):
        for name, values in self.images.items():
            images = values.get('images', [])
            if not images:
                continue
            if len(images) == 1:
                print(f'Image {name} has no pair to compare')
            else:
                m, p, s, msg = self.compare_images(images[0], images[1], title=name, interactive=interactive)
                values['MSE'] = m
                values['PSNR'] = p
                values['SSIM'] = s
                values['msg'] = msg

    def get_image(self, path, rgb=False):
        image = cv2.imread(path)
        if rgb:
            return image
        if self.grayscale:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def del_image(self, name):
        d = self.images.pop(name, None)
        if d:
            print(f'Image {name} deleted')
        else:
            print(f'No {name} image found')

    def add_image(self, path, suffix='', name=None):
        if not os.path.exists(path) and (path.endswith('.png') or path.endswith('.jpg')):
            raise FileNotFoundError(f'No {path} image found. Supported ext: [.jpg|.png ]')

        image = self.get_image(path)

        if name is None:
            name = os.path.splitext(os.path.basename(path))[0]
        if suffix:
            name = name.replace(suffix, '')

        self.images[name] = self.images.get(name, {})
        self.images[name]['MSE'] = ""
        self.images[name]['PSNR'] = ""
        self.images[name]['SSIM'] = ""
        self.images[name]['msg'] = ""
        self.images[name]['images'] = self.images[name].get('images', [])
        self.images[name]['images'].append(image)
        return image


    def _get_list_of_images(self, *pathes, number, suffix):
        im_src = []
        for path in pathes:
            if not os.path.exists(path):
                raise FileExistsError(f'No {path} found')

            if os.path.isdir(path):
                for r, _, f in os.walk(path):
                    for i, file in enumerate(sorted(f)):
                        if number and i >= number:
                            break
                        if file.endswith('.png') or file.endswith('.jpg'):
                            name = os.path.splitext(os.path.basename(path))[0]
                            if name.endswith(suffix):
                                src = os.path.join(r, file)
                                im_src.append(src)
                    break
            else:
                im_src.append(path)
        im_src.sort(key=lambda x: os.path.splitext(os.path.basename(x))[0])
        return im_src

    def _loader(self, *pathes, number, batch, suffix):
        if batch % 2 != 0:
            batch += 1
        im_src = self._get_list_of_images(*pathes, number=number, suffix=suffix)
        images = []
        for src in im_src:
            if len(images) >= batch:
                yield images
                self.clean()
                images = []
            im = self.add_image(src, suffix=suffix)
            images.append(im)
        yield images
        self.clean()

    def load_images(self, *pathes, number=0, batch=0, suffix=''):

        if batch:
            return self._loader(*pathes, number=number, batch=batch, suffix=suffix)

        for path in pathes:
            if not os.path.exists(path):
                raise FileExistsError(f'No {path} found')

            if os.path.isdir(path):
                for r, _, f in os.walk(path):
                    for i, file in enumerate(sorted(f)):
                        if number and i >= number:
                            break
                        if file.endswith('.png') or file.endswith('.jpg'):
                            name = os.path.splitext(os.path.basename(path))[0]
                            if name.endswith(suffix):
                                src = os.path.join(r, file)
                                self.add_image(src, suffix=suffix)
                    break
            else:
                self.add_image(path)
        return self.images

    def clean(self, full=False):
        if full:
            self.images = {}
        for k, v in self.images.items():
            v['images'] = []

    def _setup_plt(self, imageA, imageB, m, s, title, msg):
        fig = plt.figure(title)
        plt.suptitle(f"MSE: {m:.2f}, SSIM: {s:.6}", fontsize=15)
        plt.figtext(0.5, 0.3, f"{msg}", ha="center", va="bottom", fontsize=15)
        ax = fig.add_subplot(1, 2, 1)
        ax.set_title('Input', fontsize=15)
        if self.grayscale:
            plt.imshow(imageA, cmap=plt.cm.gray)
        else:
            plt.imshow(imageA)
        plt.axis("off")
        ax = fig.add_subplot(1, 2, 2)
        ax.set_title('Output', fontsize=15)
        if self.grayscale:
            plt.imshow(imageB, cmap=plt.cm.gray)
        else:
            plt.imshow(imageB)
        plt.axis("off")

    def _to_pil(self, cv_image):
        if isinstance(cv_image, np.ndarray):
            return PIL.Image.fromarray(cv_image)
        return cv_image

    def _to_cv(self, pil_image):
        if isinstance(pil_image, np.ndarray):
            return pil_image
        return np.array(pil_image)

    def _rgb(self, *images, globaly=False):
        if len(images) == 1:
            if len(images[0].shape) == 2:
                return cv2.cvtColor(images[0], cv2.COLOR_GRAY2RGB)
            return cv2.cvtColor(images[0], cv2.COLOR_BGR2RGB)
        if globaly:
            self.color = 'RGB' if self.color == 'BGR' else 'BGR'
        colored = []
        for im in images:
            if len(im.shape) == 2:
                im = cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)
            else:
                im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            colored.append(im)
        return colored

    def get_json_stats(self):
        j = {}
        for image, values in self.images.items():
            j[image] = {}
            j[image]['MSE'] = values.get('MSE', '')
            j[image]['PSNR'] = values.get('PSNR', '')
            j[image]['SSIM'] = values.get('SSIM', '')
            j[image]['msg'] = values.get('msg', '')
        return j

    def print_stats(self):
        j = self.get_json_stats()
        print(json.dumps(j, indent=4, sort_keys=True))

    def show_cmp_plot(self, imageA, imageB, m, s, title, msg):
        self._setup_plt(imageA, imageB, m, s, title, msg)
        plt.show()

    def get_splitted(self, image, parts=2, direction='h', to_rgb=True):
        if direction == 'h':
            w = image.shape[1]
            part = w // parts
            offset = part
            images = [image[:, offset*k:offset*k + part, ...] for k in range(parts)]
        elif direction == 'v':
            h = image.shape[0]
            part = h // parts
            offset = part
            images = [image[offset*k:offset*k + part, :, ...] for k in range(parts)]

        if to_rgb:
            images = self._rgb(*images)
        return images

    def get_concated(self, *images, to_rgb=True):
        n = len(images)
        if n < 2:
            return images
        if to_rgb:
            images = self._rgb(*images, globaly=True)
        if n == 2:
            return np.hstack((images))
        if n % 2 != 0:
            n += 1
        concat1 = np.hstack((images[:n // 2]))
        concat2 = np.hstack((images[n // 2:]))
        d = abs(concat1.shape[1] - concat2.shape[1])
        if d > 0:
            if self.grayscale:
                empty = np.zeros((concat2.shape[0], d // 2), np.uint8)
            else:
                empty = np.zeros((concat2.shape[0], d // 2, 3), np.uint8)
            empty[:, :] = 255
            concat2 = np.hstack((empty, concat2, empty))
        return np.vstack((concat1, concat2))

    def show_image(self, image, title="Image", wait=False):
        cv2.imshow(title, image)
        if wait:
            cv2.waitKey(0)

    def save_image(self, image, filename='image.png', rgb=False):
        if rgb:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(filename, image)

    def save_stats(self, filename='stats', save_format='json'):
        filename = os.path.splitext(os.path.basename(filename))[0]
        if save_format == 'json':
            j = self.get_json_stats()
            with open(f'{filename}.json', 'w') as stats:
                json.dump(j, stats, indent=4, sort_keys=True)
        elif save_format == 'csv':
            j = self.get_json_stats()
            with open(f'{filename}.csv', 'w') as stats:
                print('image_name,MSE,PSNR,SSIM,Message', file=stats)
                for image, v in j.items():
                    m, p, s, msg = v.get('MSE', ''), v.get('PSNR', ''), v.get('SSIM', ''), v.get('msg', '')
                    print(f'{image},{m},{p},{s},{msg}', file=stats)
        else:
            print(f'Error: Save format {save_format} not supported')


if __name__ == "__main__":
    imageA = "img/1/Image00001.jpg"
    imageB = "img/2/Image00001.jpg"
    image = "img/concat/image0000001.png"

    imdiff = ImageDiff(grayscale=False)
    # imageA = imdiff.add_image(imageA)
    # imageB = imdiff.add_image(imageB)
    imageA = imdiff.add_image(imageA)
    imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    print(imageA.shape)


    # a = imdiff.get_splitted(image, parts=4)
    # for i in a:
        # imdiff.show_image(i, wait=True)
    # imdiff.compare_all(interactive=True)
    # imdiff.print_stats()
    # imdiff.save_stats()
    # imdiff.save_stats(save_format='csv')
