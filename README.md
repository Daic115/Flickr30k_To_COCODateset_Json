## Flickr30k To COCO

This is a scrip to change Flickr30k token dataset into a json template as same as MSCOCO.
### Requirement: 
`spacy` Using spacy to tokenize the captions.
`pandas` Using pandas to read  `.token` file.

### Run:
`python prepro_flickr30k.py --token_file_path YOUR_FLICKR_TOKEN_FILE_PATH --output_json SAVE_PATH`
### Split:
Flickr30k has 31783 images wiht 5 captions for each.
You may need divide the dataset into train,val and test:
`python split_flickr.py --seed 123 --json_path PREVIOUS_SAVE_PATH --len_val 1000 --len_test 1000`

