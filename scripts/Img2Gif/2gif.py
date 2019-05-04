import os
from datetime import timedelta
from tqdm import tqdm
import imageio

day_dir = '/mnt/w/prj/data/alderley/FRAMESA/'
day_dir = '/mnt/w/prj/data/alderley/FRAMESB/'
day_vid = '/mnt/w/prj/data/alderley/day1_orig.avi'
night_vid = '/mnt/w/prj/data/alderley/night1_orig.avi'


def vid2gif(video_path, gif_path, fps=-1, duration=-1):
    if not os.path.exists(video_path):
        print(f'No {video_path} path found')
        return 1
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
        for i,image in enumerate(tqdm(reader, total=frames)):
            if i == frames:
                break
            writer.append_data(image)
    reader.close()
    print(f'Complete!')


def img2gif(images_dir, gif_path, fps=2, duration=-1):
    if not os.path.exists(images_dir):
        print(f'No {images_dir} path found')
        return 1

    images = []
    for root, _, imgs in os.walk(images_dir):
        for image in imgs:
            if image.endswith('.png') or image.endswith('.jpg'):
                images.append(os.path.join(root, image))
    if not images:
        print(f'No images found in {images_dir}')
        return 1
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
        for i,image in enumerate(tqdm(images, total=frames)):
            if i == frames:
                break
            image = imageio.imread(image)
            writer.append_data(image)
    print(f'Complete!')


def vid2img(video_path, images_dir, fps=-1, duration=-1):
    if not os.path.exists(images_dir):
        print(f'No {images_dir} path found')
        return 1
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

    for i, image in enumerate(tqdm(reader, total=frames)):
        if i == frames:
            break
        img_name = f'{images_dir}/image{str(i+1).zfill(7)}.png'
        imageio.imwrite(img_name, image)
    reader.close()
    print(f'Complete!')


# vid2img(night_vid, 'img/night_orig', fps=5, duration=20)
# vid2img(day_vid, 'img/day_orig', fps=5, duration=20)
img2gif('img/day_orig', 'gif/day_orig.gif', fps=5)
img2gif('img/night_orig', 'gif/night_orig.gif', fps=5)
# vid2gif(path2vid, path2gif)
# vid2gif("/home/sole/Documents/alderley/night1_orig.avi", 'night.gif')\