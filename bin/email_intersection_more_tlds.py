
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
emails = ''
mem_MB = 2000


def extract_emails(top_tlds=None, colnum=1):
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
    tlds = set(top_tlds)
    email_regex = re.compile('[a-zA-Z0-9-.!#$%&*+-/=?^_`{|}~]+@[a-zA-Z0-9-.]+(' + '|'.join(tlds) + ')')
    emails = ''
    with open('/home/hobs/Downloads/dmps/aminno_member_email.csv') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            em = email_regex.search(row[colnum])
            if em:
                emails += em.group().replace(',', '\n') + '\n'
            if len(emails) > mem_MB * 1000000:
                break
            if not (i % 100000):
                print("{}M emails read".format(i / 1000000.))
    return emails


emails = extract_emails()
with open('/home/hobs/Downloads/dmps/emails3gb.txt', 'w') as f:
    f.write(emails)
# print(emails[:100])
del emails
emails = pd.DataFrame.from_csv('/home/hobs/Downloads/dmps/emails3gb.txt').index
intersection = []
candidates = pd.DataFrame.from_csv('../data/public.raw_candidate_filings.csv')  # id_nmbr
candidates = set(candidates['email'].unique())
for i, em in enumerate(candidates):
    if str(em).lower().strip() in emails:
        intersection += [em]
        print('{}'.format(em))
    if not i * 100:
        print(i)
print(intersection)
