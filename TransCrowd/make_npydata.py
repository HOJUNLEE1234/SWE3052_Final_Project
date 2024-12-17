import os
import numpy as np

if not os.path.exists('./npydata'):
    os.makedirs('./npydata')


'''please set your dataset path'''


try:
    UCFQNRFtrain_path = '/content/drive/MyDrive/심신개/UCF-QNRF_ECCV18/train_data/images_crop/'
    UCFQNRFtest_path = '/content/drive/MyDrive/심신개/UCF-QNRF_ECCV18/test_data/images_crop/'

    train_list = []
    for filename in os.listdir(UCFQNRFtrain_path):
        if filename.split('.')[1] == 'jpg':
            train_list.append(UCFQNRFtrain_path + filename)
    train_list.sort()
    np.save('./npydata/qnrf_train.npy', train_list)

    test_list = []
    for filename in os.listdir(UCFQNRFtest_path):
        if filename.split('.')[1] == 'jpg':
            test_list.append(UCFQNRFtest_path + filename)
    test_list.sort()
    np.save('./npydata/qnrf_test.npy', test_list)
    print("Generate UCF-QNRF image list successfully", len(train_list), len(test_list))
except:
    print("The UCF-QNRF dataset path is wrong. Please check your path.")
