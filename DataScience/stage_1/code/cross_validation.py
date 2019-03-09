import os
import glob
import shutil
import subprocess
from sklearn.model_selection import KFold

fileList = glob.glob('../data/train/*.txt')
kf = KFold(n_splits = 10)
kf.get_n_splits(fileList)

models = ["svm", "random", "decision", "logistic", "linear"]

os.makedirs("../fold_logs", exist_ok=True)

j = 1;

for train_index, test_index in kf.split(fileList):
    X_train  = [fileList[i] for i in train_index]
    X_test = [fileList[i] for i in test_index]
    train_dir = '../data/train_curr'
    test_dir = '../data/test_curr'

    if os.path.isdir(train_dir):
        shutil.rmtree(train_dir)

    os.makedirs(train_dir)

    if os.path.isdir(test_dir):
        shutil.rmtree(test_dir)

    os.makedirs(test_dir)

    for curr_train in X_train:
        shutil.copyfile(curr_train, train_dir + '/' + os.path.basename(curr_train))

    for curr_test in X_test:
        shutil.copyfile(curr_test, test_dir + '/' + os.path.basename(curr_test))

    for model in models:
        print("Running for fold " + str(j) + " and model " + model)
        subprocess.call(['./run.sh', '-d', 'train_curr', '-t', 'test_curr', '-c', model, '-s', '-p'])
    if os.path.isdir("../fold_logs/fold_" + str(j)):
        shutil.rmtree("../fold_logs/fold_" + str(j))
    #os.makedirs("../fold_logs/fold_" + str(j), exist_ok=True)
    shutil.copytree("../logs", "../fold_logs/fold_" + str(j))
    j = j + 1

first = True
for model in models:
    sumPrecision = 0
    sumRecall = 0
    for j in range(1, 11):
        file = open("../fold_logs/fold_" + str(j) + "/" + model + ".log")
        for line in file.readlines():
            lineAsString = str(line).strip()
            if len(lineAsString.split()) > 0 and lineAsString.split()[0] == "1" and first:
                first = False
            elif len(lineAsString.split()) > 0 and lineAsString.split()[0] == "1":
                #print(model + " fold " + str(j) + " " + lineAsString)
                sumPrecision = sumPrecision + float(lineAsString.split()[1])
                sumRecall = sumRecall + float(lineAsString.split()[2])
                first = True
    print("Average of Precision for model " + model + " is: " + str(sumPrecision/10))
    print("Average of Recall for model " + model + " is: " + str(sumRecall/10))
    print()
    
   

