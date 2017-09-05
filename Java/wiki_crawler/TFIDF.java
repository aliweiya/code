package wiki_crawler;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

class Word {
    Word(int file_num) {
        tf = new double[file_num];
        num_in_each_file = new int[file_num];
    }

    String str;
    double[] tf;
    int[] num_in_each_file;
    double idf;
    int include_file_num;
}

class TFIDF {
    {
        words = new ArrayList<Word>();
    }
    public void tf_idf(Map<String, ArrayList<String>> map){
        //获取分类
        for(String str:map.keySet()){
            classification.add(str);
        }
        int k = 0;

        file_word_num = new int[500];
        for(Map.Entry<String, ArrayList<String>> entry:map.entrySet()){
            //一类中取20个关键词
            for(int i=0;i<entry.getValue().size();i++){
                //一条算一个文件
                ArrayList<String> array = frequency.process(entry.getValue().get(i));
                file_word_num[k*100+i] = array.size();
                for(int j=0;j<array.size();j++){
                    int index = isAlreadyExist(array.get(j));
                    if(index > -1){
                        //已存在
                        Word word = words.get(index);
                        word.include_file_num++;
                        word.num_in_each_file[k*100+i]++;
                    }else{
                        //不存在
                        Word word = new Word(500);
                        word.str = array.get(j);
                        word.num_in_each_file[k*100+i]=1;
                        word.include_file_num=1;
                        words.add(word);
                    }
                }
            }
            k++;
        }
        //计算tf和idf
        for(int i=0;i<words.size();i++){
            Word word = words.get(i);
            word.idf = Math.log(((double) 500) / ((double) word.include_file_num));
            for (int j = 0; j < 500; j++)
                word.tf[j] = ((double) word.num_in_each_file[j]) / file_word_num[j];
        }

        //写入tf_before, tfidf_before
        try {
            File tf = new File("resource/tf_before.arff");
            File tfidf = new File("resource/tfidf_before.arff");
            if(!tf.exists()){
                tf.createNewFile();
            }
            if(!tfidf.exists()){
                tfidf.createNewFile();
            }
            BufferedWriter bw_tfidf = new BufferedWriter(new FileWriter(tf, false));
            BufferedWriter bw_tf = new BufferedWriter(new FileWriter(tfidf, false));

            bw_tf.write("@relation twitter\n");
            bw_tfidf.write("@relation twitter\n");
            for(int i=0;i<words.size();i++){
                bw_tf.write("@attribute "+words.get(i).str+" numeric\n");
                bw_tfidf.write("@attribute "+words.get(i).str+" numeric\n");
            }
            bw_tf.write("@attribute twitter_class {");
            bw_tfidf.write("@attribute twitter_class {");
            for(int i=0;i<classification.size()-1;i++){
                bw_tf.write(classification.get(i)+",");
                bw_tfidf.write(classification.get(i)+",");
            }
            bw_tf.write(classification.get(classification.size()-1)+"}\n@data\n");
            bw_tfidf.write(classification.get(classification.size()-1)+"}\n@data\n");
            for(int i=0;i<500;i++){
                String str_tf = "{";
                String str_tfidf = "{";
                for(int j=0;j< words.size();j++){
                    if(words.get(j).tf[i] != 0.0)
                        str_tf=str_tf+j+" "+words.get(j).tf[i]+",";
                    if(words.get(j).tf[i] != 0.0 && words.get(j).idf != 0.0)
                        str_tfidf=str_tfidf+j+" "+words.get(j).tf[i]*words.get(j).idf+",";
                }
                if(str_tf.length()>0){
                    str_tf= str_tf+(words.size())+" "+classification.get(i/100);
                    str_tf+="}";
                    bw_tf.write(str_tf+"\n");
                }
                if(str_tfidf.length()>0){
                    str_tfidf= str_tfidf+(words.size())+" "+classification.get(i/100);
                    str_tfidf+="}";
                    bw_tfidf.write(str_tfidf+"\n");
                }
            }
            bw_tf.close();
            bw_tfidf.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void tf_idf_after(Map<String, ArrayList<String>> map) {
        words.clear();
        int k=0;
        for(ArrayList<String> list:map.values()){
            for(int i=0;i<list.size();i++){
                String[] split = list.get(i).split("/");
                ArrayList<String> array =  frequency.process(split[0]);
                file_word_num[k*100+i] = array.size();
                for(int j=0;j<array.size();j++){
                    int index = isAlreadyExist(array.get(j));
                    if(index > -1){
                        //已存在
                        Word word = words.get(index);
                        word.include_file_num++;
                        word.num_in_each_file[k*100+i] ++;
                    }
                    else{
                        //不存在
                        Word word = new Word(500);
                        word.str = array.get(j);
                        word.num_in_each_file[k*100+i]=1;
                        word.include_file_num=1;
                        words.add(word);
                    }
                }
                if(!split[1].equals(" ")  && !split[1].equals("")){
                    String[] f = split[1].split(" ");
                    for(int j=0;j<f.length;j++){
                        if(!f[j].equals("") &&!f[j].equals(" ")){
                           int index = isAlreadyExist(f[j]);
                           if(index>-1){
                               Word word = words.get(index);
                               word.num_in_each_file[k*100+i]+=Integer.parseInt(f[j+1]);
                           }
                           else{
                               Word word = new Word(500);
                               word.str = f[j];
                               word.num_in_each_file[k*100+i]=Integer.parseInt(f[j+1]);
                               word.include_file_num=1;
                               words.add(word);
                           }
                           file_word_num[k*100+i] += Integer.parseInt(f[j+1]);
                           j++;
                        }
                    }
                }
            }
            k++;
        }

        //计算tf和idf
        for(int i=0;i<words.size();i++){
            Word word = words.get(i);
            word.idf = Math.log(((double) 500) / ((double) word.include_file_num));
            for (int j = 0; j < 500; j++)
                word.tf[j] = ((double) word.num_in_each_file[j]) / file_word_num[j];
        }

        //写入tf_after, tfidf_after
        try {
            File tf = new File("resource/tf_after.arff");
            File tfidf = new File("resource/tfidf_after.arff");
            if(!tf.exists()){
                tf.createNewFile();
            }
            if(!tfidf.exists()){
                tfidf.createNewFile();
            }
            BufferedWriter bw_tfidf = new BufferedWriter(new FileWriter(tf, false));
            BufferedWriter bw_tf = new BufferedWriter(new FileWriter(tfidf, false));
            bw_tf.write("@relation twitter\n");
            bw_tfidf.write("@relation twitter\n");
            for(int i=0;i<words.size();i++){
                bw_tf.write("@attribute "+words.get(i).str+" numeric\n");
                bw_tfidf.write("@attribute "+words.get(i).str+" numeric\n");
            }
            bw_tf.write("@attribute twitter_class {");
            bw_tfidf.write("@attribute twitter_class {");
            for(int i=0;i<classification.size()-1;i++){
                bw_tf.write(classification.get(i)+",");
                bw_tfidf.write(classification.get(i)+",");
            }
            bw_tf.write(classification.get(classification.size()-1)+"}\n@data\n");
            bw_tfidf.write(classification.get(classification.size()-1)+"}\n@data\n");
            for(int i=0;i<500;i++){
                String str_tf = "{";
                String str_tfidf = "{";
                for(int j=0;j< words.size();j++){
                    if(words.get(j).tf[i] != 0.0)
                        str_tf=str_tf+j+" "+words.get(j).tf[i]+",";
                    if(words.get(j).tf[i] != 0.0 && words.get(j).idf != 0.0)
                        str_tfidf=str_tfidf+j+" "+words.get(j).tf[i]*words.get(j).idf+",";
                }
                if(str_tf.length()>0){
                    str_tf= str_tf+(words.size())+" "+classification.get(i/100);
                    str_tf+="}";
                    bw_tf.write(str_tf+"\n");
                }
                if(str_tfidf.length()>0){
                    str_tfidf= str_tfidf+(words.size())+" "+classification.get(i/100);
                    str_tfidf+="}";
                    bw_tfidf.write(str_tfidf+"\n");
                }
            }
            bw_tf.close();
            bw_tfidf.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private int isAlreadyExist(String w) {
        for (int i = 0; i < words.size(); i++) {
            if (words.get(i).str.equals(w))
                return i;
        }
        return -1;
    }

    private ArrayList<Word> words;
    private int[] file_word_num;
    private ArrayList<String> classification = new ArrayList<>();
    Frequency frequency = new Frequency();
}