import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import compare_ssim as ssim

images_1 = "images/1/Image00001.jpg"
images_2 = "images/2/Image00001.jpg"

class ImageDiff:
    def __init__(self, grayscale=True):
        self.images = {}
        self.grayscale = grayscale
        # self.fig = plt.figure("Images")

    def mse(self, imageA, imageB):
        """
        The 'Mean Squared Error' between the two images is the
        sum of the squared difference between the two images

        NOTE: the two images must have the same dimension
        """
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        # return the MSE, the lower the error, the more "similar"
        # the two images are
        return err

    def ssim(self, imageA, imageB):
        """
        The 'Structural Similarity' between the two images is the perception-based
        index for measuring the similarity between two images.
        """
        if self.grayscale:
            return ssim(imageA, imageB)
        return ssim(imageA, imageB, multichannel=True)

    def is_equal(self, imageA, imageB):
        diff = cv2.subtract(imageA, imageB)
        return not np.any(diff)

    def compare_images(self, imageA, imageB, title='Compare'):
        m = self.mse(imageA, imageB)
        s = self.ssim(imageA, imageB)

        is_equal = self.is_equal(imageA, imageB)
        if is_equal:
            msg = "The images are the same"
        else:
            msg = "The images are different"

        print(f"Title: {title}")
        print(f"MSE: {m:.2f}, SSIM: {s:.6}")
        print(msg)

        self.show_diff(imageA, imageB, m, s, title, msg)

    def compare_all(self):
        for k, v in self.images.items():
            if len(v) < 2:
                print(f'Image {k} has no pair to compare')
            else:
                self.compare_images(v[0],v[1],k)

    def absdiff(self, imageA, imageB):
        return cv2.absdiff(imageA, imageB)

    def add_image(self, path, name=None):
        if not os.path.exists(path) and (path.endswith('.png') or path.endswith('.jpg')):
            raise FileNotFoundError(f'No {path} image found. Possible ext: [.jpg|.png ]')

        image = cv2.imread(path)
        if self.grayscale:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if name is None:
            name = os.path.splitext(os.path.basename(path))[0]

        self.images[name] = self.images.get(name, [])
        self.images[name].append(image)

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

    def get_diff(self, imageA, imageB):
        diff = cv2.subtract(imageA, imageB)
        result = not np.any(diff)
        if result:
            print("The images are the same")
        else:
            print("The images are different")
        return diff

    def show_diff(self, imageA, imageB, m, s, title, msg):
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
        plt.show()
    
    def save_stats(self, csv='stats.csv'):
        pass

imdiff = ImageDiff(grayscale=True)
images = imdiff.load_images(images_1, images_2)


imdiff.compare_all()




# # loop over the images
# for (i, (name, image)) in enumerate(images):
#     # show the image
#     ax = fig.add_subplot(1, 3, i + 1)
#     ax.set_title(name)
#     plt.imshow(image, cmap=plt.cm.gray)
#     plt.axis("off")

# # compare the images
# imdiff.compare_images(original, original, "Original vs. Original")
# imdiff.compare_images(original, contrast, "Original vs. Contrast")
# imdiff.compare_images(original, shopped, "Original vs. Photoshopped")