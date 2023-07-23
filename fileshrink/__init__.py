import cv2
import os
import numpy as np
import subprocess
import zipfile
from glob import glob
import shutil
import tempfile
from tqdm import trange

# Directory Management
try:
    # Run in Terminal
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
except Warning:
    # Run in ipykernel & interactive
    ROOT_DIR = os.getcwd()
# TMP_DIR = os.path.join(ROOT_DIR, "temp")
TMP_DIR = tempfile.mkdtemp()

OUTPUT_DISPLAY = False


def debug_print(*args):
    if OUTPUT_DISPLAY:
        print(*args)

def pngquant_compress(fp, force=False, quality=None):
    '''
    description: Compress png images using pngquant.exe
        param {*} fp: file path
        param {*} force: whether to overwrite existing files (default behavior) (default: False)
        param {*} quality: 1-100(low-high)
    '''
    force_command = '-f' if force else ''

    quality_command = ''
    if quality and isinstance(quality, int):
        quality_command = f'--quality {quality}'
    if quality and isinstance(quality, str):
        quality_command = f'--quality {quality}'

    if os.path.isfile(fp):
        command = ROOT_DIR + \
            f'/pngquant/pngquant.exe \"{fp}\" --skip-if-larger {force_command} {quality_command} --ext=.png'
        subprocess.run(command)
    elif os.path.isdir(fp):
        command = ROOT_DIR + \
            f'/pngquant/pngquant.exe \"{fp}\"\\*.png --skip-if-larger {force_command} {quality_command} --ext=.png'
        subprocess.run(command)
    else:
        debug_print(f'Warning: {fp} is not a file or directory.')


def shrink_images(folder_path, PNG_Quality, JPEG_Quality, use_pngquant=True):
    # Get the list of files in the folder
    files = os.listdir(folder_path)

    # batch compress png
    debug_print("Shrinking png images...")
    if use_pngquant:
        debug_print("pngquant(no progress bar)")
        pngquant_compress(folder_path, force=True, quality=PNG_Quality)
    else:
        if OUTPUT_DISPLAY: progress = trange(len(files))
        for i in range(len(files)):
            file = files[i]
            if OUTPUT_DISPLAY: progress.update(1)
            image_path = os.path.join(folder_path, file)
            if file.endswith('.png'):
                # Support Chinese path
                image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
                cv2.imencode(".png", image, [cv2.IMWRITE_PNG_COMPRESSION,
                             PNG_Quality])[1].tofile(image_path)
    # batch compress jpg
    debug_print("Shrinking jpg images...")
    if OUTPUT_DISPLAY: progress = trange(len(files))
    for i in range(len(files)):
        file = files[i]
        if OUTPUT_DISPLAY: progress.update(1)
        image_path = os.path.join(folder_path, file)

        if file.endswith('.jpg') or file.endswith('.jpeg'):
            # Support Chinese path
            image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
            cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY,
                                         JPEG_Quality])[1].tofile(image_path)
        # elif file.endswith('.png'):
        #     pngquant_compress(image_path, force=True, quality=PNG_Quality)


def zipDir(dirpath, outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')

        for filename in filenames:
            zip.write(os.path.join(path, filename),
                      os.path.join(fpath, filename))
    zip.close()


def xmind_shrink(path, PNG_Quality=10, JPEG_Quality=20, replace=True, use_pngquant=True):
    """
    Shrinking xmind file(s)
    :param path: xmind file path or folder path containing the xmind files
    :param PNG_Quality: CV: 0-9(high-low) | pngquant: 1-100(low-high)
    :param JPEG_Quality: CV: 0-100(low-high)
    :param replace: whether to replace the original file (default: True)
    :param use_pngquant: whether to use pngquant.exe to compress png images (default: True)
    """

    xmind_files = []
    if path is None:
        debug_print("Please specify the path of the xmind file or folder containing the xmind files.")
        return
    if os.path.isfile(path):
        xmind_files = [path]
    elif os.path.isdir(path):
        xmind_files = glob(path+'/**/*.xmind', recursive=True)
    
    debug_print("Xmind Files:")
    for i in range(len(xmind_files)):
        debug_print(f'{i+1}: {xmind_files[i]}')
    debug_print('\n')
    
    for file in xmind_files:
        if file.endswith('.shrink.xmind'):
            continue
        debug_print('Shrinking No.%02d: %s' % (xmind_files.index(file)+1, file))
        if os.path.exists(TMP_DIR):
            shutil.rmtree(TMP_DIR)
        zip = zipfile.ZipFile(file)
        zip.extractall(TMP_DIR)
        zip.close()
        if os.path.exists(os.path.join(TMP_DIR, "attachments")):
            shrink_images(os.path.join(TMP_DIR, "attachments"),
                          PNG_Quality, JPEG_Quality, use_pngquant=use_pngquant)
            if replace:
                zipDir(TMP_DIR, file)
            else:
                zipDir(TMP_DIR, file+".shrink.xmind")
        else:
            debug_print(f'No images found in: {file}')
    shutil.rmtree(TMP_DIR)


if __name__ == "__main__":
    # Specify the <xmind file path> OR <folder path containing the xmind files>
    # folder_path = "D:\\CodeTestFiles\\HITSA-Courses-Xmind-Note"
    folder_path = "E:\\Temp\\Player One.xmind"

    # Specify the compression level
    use_pngquant = True
    # CV: 0-9(high-low) | pngquant: 1-100(low-high)
    PNG_Quality = 10
    # CV: 0-100(low-high)
    JPEG_Quality = 20
    
    '''
    ideal for xmind files: PNG_Quality=10, JPEG_Quality=20
    extreme compression: PNG_Quality=1, JPEG_Quality=0 (PNG will lose color(almost B&W?), JPEG will lose color details)
    '''
    OUTPUT_DISPLAY = True
    xmind_shrink(folder_path, PNG_Quality, JPEG_Quality, replace=True,
                 use_pngquant=use_pngquant)
