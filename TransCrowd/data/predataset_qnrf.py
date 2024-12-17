import os
import glob
import cv2
import h5py
import numpy as np
import scipy.io

# 데이터셋 경로 설정
root = '/content/drive/MyDrive/심신개/UCF-QNRF_ECCV18'
img_train_path = os.path.join(root, 'Train')
img_test_path = os.path.join(root, 'Test')

# 저장 경로 설정
save_train_img_path = img_train_path.replace('Train', 'train_data/images_crop')
save_test_img_path = img_test_path.replace('Test', 'test_data/images_crop')

save_train_gt_path = img_train_path.replace('Train', 'train_data/gt_density_map_crop')
save_test_gt_path = img_test_path.replace('Test', 'test_data/gt_density_map_crop')

os.makedirs(save_train_img_path, exist_ok=True)
os.makedirs(save_test_img_path, exist_ok=True)
os.makedirs(save_train_gt_path, exist_ok=True)
os.makedirs(save_test_gt_path, exist_ok=True)

distance = 1
img_train = []
img_test = []


path_sets = [img_train_path, img_test_path]

img_paths = []
for path in path_sets:
    for img_path in glob.glob(os.path.join(path, '*.jpg')):
        img_paths.append(img_path)

img_paths.sort()


for img_path in img_paths:


    Img_data = cv2.imread(img_path)
    Gt_data = scipy.io.loadmat(img_path.replace('.jpg', '_ann.mat'))

    Gt_data = Gt_data['annPoints']

    if Img_data.shape[1] >= Img_data.shape[0]:
        rate_1 = 1152.0 / Img_data.shape[1]
        rate_2 = 768 / Img_data.shape[0]
        Img_data = cv2.resize(Img_data, (0, 0), fx=rate_1, fy=rate_2)
        Gt_data[:, 0] = Gt_data[:, 0] * rate_1
        Gt_data[:, 1] = Gt_data[:, 1] * rate_2

    elif Img_data.shape[0] > Img_data.shape[1]:
        rate_1 = 1152.0 / Img_data.shape[0]
        rate_2 = 768.0 / Img_data.shape[1]
        Img_data = cv2.resize(Img_data, (0, 0), fx=rate_2, fy=rate_1)
        Gt_data[:, 0] = Gt_data[:, 0] * rate_2
        Gt_data[:, 1] = Gt_data[:, 1] * rate_1
        print(img_path)


    kpoint = np.zeros((Img_data.shape[0], Img_data.shape[1]))
    for count in range(0, len(Gt_data)):
        if int(Gt_data[count][1]) < Img_data.shape[0] and int(Gt_data[count][0]) < Img_data.shape[1]:
            kpoint[int(Gt_data[count][1]), int(Gt_data[count][0])] = 1

    height, width = Img_data.shape[0], Img_data.shape[1]

    m = int(width / 384)
    n = int(height / 384)
    fname = img_path.split('/')[-1]
    root_path = img_path.split('img_')[0]


    if root_path.split('/')[-2] == 'Train':

        for i in range(0, m):
            for j in range(0, n):
                crop_img = Img_data[j * 384: 384 * (j + 1), i * 384:(i + 1) * 384, ]
                crop_kpoint = kpoint[j * 384: 384 * (j + 1), i * 384:(i + 1) * 384, ]
                gt_count = np.sum(crop_kpoint)

                save_fname = str(i) + str(j) + str('_') + fname
                save_path = root_path.replace('Train', 'train_data/images_crop') + save_fname
                h5_path = save_path.replace('.jpg', '.h5').replace('images_crop', 'gt_density_map_crop')

                with h5py.File(h5_path, 'w') as hf:
                    hf['gt_count'] = gt_count
                cv2.imwrite(save_path, crop_img)

    else:
        save_path = root_path.replace('Test', 'test_data/images_crop') + fname
        print(save_path)
        cv2.imwrite(save_path, Img_data)

        gt_count = np.sum(kpoint)
        with h5py.File(save_path.replace('.jpg', '.h5').replace('images_crop', 'gt_density_map_crop'), 'w') as hf:
            hf['gt_count'] = gt_count