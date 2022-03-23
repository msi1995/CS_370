#### TO RUN ####

Extract contents into dir on flip. I am assuming you guys will use your own .txt files so I didn't include any other than the dictionary.

type: virtualenv hw2                   ## wait for complete
type: source hw2/bin/activate          ## you should see a (hw2) venv on the far left of terminal
type: pip install bitarray             ## needed package
type: pip install mmh3                 ## needed package
type: python lloyddo_bloom_filter.py -d dictionary.txt -i input.txt -o3 output3.txt -o5 output5.txt            ## runs prog


output3.txt and output5.txt should appear once program finishes in a few seconds. type deactivate to leave venv if needed. done