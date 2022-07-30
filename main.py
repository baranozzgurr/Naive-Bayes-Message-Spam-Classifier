import sys
#import pandas
import collections
import copy
import os
import math
#import sklearn

import re

train_data = dict()
stopword_training = dict()
test_data = dict()
stopword_test = dict()


stopWords = [] # we use the long one
data_set = ["ham","spam"]
prob = dict()
stopword_prob= dict()
classification = dict()
stp_classification = dict()



##we store ham and spam and then predicts them
class Storing:
    count_dic={}
    msg_txt=""

    
    naive=""
    trained_naive=""

    
    def __init__(self,msg_txt,ct,naive):
        self.msg_txt=msg_txt
        self.count_dic = ct
        self.naive = naive

    def MessageText(self):
        return self.msg_txt

    def Word_Count(self):
        return self.count_dic

    def OriginData(self):
        return self.naive

    def TrainedData(self):
        return self.trained_naive

    def Trained_Naive_Bayes(self,prediction):
        self.trained_naive =prediction


def Counts(words):
    wordCount=collections.Counter(re.findall(r'\w+',words))
    return dict(wordCount)


def Messages(temp_dictionary,HorS,classifier):
    for message in os.listdir(HorS):
        dictionary_join = os.path.join(HorS,message)
        if os.path.isfile(dictionary_join):
            with open(dictionary_join,'r') as message_file:
                message_text = message_file.read()
                temp_dictionary.update({dictionary_join: Storing(message_text,Counts(message_text),classifier)})

def stopWords():
    stop_wrd_list = []
    with open('stopWords.txt', 'r') as stp_file:
        stop_wrd_list=(stp_file.read().splitlines())
    return stop_wrd_list

def Filter_StopWords(stop,text_data):
    filtered_data= copy.deepcopy(text_data)
    for i in stop:
        for i2 in filtered_data:
            if i in filtered_data[i2].Word_Count():
                del filtered_data[i2].Word_Count()[i]
    return filtered_data

#list of text words
def Text_Words(text_data):
    textt = ""
    temp_list=[]
    for i in text_data:
        textt+=text_data[i].MessageText()
    for i2 in Counts(textt):
        temp_list.append(i2)
    return temp_list









def multinomial_Naive_Bayes(train,classifier,prob):
    #we use multinomial naive bayes
    temp_list= Text_Words(train)
    t = len(train)
    for x in data_set:
        temp=0.0
        text_temp = ""
        for i in train:
            if train[i].OriginData()==x:
                temp=temp+1
                text_temp+=train[i].MessageText()
        classifier[x] = float(temp) / float(t)
        temp_count = Counts(text_temp)
        for j in temp_list:
            if j in temp_count:
                prob.update({j + "_" + x: (float((temp_count[j] + 1.0)) / float((len(text_temp)+len(temp_count))))})
            else:
                prob.update({j + "_" + x: (float(1.0) / float((len(text_temp)+len(temp_count))))})



def Naive_Bayes(temp_data,classifierr,prob):
    accuracy={}
    for i in data_set:
        accuracy[i]=math.log10(float(classifierr[i]))
        for j in temp_data.Word_Count():
            if (j+ "_" +i) in prob:
                accuracy[i]=accuracy[i]+float(math.log10(prob[j+ "_" +i]))
    if accuracy["ham"] > accuracy["spam"]:
        return "ham"
    else:
        return "spam"








def main(train_spam,train_ham,test_spam,test_ham):
    Messages(train_data,train_ham,data_set[0])
    Messages(train_data,train_spam,data_set[1])
    Messages(test_data,test_ham,data_set[0])
    Messages(test_data,test_spam,data_set[1])

    
    stop_filter=stopWords() #filtering stop words(long one)

    stopword_training = Filter_StopWords(stop_filter,train_data)
    stopword_test = Filter_StopWords(stop_filter,test_data)

    
    multinomial_Naive_Bayes(train_data, classification, prob) #using naive baives for both with stopwords and without stopwords
    multinomial_Naive_Bayes(stopword_training, stp_classification, stp_classification)

    
    temp_prediction= 0
    for i in test_data:
        test_data[i].Trained_Naive_Bayes(Naive_Bayes(test_data[i], classification, prob))
        if test_data[i].TrainedData() == test_data[i].OriginData():
            temp_prediction=temp_prediction+1 #increase

    
    filtered_prediction=0 #with filtering stopwords
    for i in stopword_test:
        stopword_test[i].Trained_Naive_Bayes(Naive_Bayes(stopword_test[i], stp_classification,
                                                                stp_classification))
        if stopword_test[i].TrainedData() == stopword_test[i].OriginData():
            filtered_prediction=filtered_prediction+1

    print "True predictions without filtering stop words:%d/%d"%(temp_prediction,len(test_data))
    print "Test Data Accuracy without filtering stop words(In percent):%.4f"%(100.0*float(temp_prediction)/float(len(test_data)))
    print "True Predictions with filtering stop words:%d/%d"%(filtered_prediction,len(stopword_test))
    print "Test DataAccuracy with filtering stop words(In percent):%.4f"%(100.0*float(filtered_prediction)/float(len(stopword_test)))


main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]) # we are compiling our code with command line
