#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File           :   prepro_flickr_label.py
@Desciption     :   None
@Modify Time      @Author    @Version 
------------      -------    --------  
2019/8/23 14:42   Daic       1.0        
'''
from __future__ import unicode_literals
import pandas as pd
import json
import argparse
import spacy
import re
bad_words=['.',',','!','?','$',';',':','\"','\'','(',')','[',']']
def load_token_file(token_pth):
    return pd.read_csv (token_pth, sep='\t', header=None,
                            names=['image', 'caption'])
def get_id_and_num(str):
    pos = str.index('#')
    return str[:pos],int(str[pos+1:])

def process_caption(str):
    return re.sub("[\.,]+", " ".decode("utf8"),str).lower()

def get_tokens(str,nlp):
    tokens=[]
    nlp_str=nlp(str.decode('unicode-escape'))
    for token in nlp_str:
        if token.text not in bad_words:
            tokens.append(token.text)
    return tokens

def main(params):
    try:
        nlp =  spacy.load("en_core_web_sm")
    except:
        print('can not load en_core_web_sm model')
        nlp = spacy.load('en_core_web_lg')

    pd_file = load_token_file(params['token_file_path'])
    cap_num = len(pd_file['image'])

    #get all captions:
    captions={}
    print("sorting the dataset...")
    for i in range(cap_num):
        img_name,sent_pos=get_id_and_num(pd_file['image'][i])
        if sent_pos == 0:
            captions[img_name]=[]
            captions[img_name].append(pd_file['caption'][i].lower())
        else:
            captions[img_name].append(pd_file['caption'][i].lower())

    flickr_dataset = {'images':[],'dataset':'flickr'}
    print("changing to coco's template...")
    counting=0
    for img_name in captions.keys():
        tmp={'imgid':int(img_name[:-4]),
             'filename':img_name,
             'split':None,
             'sentences':[],
             'filepath':''
             }
        for i in range(len(captions[img_name])):
            sent_tmp={
                'raw':captions[img_name][i],
                'tokens':get_tokens(captions[img_name][i],nlp),
                'imgid':int(img_name[:-4])
            }
            tmp['sentences'].append(sent_tmp)
            counting+=1
            if counting%1000==0:
                print(float(counting)/cap_num)
        flickr_dataset['images'].append(tmp)
    print('saving json file...')
    json.dump(flickr_dataset,open(params['output_json'],'w'))

if __name__ == "__main__":

  parser = argparse.ArgumentParser()

  parser.add_argument('--token_file_path',  default='./results_20130124.token',
                      help='input token file to process into json')
  parser.add_argument('--output_json',  default='./flickr30k_dataset.json',
                      help='output json file')
  args = parser.parse_args()
  params = vars(args) # convert to ordinary dict
  main(params)
