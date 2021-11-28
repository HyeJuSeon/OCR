import cv2
import json
import os
from tqdm import tqdm
import numpy as np
import shutil
import random

base_dir = 'D:/korean_text_image'

def annotations(file):
    result = []
    with open(file, encoding='utf-8') as f:
        annotation = json.load(f)
    for annotation in annotation['annotations']:
        bbox = annotation['bbox']
        text = annotation['text']
        result.append((bbox, text))
    # filename = file['images'][0]['file_name']
    return result

def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        img_array = np.fromfile(filename, dtype)
        return cv2.imdecode(img_array, flags)
    except Exception as e:
        print(e)
        return None

def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)
        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
                return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def preprocessing(phase):
    labels = open(f'{base_dir}/data/gt_{phase}.txt', 'w')
    file_ext = r'.json'
    files = [_ for _ in os.listdir(f'{base_dir}/{phase}/[label]{phase}/1.간판') if _.endswith(file_ext)]
    # print(len(files))
    # print(len(os.listdir(f'{base_dir}/{phase}/[source]{phase}_간판_가로형간판')))
    for file in tqdm(files):
        annotation = annotations(f'{base_dir}/{phase}/[label]{phase}/1.간판/{file}')
        for i, anno in enumerate(annotation):
            bbox, text = anno
            if text == 'xxx':
                continue
            x, y, width, height = bbox
            # 한글 경로
            # img = cv2.imread(f'{base_dir}/{phase}/[source]{phase}_간판_가로형간판/{file[:-5]}.jpg')
            img = imread(f'{base_dir}/{phase}/[source]{phase}_간판_가로형간판/{file[9:-5]}.jpg')
            try:
                cropped = img[y:y + height, x:x + width]
            except:
                print(f'{base_dir}/{phase}/[source]{phase}_간판_가로형간판/{file[9:-5]}.jpg')
                break
            # 한글 경로
            # cv2.imwrite(f'{base_dir}/data/{phase}/{file[:-5]}_{i}.jpg', cropped)
            imwrite(f'{base_dir}/data/{phase}/{file[:-5]}_{i}.jpg', cropped)
            # cv2_imshow(cropped)
            # print(f'{drive_path}/data/{phrase}/{file[:-5]}_{i}.jpg', text)
            labels.write(f'{phase}/{file[:-5]}_{i}.jpg\t{text}\n')
    labels.close()

def img_remove():
    # 媛꾪뙋_媛\x80濡쒗삎媛꾪뙋 이름이 잘못 저장된 경우
    path = f'{base_dir}/data/train'
    files = os.listdir(path)
    for file in files:
        if '꾪' in file:
            os.remove(f'{path}/{file}')
    print('remove', len(os.listdir(path)))

def val_test_split():
    from_ = f'{base_dir}/data/val/'
    to_ = f'{base_dir}/data/test/'
    shutil.copyfile(f'{base_dir}/data/gt_val.txt', f'{base_dir}/data/val_test.txt')
    with open(f'{base_dir}/data/gt_val.txt', 'r') as f:
        val_labels = f.readlines()
    test_samples = random.sample(val_labels, len(val_labels) // 2)

    test_labels = []
    for sample in tqdm(test_samples):
        val_labels.remove(sample)
        test_labels.append(sample.replace('val', 'test'))
        tab_idx = sample.find('\t')
        filename = sample[4:tab_idx]
        shutil.move(from_ + filename, to_ + filename)

    with open(f'{base_dir}/data/gt_val.txt', 'w') as f:
        f.writelines(val_labels)
    with open(f'{base_dir}/data/gt_test.txt', 'w') as f:
        f.writelines(test_labels)
    print('val image number:', len(os.listdir(f'{base_dir}/data/val')), 'val label number:', len(val_labels))
    print('test image number:', len(os.listdir(f'{base_dir}/data/test')), 'test label number:', len(test_labels))

def canny_threshold(idx):
    path = f'{base_dir}/data/train'
    files = os.listdir(path)
    file = files[idx]
    img = imread(f'{path}/{file}', cv2.IMREAD_GRAYSCALE)
    winname = 'gray'
    cv2.namedWindow(winname, flags=cv2.WINDOW_NORMAL)
    cv2.moveWindow(winname, 40, 30)
    cv2.imshow(winname, img)
    cv2.waitKey(0)
    thresholds = [(50, 200), (50, 100), (30, 100), (30, 70), (30, 50), (20, 100), (20, 70), (20, 50)]
    for threshold in thresholds:
        th1, th2 = threshold
        canny = cv2.Canny(img, th1, th2)
        winname = f'canny_{th1}_{th2}'
        cv2.namedWindow(winname, flags=cv2.WINDOW_NORMAL)
        cv2.moveWindow(winname, 40, 30)
        cv2.imshow(winname, canny)
        cv2.waitKey(0)
    cv2.destroyAllWindow()

def canny_edge_detection(phase, threshold=(50, 200)):
    path_origin = f'{base_dir}/data/{phase}'
    path_canny = f'{base_dir}/canny_data/{phase}'
    files = os.listdir(path_origin)
    th1, th2 = threshold
    for file in tqdm(files):
        img = imread(f'{path_origin}/{file}', cv2.IMREAD_GRAYSCALE)
        canny = cv2.Canny(img, th1, th2)
        imwrite(f'{path_canny}/{file}', canny)
    # copy label
    shutil.copyfile(f'{base_dir}/data/gt_{phase}.txt', f'{base_dir}/canny_data/gt_{phase}.txt')


if __name__ == '__main__':
    preprocessing('train')
    preprocessing('val')
    img_remove()
    val_test_split()
    # canny_threshold(333)
    canny_edge_detection('train')
    canny_edge_detection('val')
    canny_edge_detection('test')
