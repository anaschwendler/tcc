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

## Similarity mesures

## Centrality

## Evaluation strategies

## ROUGE

## CST-News

## Tasks

- [x] attempt to adjust the lexRank algorithm to concept version
- [ ] write about the project, to clear things
- [ ] collect results for our algorithm to one document
- [ ] collect results for our algorithm for all CST documents.


