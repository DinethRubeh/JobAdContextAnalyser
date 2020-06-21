import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm

import config
import pandas as pd
from job_context import text_pre_process

nlp = en_core_web_sm.load()

# load test data
test_df = pd.read_json(config.ad_details_path + 'test_details.json', orient='records')

# remove new line string
test_df["description"] = test_df.description.str.replace('\n',' ', regex=True)

# merge position and description (textual data)
# test_df['text'] = test_df['position'] + test_df['description']
test_df['text'] = test_df['description']
# apply text pre procesing to each row
test_df['text'] = test_df['text'].apply(lambda x: text_pre_process(x))

# test df text column to list
test_docs = test_df['text'].tolist()

# get sample test document
test_doc = test_docs[1]

print(test_doc)
print("========?==========")

doc = nlp(test_doc)
print([(X, X.ent_iob_, X.ent_type_) for X in doc])
# ([(X, X.ent_iob_, X.ent_type_) for X in doc])