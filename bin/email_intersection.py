import re
import pandas as pd
np = pd.np
np.norm = np.linalg.norm
from datetime import datetime, date

import matplotlib
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import train_test_split


# # to get some interesting e-mails to colate with politicians
# # sudo apt-get install pv gzip
# # curl -O --anyauth https://raw.githubusercontent.com/jamesmishra/mysqldump-to-csv/master/mysqldump_to_csv.py
# # chmod +x mysqldump_to_csv.py
# # pv aminno_member_email.dump.gz | zcat | python2 mysqldump_to_csv.py > aminno_member_email.csv

pacs_scraped = pd.DataFrame.from_csv('public.raw_committees_scraped.csv')  # id
pacs = pd.DataFrame.from_csv('public.raw_committees.csv')  # no ID that I can find
print(pacs_scraped.info())
print(candidates.info())

df = pacs_scraped
names = df.index.values
corpus = [' '.join(str(f) for f in fields if (not isinstance(f, (float, int, datetime, date, np._int, np._float)) and not f in (None, np.nan)))
          for fields in zip(*[df[col] for col in df.columns if df[col].dtype == pd.np.dtype('O')])]
print(corpus[:3])

from collections import Counter
from itertools import chain
tf = Counter(chain(*[doc.split() for doc in corpus]))
print(tf.most_common(10))

# so we need to exclude dates and numbers and "nan"s (we'll let nltk and sklearn handle stop words)
bad_words = set(['nan'])
regex = re.compile(r'^[a-zA-Z][-_a-zA-Z]*[a-zA-Z0-9][!.?]*$')
corpus = [' '.join(token for token in doc.split() if regex.match(token) and token not in bad_words)
          for doc in corpus]

vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), stop_words='english')
# rows should be documents, columns should be "words"
vectors = vectorizer.fit(corpus)
tfidf = vectors.transform(corpus)
tfidf_df = pd.DataFrame(tfidf.todense(), index=names)
print(dir(tfidf))
cov = tfidf * tfidf.T
cov_df = pd.DataFrame(cov.todense(), columns=names, index=names)

# to get some interesting e-mails to colate with politicians
# sudo apt-get install pv gzip
# curl -O --anyauth https://raw.githubusercontent.com/jamesmishra/mysqldump-to-csv/master/mysqldump_to_csv.py
# chmod +x mysqldump_to_csv.py
# pv aminno_member_email.dump.gz | zcat | python2 mysqldump_to_csv.py > aminno_member_email.csv

import pandas as pd
import csv
import os
import re
home = os.getenv('HOME')
downloads = os.path.join(home, 'Downloads', 'dmps')
extracted_emails = os.path.join(downloads, 'emails3gb.txt')
mem_MB = 2000
top_tlds = top_tlds or {
    '.com': ('Commercial', 4860000000),
        '.org': ('Noncomercial', 1950000000),
    '.edu': ('US accredited postsecondary institutions', 1550000000),
    '.gov': ('United States Government', 1060000000),
        '.uk':  ('United Kingdom', 473000000),
        '.net': ('Network services', 206000000),
        '.ca': ('Canada', 165000000),
        '.de': ('Germany', 145000000),
        '.jp': ('Japan', 139000000),
        '.fr': ('France', 96700000),
        '.au': ('Australia', 91000000),
        '.us': ('United States', 68300000),
        '.ru': ('Russian Federation', 67900000),
        '.ch': ('Switzerland', 62100000),
        '.it': ('Italy', 55200000),
        '.nl': ('Netherlands', 45700000),
        '.se': ('Sweden', 39000000),
        '.no': ('Norway', 32300000),
        '.es': ('Spain', 31000000),
        '.mil': ('US Military', 28400000)
        }


def extract_emails(top_tlds=top_tlds, colnum=1,
                   dest=os.path.join(downloads, extracted_emails)):
tlds = set(top_tlds)
    email_regex = re.compile('[a-zA-Z0-9-.!#$%&*+-/=?^_`{|}~]+@[a-zA-Z0-9-.]+(' + '|'.join(tlds) + ')')
    emails = ''
    with open(os.path.join(downloads, 'aminno_member_email.csv')) as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
            em = email_regex.search(row[colnum])
        if em:
                emails += em.group().replace(',', '\n') + '\n'
            if len(emails) > mem_MB * 1000000:
            break
        if not (i % 100000):
                print("{}M emails read".format(i / 1000000.))
    with open(dest, 'w') as f:
    f.write(emails)
    # return emails
extract_emails()


# emails = pd.Series(emails.split('\n'))

# print(emails[:100])
emails = pd.DataFrame.from_csv(extracted_emails).index
# $ free -h
#              total       used       free     shared    buffers     cached
# Mem:          7.7G       6.4G       1.3G       139M       108M       2.6G
# -/+ buffers/cache:       3.6G       4.1G
# Swap:           0B         0B         0B
# (hackor)hobs@hplap:~/src/totalgood/webapps/hackor$  master
# $ free -h
#              total       used       free     shared    buffers     cached
# Mem:          7.7G       6.5G       1.2G       139M       108M       2.6G
# -/+ buffers/cache:       3.7G       4.0G
# Swap:           0B         0B         0B
# (hackor)hobs@hplap:~/src/totalgood/webapps/hackor$  master
# $ free -h
#              total       used       free     shared    buffers     cached
# Mem:          7.7G       7.5G       171M       132M       107M       1.8G
# -/+ buffers/cache:       5.6G       2.1G
# Swap:           0B         0B         0B
# (hackor)hobs@hplap:~/src/totalgood/webapps/hackor$  master
# $ free -h
#              total       used       free     shared    buffers     cached
# Mem:          7.7G       6.8G       937M       134M       107M       1.8G
# -/+ buffers/cache:       4.9G       2.8G
# Swap:           0B         0B         0B
# (hackor)hobs@hplap:~/src/totalgood/webapps/hackor$  master
# $ free -h
#              total       used       free     shared    buffers     cached
# Mem:          7.7G       5.1G       2.6G       134M       115M       1.9G
# -/+ buffers/cache:       3.1G       4.6G
# Swap:           0B         0B         0B

intersection = []
candidates = pd.DataFrame.from_csv(
    os.path.joint(data, 'public.raw_candidate_filings.csv')
candidates = set(candidates['email'].unique())
for i, em in enumerate(candidates):
    if str(em).lower().strip() in emails:
        intersection += [em]
        print('{}'.format(em[-10:]))
# @yahoo.com
# @yahoo.com
# @gmail.com
# ue@msn.com
# eurlaw.com
# etmail.com
# m1@msn.com
# @gmail.com

# print(intersection)
