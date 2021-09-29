import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier
import joblib
from sklearn import datasets

dataset = datasets.load_iris()

X = dataset.data
y = dataset.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, shuffle=True)

classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)
prediction=classifier.predict(X_test)

print("Confusion Matrix:")
print(confusion_matrix(y_test, prediction))

joblib.dump(classifier, 'classifier.joblib')