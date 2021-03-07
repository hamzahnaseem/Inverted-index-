import glob
import string
from abc import ABC
from html.parser import HTMLParser
import math
from nltk import word_tokenize
from nltk import PorterStemmer


class MyHTMLParser(HTMLParser, ABC):
    temp = "a"
    temp2 = "b"
    def handle_data(self, data):
        self.temp += data
        return self.temp

path = 'C:/Users/Hp/source/repos/PythonApplication1/PythonApplication1/corpus/*'
files = glob.glob(path)
index = 1         #index of term in document
index_docid = 0   #document ids
index_termid = 0

hash_map = {}
key_hash_map = 0
term_doc_list = []
stemmedlist = []
total_word_count = []
dictionary = []
doc_ids = []
list_of_doc = []
doc_index_term = []
documents_data = []  #containing data for each document e.g data for document one is one first index
documents_data_index = 0
for name in files:
    list_of_doc.clear()
  #  print(name, '/', index)
    docfile = open("docids.txt", "a+")
    docids = docfile.write(name[70:99] + "\t" + str(index_docid) + "\n")
    docfile.close()

    File = open(name, errors='ignore')
    contents = File.read()

    parser = MyHTMLParser()
    parser.feed(contents)

    tokenized_aray = word_tokenize(parser.temp.lower())

    thestoplist = open('stoplist.txt', 'r')
    thestopwordaray = thestoplist.read()

    after_stop_word = [word for word in tokenized_aray if word not in thestopwordaray]
    #print(after_stop_word)
    thestoplist.close()

    ps = PorterStemmer()

    after_stop_word = [''.join(c for c in s if c not in string.punctuation) for s in after_stop_word]
    after_stop_word = [s for s in after_stop_word if s]
    after_stop_word = [x for x in after_stop_word if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())]
    after_stop_word = [i for i in after_stop_word if len(i) > 1]

    index = 1

    for a in after_stop_word:
        afterstem = ps.stem(a)
        stemmedlist.append(afterstem)

        if afterstem not in dictionary:
            dictionary.append(afterstem)
            index_termid = dictionary.index(afterstem)
            termfile = open("termids.txt", "a+", errors='ignore')
            termids = termfile.write(str(dictionary[index_termid]) + "\t" + str(index_termid) + "\n")
            termfile.close()
            hash_map[dictionary.index(afterstem)] = [(index_docid, index)]
        else:
            hash_map[dictionary.index(afterstem)].append((index_docid, index))

        term_doc_list.append([dictionary.index(afterstem),index_docid,index])
        index = index + 1

        #print(term_doc_list[just_temp])
        #just_temp = just_temp + 1

    documents_data.append(stemmedlist[:])
    stemmedlist.clear()




    index_docid = index_docid + 1

    #print(documents_data)

File.close()

#By sorting algorithm

term_doc_list.sort(key=lambda x: x[0])

just_temp = 0
temp = []
postings = []
count_docs = []
temp_count_docs = []
count_corpus = []
temp_count_corpus = 0
delta = 0

for this in term_doc_list:
    #print(this)
    if this[0] == just_temp + 1:
        postings.append(temp[:])
        temp.clear()
        count_docs.append(len(temp_count_docs))
        temp_count_docs.clear()
        count_corpus.append(temp_count_corpus)
        temp_count_corpus = 0
        delta = 0


    if this[1] not in temp_count_docs:
        temp_count_docs.append(this[1])

    temp_count_corpus = temp_count_corpus + 1

    temp.append([this[1] - delta, this[2]])
    just_temp = this[0]
    delta = this[1]

postings.append(temp[:])
temp.clear()
count_docs.append(len(temp_count_docs))
temp_count_docs.clear()
count_corpus.append(temp_count_corpus)
temp_count_corpus = 0


#for this in postings:
#    print(postings.index(this))
#    print(this)



#for this in count_docs:
    #print(count_docs.index(this))
    #print(this)

#for this in count_corpus:
    #print(this)


#for a in range(len(dictionary)):
    #print(str(a) + "\t" + str(count_corpus[a]) + "\t" + str(count_docs[a]) + "\t" + str(postings[a]) + "\t" "\n")


sorting = open("with_sorting.txt", "a+", errors='ignore')
for a in range(len(dictionary)):
    any = sorting.write(str(a) + "\t" + str(count_corpus[a]) + "\t" + str(count_docs[a]) + "\t" + str(postings[a]) + "\t" "\n")

sorting.close()

#hashmap
#print(hash_map)


h = open("with_hash_map.txt", "a+", errors='ignore')
for a in range(len(dictionary)):
    any1 = h.write(str(a) + "\t" + str(count_corpus[a]) + "\t" + str(count_docs[a]) + "\t" + str(hash_map[a]) + "\t" "\n")

h.close()

#reading
read = 'http'
term_data = 0
found_id = 0
f = open("termids.txt", "r")

for a in f:
    term_data = a.split()
    if read in term_data:
        found_id = term_data[1]
        print(found_id)

f.close()

inverted = open("with_hash_map.txt", "r")
for a in inverted:
    term_data = a.split()
    if found_id == term_data[0]:
        print(found_id , term_data[1] , term_data[2])


