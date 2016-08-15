package datastructure;
import java.util.*;

public class Document{
  private String name = "";
  private BagOfWords lstWords = new BagOfWords();

  private static final double EPSILON = 0.0000000000000001;

  public Document(String filename){
    name = filename;
  }

  public void addWord(String word){
    lstWords.addWord(word);
  }

  public String getName(){
    return name;
  }

  public int nWords(){
    return lstWords.size();
  }

  public int nOccurrences(){
    return lstWords.getNumberOfOcurrences();
  }

  public String[] getWords(){
    return lstWords.getWords();
  }

  public Word[] getWordList(){
    return lstWords.getWordList();
  }

  public void setWeightType(BagOfWords.WEIGHT_TYPE type){
    lstWords.setWeightType(type);
  }

  public double similarityTo(Document d){
    // método definido em Loh et al. (2001)
    // utilizar algum padrão de projeto para permitir mudança on the fly 
    double result = 0.0d;
    double wordWeightMax = 0.0d;
    double wordWeightMin = 0.0d;
    double negationWordWeightMax = 0.0d;
    double negationWordWeightMin = 0.0d;
    double c1 = 0.0d;
    double c2 = 0.0d;
    double c3 = 0.0d;
    double c4 = 0.0d;
    double m1 = 0.0d;
    double m2 = 0.0d;
    List<Word> commonWords = new ArrayList<Word>();

    // identify the smaller and the bigger document, considering number of words
    Document min = this.nWords()<d.nWords()?this:d;
    Document max = this.nWords()>d.nWords()?this:d;

    // identify common words
    for(Word w:min.getWordList())
      if(max.containsWord(w.getWord()))
        commonWords.add(w);

    // calculates similarity
    for(Word w:commonWords){
      wordWeightMax = max.getWordWeight(w.getWord());
      wordWeightMin = min.getWordWeight(w.getWord());
      negationWordWeightMax = 1 - wordWeightMax;
      negationWordWeightMin = 1 - wordWeightMin;

      c1 = wordWeightMin == 0 ? 1 : wordWeightMax / wordWeightMin;
      c2 = wordWeightMax == 0 ? 1 : wordWeightMin / wordWeightMax;
      c3 = negationWordWeightMin == 0 ? 1 : negationWordWeightMax / negationWordWeightMin;
      c4 = negationWordWeightMax == 0 ? 1 : negationWordWeightMin / negationWordWeightMax;

      //c1 = c1 > 1 ? 1 : c1;
      //c2 = c2 > 1 ? 1 : c2;
      //c3 = c3 > 1 ? 1 : c3;
      //c4 = c4 > 1 ? 1 : c4;

      m1 = Math.min(Math.min(c1, c2), 1);
      m2 = Math.min(Math.min(c3, c4), 1);

      result+=0.5*(m1+m2);
    }

    result = result / (min.nWords() + max.nWords() - commonWords.size() + EPSILON);

    return result;
  }

  public boolean containsWord(String word){
    return lstWords.containsWord(word);
  }

  public double getWordWeight(String word){
    return lstWords.getWordWeight(word);
  }
}
