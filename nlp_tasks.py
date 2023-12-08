#!/usr/bin/env python3
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""Sample code for Comp24011 BM25 lab solution

NB: The default code in non-functional; it simply avoids type errors
"""

__author__ = "USERNAME"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# we recommend you consider these Python modules while developing your code
import math
import re
import string
import sys

from nlp_tasks_base import NLPTasksBase

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class NLPTasks(NLPTasksBase):
    def __init__(self, *params):
        """Initialise instance by passing arguments to super class"""
        super().__init__(*params)

    def preprocess(self, texts):
        """Implements text preprocessing

        :param texts: text lines
        :type texts:  list

        :return: preprocessed lines
        :rtype:  list[str]
        """
        translator = str.maketrans(string.punctuation, " " * len(string.punctuation))
        removed_punc = [text.lower().strip().translate(translator) for text in texts]
        processed_list = removed_punc
        if self.stopwords_list:
          processed_list = [' '.join([word for word in text.split() if word.lower() not in self.stopwords_list]) for text in removed_punc]
          stemmed_list = processed_list
        if self.stemmer:
          stemmed_list = [' '.join([self.stemmer.stemWord(word) for word in text.split()]) for text in processed_list]
        return stemmed_list

    def calc_IDF(self, term):
        """Calculates Inverse Document Frequency (IDF)
        of given term in preprocessed corpus

        :param term: given term
        :type term:  string

        :return: IDF
        :rtype:  float
        """
        count = 0.0
        total_doc = len(self.preprocessed_corpus)
    
        for sentence in self.preprocessed_corpus:
          if ((term) in sentence.split()):
            count += 1

        idf = math.log10( (total_doc - count + 0.5) / (count + 0.5) )

        return idf

    def calc_BM25_score(self, index):
        """Calculates BM25 score
        for preprocessed question in preprocessed document

        :param index: index of document in preprocessed corpus
        :type index:  int

        :return: BM25
        :rtype:  float
        """
        count = 0.0
        split_corpus = [doc.split() for doc in self.preprocessed_corpus]
        num_of_doc = len(split_corpus)
        avg_len = 0.0
        for doc in split_corpus:
          avg_len += len(doc)
        
        avg_len = avg_len / num_of_doc
        split_question = self.preprocessed_question.split()
        split_doc = self.preprocessed_corpus[index].split()
        doc_len = len(split_doc)
        for word in split_question:
          idf = self.calc_IDF(word)
          tf = split_doc.count(word)
         
          count = count + (idf * ((tf*3)/(tf + 2*(0.25 + 0.75*(doc_len/avg_len)))))
          
        
        return count

    def find_top_matches(self, n):
        """Finds the top scoring documents
        for preprocessed question in corpus

        :param n: number of documents to find
        :type n:  int

        :return: top scoring original documents
        :rtype:  list[str]
        """
        results = [(i,self.calc_BM25_score(i)) for i in range(len(self.preprocessed_corpus))]

        sorted_results = sorted((results), key=lambda x: x[1], reverse=True)
        
        matches = []
        for result in sorted_results:
          matches.append(self.original_corpus[result[0]])
      
        matches = matches[:n]
        return matches

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    import run_BM25
    run_BM25.main(sys.argv[1:])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# vim:set et sw=4 ts=4:
