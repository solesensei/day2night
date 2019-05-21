import os
import sys
import numpy as np
from datetime import timedelta
from tqdm import tqdm
import imageio
sys.path.append(os.path.abspath(".."))
from ImageDiff.compare import ImageDiff
from PIL import Image

def vid2img(video_path, images_dir, fps=-1, duration=-1):
    if not os.path.exists(images_dir):
        print(f'No {images_dir} path found')
        return
    if fps == -1:
        reader = imageio.get_reader(video_path)
    else:
        reader = imageio.get_reader(video_path, fps=fps)
    vid_format = os.path.splitext(os.path.basename(video_path))[1].upper()
    vid_fps = reader.get_meta_data()['fps']
    vid_len = int(reader.get_meta_data()['duration'])
    vid_flen = str(timedelta(seconds=vid_len))
    frames = vid_frames = int(vid_len * vid_fps)
    if duration != -1:
        f_duration = str(timedelta(seconds=duration))
        frames = min(int(duration * vid_fps), vid_frames)
    else:
        f_duration = 'full'

    print(f'Start converting: {vid_format} -> IMAGES | {video_path} -> {images_dir}')
    print(f'FPS: {int(vid_fps)}')
    print(f'Video Duration: {vid_flen}')
    print(f'Video Frames: {vid_frames}')
    print(f'Save Duration: {f_duration}')
    print(f'Save Frames: {frames}')

    for i, image in enumerate(tqdm(reader, total=frames, desc='Split video into frames')):
        if i == frames:
            break
        img_name = f'{images_dir}/image{str(i+1).zfill(7)}.png'
        imageio.imwrite(img_name, image)
    reader.close()
    print(f'Complete!')

def gif2img(gif_path, images_dir, duration=-1):
    if not os.path.exists(images_dir):
        print(f'No {images_dir} path found')
        return
    gif = Image.open(gif_path)
    frames = gif_frames = gif.n_frames
    gif_len = int(gif.info['duration']) / 1000 * frames
    gif_flen = str(timedelta(seconds=gif_len))
    gif_fps = frames // gif_len
    if duration != -1:
        f_duration = str(timedelta(seconds=duration))
        frames = min(int(duration * gif_fps), gif_frames)
    else:
        f_duration = 'full'

    print(f'Start converting: GIF -> IMAGES | {gif_path} -> {images_dir}')
    print(f'GIF Duration: {gif_flen}')
    print(f'GIF Frames: {gif_frames}')
    print(f'Save Duration: {f_duration}')
    print(f'Save Frames: {frames}')

    for frame in tqdm(range(0, frames), desc='Split gif into frames'):
        gif.seek(frame)
        img_name = f'{images_dir}/image{str(frame+1).zfill(7)}.png'
        gif.save(img_name)
    gif.close()
    print(f'Complete!')

def vid2gif(video_path, gif_path, fps=-1, duration=-1):
    if not os.path.exists(video_path):
        print(f'No {video_path} path found')
        return
    if fps == -1:
        reader = imageio.get_reader(video_path)
    else:
        reader = imageio.get_reader(video_path, fps=fps)
    vid_format = os.path.splitext(os.path.basename(video_path))[1].upper()
    fps = vid_fps = reader.get_meta_data()['fps']
    vid_len = int(reader.get_meta_data()['duration'])
    vid_flen = str(timedelta(seconds=vid_len))
    frames = vid_frames = int(vid_len * vid_fps)
    vid_fps = reader.get_meta_data()['fps']
    vid_len = int(reader.get_meta_data()['duration'])
    vid_flen = str(timedelta(seconds=vid_len))
    vid_frames = int(vid_len * vid_fps)
    if duration != -1:
        f_duration = str(timedelta(seconds=duration))
        frames = min(int(duration * vid_fps), vid_frames)
    else:
        f_duration = 'full'

    print(f'Start converting: {vid_format} -> GIF | {video_path} -> {gif_path}')
    print(f'FPS: {int(vid_fps)}')
    print(f'Video Duration: {vid_flen}')
    print(f'Video Frames: {vid_frames}')
    print(f'Save Duration: {f_duration}')
    print(f'Save Frames: {frames}')

    with imageio.get_writer(gif_path, mode='I', fps=fps) as writer:
        for i, image in enumerate(tqdm(reader, total=frames, desc='Converting to GIF')):
            if i == frames:
                break
            writer.append_data(image)
    reader.close()
    print(f'Complete!')


