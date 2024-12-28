import os
import re

class Tokenizer(object):

    def __init__(self):
        try:
            fname = 'verdict.txt'
            current_dir_path = os.path.dirname(os.path.realpath(__file__))
            
            # Reading the file from the current directory
            with open(current_dir_path+'/'+fname) as raw_file:
                raw_text = raw_file.read()

                pre_processed_text = re.split(r'([,.:;?_!"()\']|--|\s)', raw_text)
                pre_processed_text = [item.strip() for item in pre_processed_text if item.strip()]
                
                all_words = sorted(set(pre_processed_text))
                all_words.extend(['<|endoftext>|', '<|unknow|>'])
                vocabulary = {token:integer  for integer, token in enumerate(all_words)}
            
            self.str_to_int = vocabulary
            self.int_to_str = {i:s for s, i in vocabulary.items()}

        except IOError:
            print("OS error occured trying to open the file {0}".format(fname))

        except Exception as e:
            print("Unexpected error opening {0} is {1}".format(fname,repr(e)))

    def encode(self, text):
        """Ecoding the text """
        pre_processed = re.split(r'([,.:;?_"()\']|--|\s)', text)
        pre_processed = [item.strip() for item in pre_processed if item.strip()]

        # adding the unknown if the words are not present
        # in 'pre_processed' text
        pre_processed =[
            item if item in self.str_to_int else '<|unknow|>' for item in pre_processed
        ]
        ids = [self.str_to_int[token] for token in pre_processed]
        return ids
    

    def decode(self, ids):
        text = " ".join([self.int_to_str[id] for id in ids])

        #Replace the space befor the specified punctuation
        text = re.sub(r'\s+([,.:;?_"()\'])',r'\1', text)

        return text

tokenizer = Tokenizer()
sentence = "How are you?"
ids = tokenizer.encode(sentence)

print("Tokenized:{}".format(ids))
decoded_text = tokenizer.decode(ids)
print("Detokenized:{}".format(decoded_text))
