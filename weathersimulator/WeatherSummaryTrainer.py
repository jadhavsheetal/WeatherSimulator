import numpy as np
import argparse
import FileUtil


from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB 

from sklearn.model_selection import KFold
from nltk.classify.scikitlearn import SklearnClassifier

# Creates a classifier to predict weather summary {Rain, Sunny, Snow} 
# The prediction is based on temperature, pressure, humidity which become the features for training the model
# 
# Builds and trains a classifier based on given training data X and Y
# SKLearnClassifier internally uses DictVectorizer to fit and transform X
# and LabelEncoder to encode class labels
# Multinomial Naive Bayes is set as the model for classification. 
#
class WeatherSummaryTrainer :

    def buildAndTrainClassifier(self, X, Y) :
        print ('Building and Training Classifier')

        n_folds = 10
        kf = KFold(n_splits=n_folds, shuffle=True, random_state=42)
        fold = 1
        for train, test in kf.split(X):
            print ('Training on cross validation set ', fold )

            train_X = np.array(X)[train]
            test_X = np.array(X)[test]
            train_y = np.array(Y)[train]
            test_y = np.array(Y)[test]
            print('Training size: ', len(train_y))
            print('Test size: ', len(test_y))

            labeled_features = list(zip(train_X, train_y))
            #print(labeled_features[0])
            #print(type(train_X[0]))
            model = SklearnClassifier(MultinomialNB()).train(labeled_features)            
            predicted = model.classify_many(test_X)
            fold += 1
           
        print('Confusion matrix =', confusion_matrix(test_y, predicted))
        print('Precision score =', precision_score(predicted, test_y, average=None))
        print('Recall score =', recall_score(predicted, test_y, average=None))
        print('Accuracy score =', accuracy_score(predicted, test_y))
        print('Training score =', f1_score(predicted, test_y, average=None))

        return model