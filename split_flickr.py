import json
import argparse
import random
def main(params):
    if params['len_val']+params['len_test']>30000:
        raise Exception("Too much images in val and test!")

    random.seed(params['seed'])
    flickr_dataset = json.load(open(params['json_path']))
    idx = []
    for i in range(len(flickr_dataset['images'])):
        idx.append(i)
    idx_ = random.sample(idx, params['len_val']+params['len_test'])

    idx_val = idx_[:params['len_val']]
    idx_test = idx_[params['len_val']+1:]
    print('spliting...')
    for i in range(len(flickr_dataset['images'])):
        if i in idx_val:
            flickr_dataset['images'][i]['split']='val'
        elif i in idx_test:
            flickr_dataset['images'][i]['split'] = 'test'
        else:
            flickr_dataset['images'][i]['split'] = 'train'

    print('saving at %s'%(params['json_path'][:-5]+'_split.json'))
    json.dump(flickr_dataset,open(params['json_path'][:-5]+'_split.json','w'))

if __name__ == "__main__":

  parser = argparse.ArgumentParser()

  parser.add_argument('--seed',  default=123)
  parser.add_argument('--json_path', default='./flickr30k_dataset.json')
  parser.add_argument('--len_val',  default=1000)
  parser.add_argument('--len_test', default=1000)
  args = parser.parse_args()
  params = vars(args) # convert to ordinary dict
  main(params)