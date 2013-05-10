INFO 290 Final Project: Predicting Star Ratings from Reviews
================

My final project for INFO 290.

My final report and presentation is located in docs/

A little warning before you download this repo, it's somewhat large (~3 gigs).

### PREREQUISITES
If you want to run the code, you must download a few packages for python first.
You will need scipy (version 0.11), numpy (version 1.7.0), nltk (version 2.0.4), and sklearn (version 0.13.1). The version numbers here are important because they sometimes break if you download different versions.
I ran this on Python 2.7 with Windows 7 64bit.

### CODE
The classifiers are programmed to train one classifier per sub-dataset (either restricted or not, switched by the bool RESTRICT_TO_RESTAURANTS at the top of each classifier). It will save the classifier
and use it to predict 100 test cases. It will output a log consisting the prediction results.

My naive bayes and random forest classifiers are located in the root directory (nbClassifier.py and treeClassifier.py).
You can run them with `python nbClassifier.py` and `python treeClassifier.py`.
treeClassifier.py is by default the Random Forest classifier. You can change the USE_TREE boolean to true if you want only the Decision Tree classifier.

My svm related code is located in libsvm-3.17/python/
In there, svmStarClassifier.py is my svm classifier. Again, you can run it with `python svmStarClassifier.py`. It will produce models stored in infoProject/models/
combinedClassifier.py is my classifier that uses DecisionTree, NaiveBayes and SVM classifiers. It requires the saved models of each of these classifiers. I configured it to work only on the classifier versions that performed best: Naive Baye's 10,000 unigram model, Tree's 100 unigram model, and SVM's 10,000 unigram model.

My dataset creation code is in libsvm-3.17/python/infoProject/
generateDataSets.py generates all the sub-datasets I refer to in my report. They are produced inside data/. It also produces csvs for each set of test cases. These csvs 
are organized as test_case_id, num_stars, text. I use this to figure out the reviews the classifier logs refer to in their predictions (the logs are structured like: test_case_id, match/mismatch). 
generateGramStats.py produces the csv files you see in this directory. They just contain the n-gram counts of the 10,000 reviews used in my datasets.
Generation of my datasets requires that the businesses.json file be created. This is done in the getBusinesses.py file.

Finally, the finished results can be seen in the root directory. finalClassifier.py uses the saved Naive Bayes model on 10,000 unigram reviews and provides an interactive user interface for detection.
Run it like the others, `python finalClassifier.py`. This requires generateDataSets.py and nbClassifier.py to have been run before in order to generate the symbol table and model.