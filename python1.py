import glob
import string
from abc import ABC
from html.parser import HTMLParser
import math
from nltk import word_tokenize
from nltk import PorterStemmer


from bs4 import BeautifulSoup


class MyHTMLParser(HTMLParser, ABC):
    temp = "a"
    temp2 = "b"

    def handle_data(self, data):
        self.temp += data
        return self.temp

index_query_id = 0
query_id = []
query_id.append(202)
query_id.append(214)
query_id.append(216)
query_id.append(221)
query_id.append(227)
query_id.append(230)
query_id.append(234)
query_id.append(243)
query_id.append(246)
query_id.append(250)

debug = 0
index = 0  # document ids
index_termid = 1
stemmedlist = []
total_word_count = []
dictionary = []
doc_ids = []
list_of_doc = []
doc_index_term = []
documents_data = []  # containing data for each document e.g data for document one is one first index
documents_data_index = 1

stemmedlist1 = []
total_word_count1 = []
dictionary1 = []
doc_ids1 = []
list_of_doc1 = []
doc_index_term1 = []

term_data = []
# f = open("TERMID.txt", "r")

f = open("docids.txt", "r")
for a in f:
    index = index + 1
f.close()
thestoplist1 = open('stoplist.txt', 'r')
stopwords = thestoplist1.read()

path2 = 'C:/Users/Hp/source/repos/PythonApplication1/topics/*'
queryFile1 = glob.glob(path2)
for queryFile in queryFile1:
    with open(queryFile) as fp:
        querySoup = BeautifulSoup(fp, 'html.parser')

        queries = querySoup.findAll("topic")
        for query in queries:
            #print('\n' + query['number'])
            queryText = query.query.get_text().split()

            # print((query.description.get_text('strip = True')).strip())

            ##  stop and stemm query
            queryText = [word for word in queryText if not word in stopwords]
            pStemmer = PorterStemmer()
            queryText = [pStemmer.stem(word) for word in queryText]
            stemmedlist1.append(queryText)

            queryfile = open("queries.txt", "a+")
            docids = queryfile.write(str(queryText) + "\t" + "\n")
            queryfile.close()

docid = 0
delta = 0
average_doc_lengths = 0
k1 = 1.2
k2 = 10
b = 0.75
size_query = len(stemmedlist1)

temp_array = []


document_freq = []
h = 0
inverted = open("term_index.txt", "r")
for a in inverted:
    term_data = a.split()

    document_freq.append(term_data[2])
inverted.close()

term_freq_in_corpus = []
size_of_corpus = 0

inverted = open("term_index.txt", "r")
for a in inverted:
    term_data = a.split()

    term_freq_in_corpus.append(term_data[1])
    size_of_corpus = size_of_corpus + int(term_data[1])

#print('size of corpus : ' + str(size_of_corpus))
#debug = input()

inverted.close()

bol = 0
document_lengths = []
dl = 0
for count in range(index):
    df = 0
    inverted = open("term_index.txt", "r")
    for a in inverted:
        term_data = a.split()
        for now in term_data:
            if ',' in now:
                docid = now.split(",")
                # print(just[0])
                if int(docid[0]) != 0 and bol == 1:
                    bol = 0

                if int(docid[0]) + delta == count + 1 or bol == 1:
                    dl = dl + 1
                    bol = 1
                else:
                    delta = delta + int(docid[0])
    document_lengths.append(dl)
    average_doc_lengths = average_doc_lengths + dl
    inverted.close()
delta = 0

average_doc_lengths = average_doc_lengths / index


bol = 0
term_id = 0
# first formula
index_query_word = 0
bm25 = []
temp_bm25 = []

