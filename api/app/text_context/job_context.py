import os
import re

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

import config

# some mild pre-processing
def text_pre_process(txt):

    # lowercase
    txt = txt.lower()
    # remove newline
    txt = re.sub("(\n+)","",txt)
    # replace brackets ( (),[] ) with whitespace
    txt = re.sub(r"[\[,\],\(,\)]"," ",txt)
    # remove mutiple whitespace
    mod_txt = ' '.join(txt.split())

    return mod_txt

# helper functions
def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
 
def extract_topn_from_vector(feature_names, sorted_items, topn=25):
    """get the feature names and tf-idf score of top n items"""
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]
 
    score_vals = []
    feature_vals = []
    
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])
 
    #create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results

def job_keywords():

    # load training json
    details_df = pd.read_json(config.ad_details_path + 'details.json', orient='records')

    # merge position and description (textual data)
    details_df['text'] = details_df['position'] + details_df['description']
    # apply text pre procesing to each row
    details_df['text'] = details_df['text'].apply(lambda x: text_pre_process(x))

    # text column as a list
    docs = details_df['text'].tolist()


    # create a vocabulary
    # max_df = document frequency of words, eliminate stop words
    cv = CountVectorizer(max_df=0.8, stop_words='english')

    # count vectorizer sparse matrix
    word_count_vec = cv.fit_transform(docs)
    # total word count
    print(word_count_vec.shape[1])

    # vocab word count
    print(len(list(cv.vocabulary_.keys())))

    # compute idf
    tfidf_transformer = TfidfTransformer(smooth_idf=True,use_idf=True)
    tfidf_transformer.fit(word_count_vec)

    return cv, tfidf_transformer

def test_keywords(count_vectorizor,tfidf_transformer):

    # load test data
    test_df = pd.read_json(config.ad_details_path + 'test_details.json', orient='records')

    # remove new line string
    test_df["description"] = test_df.description.str.replace('\n',' ', regex=True)
    print(test_df.head(5))

    # merge position and description (textual data)
    test_df['text'] = test_df['position'] + test_df['description']
    # apply text pre procesing to each row
    test_df['text'] = test_df['text'].apply(lambda x: text_pre_process(x))

    # test df text column to list
    test_docs = test_df['text'].tolist()

    # index to feature names mapping
    feature_names = count_vectorizor.get_feature_names()

    # get sample test document
    test_doc = test_docs[2]

    test_doc_vec = count_vectorizor.transform([test_doc])

    # get tf_idf for the selected test doc
    req_tf_idf_vec = tfidf_transformer.transform(test_doc_vec)

    sorted_items = sort_coo(req_tf_idf_vec.tocoo())

    keywords = extract_topn_from_vector(feature_names,sorted_items,50)

    print("\n======Doc========")
    print(test_doc)
    print("\n======Keywords========")
    for k in keywords:
        print(k,keywords[k])

def main():
    cv, tfidf = job_keywords()
    print(test_keywords(cv,tfidf))
    # print(text_pre_process(""))

if __name__ == "__main__":
    main()




