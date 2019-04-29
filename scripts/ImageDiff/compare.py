import os
import json
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import compare_ssim as ssim

images_1 = "img/1/Image00001.jpg"
images_2 = "img/2/Image00001.jpg"

class ImageDiff:
    def __init__(self, grayscale=True):
        self.images = {}
        self.grayscale = grayscale
        # self.fig = plt.figure("Images")

    def mse(self, imageA, imageB):
        """
        The 'Mean Squared Error' between the two images is the
        sum of the squared difference between the two images
        ```
        NOTE: the two images must have the same dimension
        return the MSE, the lower the error, the more "similar" images are
        ```
        """
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        return err

    def ssim(self, imageA, imageB):
        """
        The 'Structural Similarity' between the two images is the perception-based
        index for measuring the similarity between two images.
        ```
        return the SSIM, the higher is better
        ```
        """
        if self.grayscale:
            return ssim(imageA, imageB, full=True)
        return ssim(imageA, imageB, multichannel=True, full=True)
    
    def get_diff(self, imageA, imageB):
        return cv2.subtract(imageA, imageB)

    def get_absdiff(self, imageA, imageB):
        return cv2.absdiff(imageA, imageB)

    def is_equal(self, imageA, imageB):
        diff = cv2.subtract(imageA, imageB)
        return not np.any(diff)

    def compare_images(self, imageA, imageB, interactive=False, title='Compare'):
        m = self.mse(imageA, imageB)
        s, d = self.ssim(imageA, imageB)
        d = (d * 255).astype("uint8")
        thresh = cv2.threshold(d, 0, 255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        is_equal = self.is_equal(imageA, imageB)
        if is_equal:
            msg = "The images are the same"
        else:
            msg = "The images are different"

        print(f"Title: {title} MSE: {m:.2f}, SSIM: {s:.6}, msg: {msg}")

        if interactive:
            self.show_plt_diff(imageA, imageB, m, s, title, msg)
        print(d)
        print(d)
        
        diff = self.get_diff(imageA, imageB)


        cv2.imshow("Diff", d)
        cv2.imshow("Diff(stand)", diff)        
        cv2.imshow("Thresh", thresh)
        cv2.waitKey(0)

        return m, s, msg

    def compare_all(self, interactive=False):
        for name, values in self.images.items():
            images = values.get('images', [])
            if len(images) < 2:
                print(f'Image {name} has no pair to compare')
            else:
                m, s, msg = self.compare_images(images[0], images[1], title=name, interactive=interactive)
                values['MSE'] = m
                values['SSIM'] = s
                values['msg'] = msg

    def add_image(self, path, name=None):
        if not os.path.exists(path) and (path.endswith('.png') or path.endswith('.jpg')):
            raise FileNotFoundError(f'No {path} image found. Supported ext: [.jpg|.png ]')

        image = cv2.imread(path)
        if self.grayscale:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if name is None:
            name = os.path.splitext(os.path.basename(path))[0]

        self.images[name] = self.images.get(name, {})
        self.images[name]['MSE'] = ""
        self.images[name]['SSIM'] = ""
        self.images[name]['images'] = self.images[name].get('images', [])
        self.images[name]['images'].append(image)
        return image

    def load_images(self, *pathes):
        for path in pathes:
            if not os.path.exists(path):
                raise FileExistsError(f'No {path} found')

            if os.path.isdir(path):
                for r, _, f in os.walk(path):
                    for file in f:
                        if file.endswith('.png') or file.endswith('.jpg'):
                            src = os.path.join(r, file)
                            self.add_image(src)
                    break
            else:
                self.add_image(path)
        return self.images

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

    def show_plt_diff(self, imageA, imageB, m, s, title, msg):
        self._setup_plt(imageA, imageB, m, s, title, msg)
        plt.show()

    def get_json_stats(self):
        j = {}
        for image, values in self.images.items():
            j[image] = {}
            j[image]['MSE'] = values['MSE']
            j[image]['SSIM'] = values['SSIM']
            j[image]['msg'] = values['msg']
        return j

    def print_stats(self):
        j = self.get_json_stats()
        print(json.dumps(j, indent=4, sort_keys=True))

    def save_image(self, image, filename='image.png'):
        cv2.imwrite(filename, image)

    def save_diff_images(self, imageA, imageB, name='image.png', sides=False, absolute=False):
        diff = self.get_diff(imageA, imageB)
        if self.is_equal(imageA, imageB):
            pass


    def save_stats(self, filename='stats', save_format='json'):
        filename = os.path.splitext(os.path.basename(filename))[0]
        if save_format == 'json':
            j = self.get_json_stats()
            with open(f'{filename}.json', 'w') as stats:
                json.dump(j, stats, indent=4, sort_keys=True)
        elif save_format == 'csv':
            j = self.get_json_stats()
            with open(f'{filename}.csv', 'w') as stats:
                print('image_name,MSE,SSIM,Message', file=stats)
                for image, v in j.items():
                    m, s, msg = v['MSE'], v['SSIM'], v['msg']
                    print(f'{image},{m},{s},{msg}', file=stats)
        else:
            print(f'Error: Save format {save_format} not supported')


imdiff = ImageDiff(grayscale=True)
images = imdiff.load_images(images_1, images_2)


imdiff.compare_all(interactive=True)
imdiff.print_stats()
imdiff.save_stats()
imdiff.save_stats(save_format='csv')
