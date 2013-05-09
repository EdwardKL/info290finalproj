INFO 290 Final Project: Predicting Star Ratings from Reviews
================

My final project for INFO 290.

My final report and presentation is located in docs/

### PREREQUISITES
If you want to run the code, you must download a few packages for python first.
You will need scipy (version 0.11), numpy (version 1.7.0), nltk (version 2.0.4), and sklearn (version 0.13.1). The version numbers here are important because they sometimes break if you download different versions.
I ran this on Python 2.7 with Windows 7 64bit.

### CODE
My naive bayes and random forest classifiers are located in the root directory (nbClassifier.py and treeClassifier.py).
You can run them with `python nbClassifier.py`.
treeClassifier.py is by default the Random Forest classifier. You can change the USE_TREE boolean to true if you want only the Decision Tree classifier.
These classifiers output a pickle of the learned model and a log consisting of the prediction results.

My svm related code is located in libsvm-3.17/python/
In there, svmStarClassifier.py is my svm classifier. Again, you can run it with `python svmStarClassifier.py`. It will produce models stored in infoProject/models/
finalClassifier.py is my classifier that uses DecisionTree, NaiveBayes and SVM classifiers. It requires the saved models of each of these classifiers. I configured it to work only on the classifier versions that performed best: Naive Baye's 10,000 unigram model, Tree's 100 unigram model, and SVM's 10,000 unigram model.

My dataset creation code is in libsvm-3.17/python/infoProject/
generateDataSets.py generates all the sub-datasets I refer to in my report. They are produced inside data/.
generateGramStats.py produces the csv files you see in this directory. They just contain the n-gram counts of the 10,000 reviews used in my datasets.
Generation of my datasets requires that the businesses.json file be created. This is done in the getBusinesses.py file.