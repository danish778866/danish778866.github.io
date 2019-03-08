import numpy as np  
import pandas as pd  
import os, getopt, sys
import pickle
from sklearn.model_selection import train_test_split  
from sklearn.svm import SVC 
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier 
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score  

def usage():
    print("You should just know!")
    sys.exit(2)

def test_model(model, project_dir, test_dir_name, classifier):
    feature_vector, labels = read_input(project_dir, test_dir_name)
    x_test = feature_vector.values
    y_test = labels.values
    y_pred = predict_class(model, x_test, classifier)
    print_prediction_stats(y_test, y_pred)

def train_model(project_dir, dev_dir_name, classifier):
    feature_vector, labels = read_input(project_dir, dev_dir_name)
    x_train, x_test, y_train, y_test = split_data(feature_vector, labels)
    model = create_model(x_train, y_train, classifier)
    y_pred = predict_class(model, x_test, classifier)
    print_prediction_stats(y_test, y_pred)
    print_wrong_predictions(y_pred, y_test, x_test)
    return model

def read_input(project_dir, data_dir_name):
    features_csv = project_dir + os.sep + "data" + os.sep + data_dir_name + os.sep + "features" + os.sep + "features.csv"
    labels_csv = project_dir + os.sep + "data" + os.sep + data_dir_name + os.sep + "labels" + os.sep + "labels.csv"
    feature_vector = pd.read_csv(features_csv)
    labels = pd.read_csv(labels_csv)
    return feature_vector, labels

def split_data(feature_vector, labels):
    x = feature_vector.values
    y = labels.values
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    return x_train, x_test, y_train, y_test

def create_model(x_train, y_train, classifier):
    if classifier == "svm":
        model = SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
           decision_function_shape='ovr', degree=3, gamma='scale', kernel='rbf',
           max_iter=-1, probability=False, random_state=None, shrinking=True,
           tol=0.001, verbose=False)       
    elif classifier == "linear":
        model = LinearRegression()
    elif classifier == "logistic":
        model = LogisticRegression(random_state=0, solver='liblinear', multi_class='ovr')
    elif classifier == "random":
        model = RandomForestClassifier(n_estimators=20, random_state=0)  
    elif classifier == "decision":
        model = DecisionTreeClassifier(criterion = "gini", random_state = 100,max_depth=3, min_samples_leaf=5) 
    else:
        print("Please enter a valid classifier...")
        usage()
    X_train = x_train[:, 3:]
    model.fit(X_train, y_train.ravel())
    return model

def predict_class(model, x_test, classifier):
    X_test = x_test[:, 3:]
    y_pred = model.predict(X_test)
    if classifier == "linear":
        y_pred = [1 if y > 0.5 else 0 for y in y_pred]
    return y_pred
   
def print_prediction_stats(y_test, y_pred):
    print("...Confusion Matrix...")
    print(confusion_matrix(y_test,y_pred))
    print("...Classification Report...")
    print(classification_report(y_test,y_pred))
    print("...Accuracy Score...")
    print(accuracy_score(y_test, y_pred))

def print_wrong_predictions(y_pred, y_test, x_test):
    for yp, yt, xt in zip(y_pred, y_test, x_test):
        if yp != yt and yt == 1:
            print (xt[0:3], yt, yp)

def finalize_model(model, project_dir, classifier):
    models_dir = project_dir + os.sep + "models"
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    model_filename = models_dir + os.sep + classifier + ".sav"
    pickle.dump(model, open(model_filename, 'wb'))

def load_model(project_dir, classifier):
    models_dir = project_dir + os.sep + "models"
    model_filename = models_dir + os.sep + classifier + ".sav"
    model = pickle.load(open(model_filename, 'rb'))
    return model

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:t:c:s", ["help", "dev=", "test=", "classifier=", "save"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
    dev_dir = ""
    test_dir = ""
    classifier = ""
    save_model = False
    for o, a in opts:
        if o in ("-d", "--dev"):
            dev_dir = a
        elif o in ("-t", "--test"):
            test_dir = a
        elif o in ("-c", "--classifier"):
            classifier = a
        elif o in ("-s", "--save"):
            save_model = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"
    project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    if dev_dir != "" and classifier != "":
        model = train_model(project_dir, dev_dir, classifier)
        if save_model:
            finalize_model(model, project_dir, classifier)
        if test_dir != "":
            test_model(model, project_dir, test_dir, classifier)
    elif dev_dir == "" and test_dir != "" and classifier != "":
        model = load_model(project_dir, classifier)
        test_model(model, project_dir, test_dir, classifier)
    else:
        usage()

if __name__ == '__main__':
    main()
