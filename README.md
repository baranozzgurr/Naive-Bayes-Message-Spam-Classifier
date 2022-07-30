# Naive-Bayes-Message-Spam-Classifier
The data set is divided into two sets: training set and test set. Each set has two directories: spam and ham. All les in the spam folders are spam messages and all les in the ham folder are legitimate (non spam) messages.

The multinomial Naive Bayes algorithm for text classication described here: http://nlp.stanford.edu/IR-book/pdf/13bayes.pdf. The algorithm uses add-one laplace smoothing.
Ignore punctuation and special characters and normalize words by converting them to lower case, converting plural words to singular (i.e., \Here" and \here" are the same word, \pens" and \pen" are the same word).
After that this Naive Bayes Algorithm will improve by throwing away (i.e., ltering out) stop words such as \the" \of" and \for" from all the documents.

Compiling command is below :

python main.py train/spam train/ham test/spam test/ham

The output will be number of true predictions with and without stop words 

The output also will be test accuracy with and without stopwords
