import os
import config
import pandas as pd

# load full_job_details csv
job_details_df = pd.read_csv(config.ad_details_path + 'job_full_details.csv')

def get_jobs_for_key_word(key_word):

    # key_word = "php"
    # boolean mask with key word availability
    key_word_mask = job_details_df['description'].str.contains(key_word, na=False)

    # apply key_word_mask
    filtered_df = job_details_df[key_word_mask]

    # drop description column
    filtered_df.drop(['description'], axis=1, inplace=True)
    
    # convert to json
    filtered_json = filtered_df.to_dict('records')

    return filtered_json

def main():
    print(get_jobs_for_key_word("python"))

if __name__ == "__main__":
    main()