def img2gif(images_dir, gif_path, fps=2, duration=-1):
    if not os.path.isdir(images_dir):
        print(f'No {images_dir} folder found')
        return

    images = []
    for root, _, imgs in os.walk(images_dir):
        for image in imgs:
            if image.endswith('.png') or image.endswith('.jpg'):
                images.append(os.path.join(root, image))
        break
    images.sort()
    if not images:
        print(f'No images found in {images_dir}')
        return
    frames = len(images)
    if duration != -1:
        f_duration = str(timedelta(seconds=duration))
        frames = min(int(duration * fps), len(images))
    else:
        f_duration = 'full'

    print(f'Start converting: IMAGES -> GIF | {images_dir} -> {gif_path}')
    print(f'FPS: {fps}')
    print(f'Images in folder: {len(images)}')
    print(f'Save Duration: {f_duration}')
    print(f'Save Frames: {frames}')

    with imageio.get_writer(gif_path, mode='I', fps=fps) as writer:
        for i, image in enumerate(tqdm(images, total=frames, desc='Converting to GIF')):
            if i == frames:
                break
            image = imageio.imread(image)
            writer.append_data(image)
    print(f'Complete!')


def img_resize(image, factor, opencv=False, save=False):
    if factor == 0:
        print('Factor can\'t be equal to zero')
        return
    try:
        if opencv:
            im = Image.fromarray(image)
        else:
            im = Image.open(image)
        s = max(im.size) // factor
        im.thumbnail((s, s))
        if save:
            outfile = os.path.splitext(image)[0] + "_r.png"
            im.save(outfile, "PNG")
        if opencv:
            return np.array(im)
        return im
    except IOError:
        print(f"Cannot create thumbnail for '{image}'")


def img2img(images_dir_1, images_dir_2, sort=True, resize=0, concat=0, concat_dir='img/concat'):
    images_1 = []
    for root, _, imgs in os.walk(images_dir_1):
        for image in imgs:
            if image.endswith('.png') or image.endswith('.jpg'):
                images_1.append(os.path.join(root, image))
        break
    if sort:
        images_1.sort()
    if concat:
        if not os.path.isdir(concat_dir):
            os.mkdir(concat_dir)
        images_2 = []
        for root, _, imgs in os.walk(images_dir_2):
            for image in imgs:
                if image.endswith('.png') or image.endswith('.jpg'):
                    images_2.append(os.path.join(root, image))
            break
        if sort:
            images_2.sort()
        imdiff = ImageDiff(grayscale=False)
        for (image_1, image_2) in tqdm(zip(images_1, images_2), total=min(len(images_1), len(images_2)), desc='Concatenation'):
            im_1 = imdiff.get_image(image_1, rgb=True)
            im_2 = imdiff.get_image(image_2, rgb=True)
            c = imdiff.get_concated(im_1, im_2, to_rgb=False)
            if resize:
                c = img_resize(c, resize, opencv=True)
            dst = os.path.join(concat_dir, os.path.basename(image_1))
            imdiff.save_image(c, dst)
    elif resize:
        for im in images_1:
            im = img_resize(im, resize)
            dst = os.path.join(images_dir_2, os.path.basename(image_1))
            im.save(dst, "PNG")
    else:
        print('Nothing to do')


if __name__ == "__main__":

    data_dir = '/home/sole/prj/data/alderley'
    # data_dir = '/mnt/w/prj/data/alderley'
    day_dir = f'{data_dir}/FRAMESB/'
    night_dir = f'{data_dir}/FRAMESA/'
    day_vid = f'{data_dir}/day1_orig.avi'
    night_vid = f'{data_dir}/night1_orig.avi'
    check_dir = '/mnt/w/prj/GraduateWork/day2night/UNIT/checkpoints'
    gif_path = './gif/day2night.gif'

    # gif2img(gif_path, 'gif/img')
    # img2img('gif/img', 'gif/img/vgg', concat=True, concat_dir=f'img')
    img2gif('img', 'day2night.gif', fps=10)
    # img2img(f'{check_dir}/unit/out', f'{check_dir}/unit_no_err/out', concat=True, concat_dir=f'{check_dir}/unit_no_err/concat2')
    # img2img(f'{check_dir}/unit/out/input', f'{check_dir}/unit_no_err/concat2', concat=True, concat_dir=f'{check_dir}/unit/concat3')
    # vid2img(night_vid, 'img/night_orig', fps=5, duration=20)
    # vid2img(day_vid, 'img/day_orig', fps=5, duration=20)
    # img2gif('img/day_orig', 'gif/day_orig.gif', fps=5)
    # img2gif('img/night_orig', 'gif/night_orig.gif', fps=5)
    # img2gif('/mnt/w/prj/GraduateWork/day2night/UNIT/checkpoints/vgg/out/concat_3', '/mnt/w/prj/GraduateWork/day2night/UNIT/checkpoints/vgg/out/concat_3/concat_3.gif', fps=8)
