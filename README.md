# Graph-based conceptual centrality as salience in extractive text summarization

## Automatic text summarization (AS)

Automatic Text Summarization (AS) is a Natural Language Processing (NLP) task that aims to reduce the amount of text into a shorter version while preserving the core information content \cite{nenkova2011automatic}.
This kind of shorter text is useful for many daily activities, since the amount of information is growing, and we cannot get all the news by reading all the texts that are being published in one day.
This work in progress presents a proposal aimed to minimize problems related to AS, since some extractive techniques are not totally prepared to handle with some issues, such as typos, synonyms and other orthographic variations.

## Vector Space Model
Related work in this area relies on the Vector Space Model (VSM), to represent the content and relationship of texts. This representation implies a mesure of similarity that can be based on the cosine similarity. However this similarity in VSM can be influenced by problems derived from NLP.
In order to minimize this problems, our research uses concepts, instead of words to describe the content of summaries.

## Summarization
Is the process of reducing a textual document in order to create a summary that retains the most important points of the original document. **Summary** is the result of the summarization process.

* Purpose relation
    * Indicative summary: this kind of summary only indicates which part of the texts should be read by the user.
    * Informative summary: this summary replaces the original document

* Summary and original text relation
    * Extractive summary: it selects a couple of relevant sentences, based on statiscal analysis.
    * Abstractive summary: attempts to understand the central concepts from the document, creating a totally new text.

* Input document relation
    * Single document: the sentences are extract from one only text.
    * Multi-document: the information can be digested from multiple text sources into one single document.
    
* Language relation
    * Monolingual: the output language is the same as the input text language.
    * Multilingual: the output language can be the same as the input language, but it can work in more than one language.
    * Cross-lingual: it get a source text in a particular language and built the summary in another language.
    
## Model and representation
Extractive summarization relies on graph representation of documents for computing relative importance (salience) of its textual units[Erkan and Radev 2004]. That representation consists in sentences being representated as nodes and its similarity are represented by edges. The salient nodes represent the most representative sentences, which should be included in the final summary.
- There are two points that should be considered in the definition of centrality.
    - How to define the similarity between two sentences;
    - How to compute the overall (global) centrality of a sentence

## Similarity mesures
Answering about the points above, the similarity between two sentences can be defined as the amount of information in commom that they share. For example, to define the similarity between two sentences using the **cosine between two vectors**, defined by the value of the corresponding dimension of the vector representation of the sentence (number of ocurrence of the word in the sentence * idf of the word) can be affected by NLP problems, as we mentioned before.

**Concepts** represent real world attributes and they help understanding ideas and ideologies present in texts. Concepts are not in the same level of terms of words, so it can minimize the vocabulary problem, and the effort necessary to extract useful information.
The first thing to do is to identify or extract concepts from documents (in our case, sentences). To do it is sugested by [Loh et al. 2000] applying an automatic **categorization** task. 
- This categorization is guided by a set of *rules* that describe how a concept should be identified.
- These rules include cue *terms* that once found in a document may indicate the presence of concept.
- The terms may include synonyms, lexical variations and derivations, and semantic related words.
- Each term has an weight associated that correspond to the relative importance of this term from 0 (irrelevant) to 1 (relevant). It can be manually assigned or can use learning process.
Once the concepts are identified, we can identify the similarity among the concepts of each sentence. To do this we calculate the grade of similarity (gs) between two vectors (v1, v2).

## Evaluation strategies
A good summary contains
- Coverage - Contain the main topics of the original document.
- High diversity - Keep the redundancy to a minimum.
- High coherence - Have smooth connection among sentences.
There are many methods to perform intrinsec evaluation, but in our work we will be using the **[ROUGE](http://kavita-ganesan.com/rouge-howto)** method, which is inspired by the success of the BLUE evaluation, using n-gram overlaps as the basis of mesure. It will be more explained in the next section.

## ROUGE

## CST-News

## Tasks

- [x] attempt to adjust the lexRank algorithm to concept version
- [ ] write about the project, to clear things
- [ ] collect results for our algorithm to one document
- [ ] collect results for our algorithm for all CST documents.