for y in range(index):  # loop for document
    for h in range(size_query):  # loop for query
        index_query_word = 0

        for z in stemmedlist1[h]:
            index_query_word = index_query_word + 1
            term_id = 0
            f = open("TERMID.txt", "r")

            for a in f:
                term_data = a.split()
                if z in term_data:
                    term_id = term_data[0]
                    #print('termid : ' + str(term_id))

                    #print(z)
                    #debug = input()
            f.close()

            #print('termid : ' + str(term_id))

            # first value

            df = 0
            tf = 0
            first_value = index + 0.5
            #print('termid : ' + str(document_freq))
            #term_id = input()
            first_value = first_value / (int(document_freq[int(term_id) - 1]) + 0.5)
            first_value = math.log(first_value)
            #print('document freq : ' + document_freq[int(term_id) - 1])
            #debug = input()

            # second value
            delta = 0
            inverted = open("term_index.txt", "r")
            for a in inverted:
                term_data = a.split()
                if term_id == term_data[0]:
                    for now in term_data:
                        if ',' in now:

                            #print(' now in loop and docid : ' + docid[0])
                            #debug = input()
                            docid = now.split(",")
                            #print(just[0])
                            if int(docid[0]) != 0 and bol == 1:
                                bol = 0

                            if int(docid[0]) + delta == y or bol == 1:
                                tf = tf + 1
                                bol = 1
                            else:
                                delta = delta + int(docid[0])
            #print('term freq : ' + str(tf) )
            #debug = input()

                # print(term_data[0] + '\t' + term_data[1])
                # print(term_data)

            inverted.close()


            # find k
            k = document_lengths[y] / average_doc_lengths
            k = k * b
            k = k + (1 - b)
            k = k * k1

            second_value = 1 + k1
            second_value = second_value * tf
            second_value = second_value / (k + tf)

            # third value
            third_value = 1 + k2
            third_value = third_value / k2

            if index_query_word == 1:
                final_value = first_value * second_value * third_value

            else:
                final_value = final_value*first_value * second_value * third_value

        #print(final_value)

        temp_bm25.append([query_id[index_query_id], y, final_value])
        index_query_id = index_query_id + 1

    index_query_id = 0

temp_bm25.sort(key=lambda x: x[0])

ranking = []

#print(temp_bm25)
#debug = input()

for a in query_id:
    #print(a)
    #debug = input()
    for b in temp_bm25:
        if a == b[0]:
            ranking.append(b)
    ranking.sort(key=lambda x: x[2])
    for b in ranking:
        bm25.append(b)
    ranking.clear()

rank = index
scores = open("score1.txt", "a+")

for a in bm25:
    docids = scores.write(str(a[0]) + "\t" + str(a[1]) + "\t" + str(a[2]) + "\t " + str(rank) + "\t " + "\n")  # query number / doc number / score
    rank = rank - 1
    if rank == 0:
        rank = index

scores.close()



index_query_id = 0
#method 2

dirichlet = []
temp_dirichlet = []
final_value2 = 0
big_box = 0
small_box = 0
for y in range(index):  #loop for document
    for h in range(size_query):
        index_query_word = 0
        for z in stemmedlist1[h]:
            index_query_word = index_query_word + 1
            term_id = 0
            f = open("TERMID.txt", "r")

            for a in f:
                term_data = a.split()
                if z in term_data:
                    term_id = term_data[0]
                    # print('termid : ' + str(term_id))

                    # print(z)
                    # debug = input()
            f.close()

            # print('termid : ' + str(term_id))

            # first value
            delta = 0
            inverted = open("term_index.txt", "r")
            for a in inverted:
                term_data = a.split()
                if term_id == term_data[0]:
                    for now in term_data:
                        if ',' in now:
                            docid = now.split(",")
                            #print(just[0])
                            if int(docid[0]) != 0 and bol == 1:
                                bol = 0

                            if int(docid[0]) + delta == y or bol == 1:
                                tf = tf + 1
                                bol = 1
                            else:
                                delta = delta + int(docid[0])

            small_box = tf / document_lengths[y]

            first_value = document_lengths[y]
            first_value = first_value / (document_lengths[y] + 5)
            first_value = first_value * small_box


            #second value

            big_box = int(term_freq_in_corpus[int(term_id)]) / int(size_of_corpus)

            second_value = 5
            second_value = second_value / (document_lengths[y] + 5)
            second_value = second_value * big_box


            if index_query_word == 1:
                final_value2 = first_value + second_value

            else:
                final_value2 = final_value2 * (first_value + second_value)

            #print(final_value2)

        temp_dirichlet.append([query_id[index_query_id], y, final_value2])
        index_query_id = index_query_id + 1

    index_query_id = 0

temp_dirichlet.sort(key=lambda x: x[0])

ranking2 = []

#print(temp_dirichlet)
#debug = input()


for a in query_id:
    for b in temp_dirichlet:
        if a == b[0]:
            ranking2.append(b)
    ranking2.sort(key=lambda x: x[2])
    for b in ranking2:
        dirichlet.append(b)
    ranking2.clear()


rank = index
scores2 = open("score2.txt", "a+")

for a in dirichlet:
    docids = scores2.write(str(a[0]) + "\t" + str(a[1]) + "\t" + str(a[2]) + "\t " + str(rank) + "\t " + "\n")  # query number / doc number / score
    rank = rank - 1
    if rank == 0:
        rank = index

scores2.close()


