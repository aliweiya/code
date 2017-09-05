package wiki_crawler;

import java.awt.Toolkit;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.TreeMap;

import weka.classifiers.Evaluation;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.trees.*;
import weka.core.Instances;
import weka.core.converters.ArffLoader;
import weka.gui.beans.Classifier;

import javax.swing.JFileChooser;
import javax.swing.JLabel;
import javax.swing.JMenuBar;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuItem;
import javax.swing.WindowConstants;
import javax.swing.filechooser.FileFilter;

public class Main{
    public static void main(String args[]){

        screenWidth = Toolkit.getDefaultToolkit().getScreenSize().width;
        screenHeight = Toolkit.getDefaultToolkit().getScreenSize().height;
        windowWidth = 960;
        windowHeight = 640;

        JFrame jf=new JFrame("扩充短文本");
        jf.setBounds((screenWidth - windowWidth)/2,
                (screenHeight - windowHeight)/2, windowWidth, windowHeight);

        setMenu(jf);

        textArea = new JTextArea();
        textArea.setEditable(false);
        JScrollPane scroll =new JScrollPane(textArea);
        scroll.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);
        scroll.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);
        jf.add(scroll);
        jf.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        jf.setVisible(true);
    }
    private static void setMenu(JFrame jf){
        JMenuBar menuBar = new JMenuBar();
        JMenu fileMenu = new JMenu("文件");
        JMenuItem openSourceFile = new JMenuItem("打开原文件");
        openSourceFile.addActionListener(e->{
            JFileChooser fileChooser = new JFileChooser("./resource");
            fileChooser.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);
            fileChooser.setAcceptAllFileFilterUsed(false);
            fileChooser.addChoosableFileFilter(new FileFilter() {
                @Override
                public boolean accept(File f){
                    if(f.getName().endsWith(".txt"))
                        return true;
                    else if(f.isDirectory())
                        return true;
                    return false;
                }

                @Override
                public String getDescription(){
                    return "txt文本文件";
                }
            });
            fileChooser.showDialog(new JLabel(), "Open");
            fileChooser.setVisible(true);
        });
        fileMenu.add(openSourceFile);

        JMenu operationMenu = new JMenu("操作");
        JMenuItem generate_TFIDF_before = new JMenuItem("生成ARFF文件");
        generate_TFIDF_before.addActionListener(e->{
            Thread t = new Thread(new Runnable() {
                @Override
                public void run() {
                    //读取文件
                    read();
                    printMessage("读取文件...");
                    //去停用词,计算tf和idf
                    tfidf = new TFIDF();
                    tfidf.tf_idf(data);
                    printMessage("完成");
                }
            });
            t.start();
        });
        operationMenu.add(generate_TFIDF_before);

        JMenuItem generate_TFIDF_after = new JMenuItem("生成扩展后的ARFF文件");
        generate_TFIDF_after.addActionListener(e->{
           Thread t = new Thread(new Runnable() {
               @Override
               public void run() {
                   //提取关键词
                   printMessage("提取关键词");
                   get_keywords();
                   //爬取数据,插入到原文
                   printMessage("爬取数据,插入到原文");
                   try{
                       crawl_words(1,1,30);
                   }catch (IOException e1){
                       e1.printStackTrace();
                   }
                   //重新计算tfidf
                   printMessage("重新计算tfidf");
                   tfidf.tf_idf_after(data);
               }
           });
           t.start();
        });
        operationMenu.add(generate_TFIDF_after);

        JMenuItem call_weka = new JMenuItem("调用weka");
        call_weka.addActionListener(e->{
            Thread t = new Thread(new Runnable() {
                @Override
                public void run() {
                    weka();
                }
            });
            t.start();
        });
        operationMenu.add(call_weka);

        menuBar.add(fileMenu);
        menuBar.add(operationMenu);
        jf.setJMenuBar(menuBar);

    }
    static private void read(){
        try{
            BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(new File("resource/resource.txt"))));
            String str = "";
            while((str = br.readLine())!=null){
                //读取5类，每类100条
                String classification = str.substring(str.lastIndexOf(' ')+1,str.length());
                if(data.containsKey(classification)){
                    if(data.get(classification).size()<100){
                        data.get(classification).add(str.substring(0,str.lastIndexOf(' ')));
                    }
                }else if(data.size()<5){
                    ArrayList<String> list = new ArrayList<>();
                    list.add(str.substring(0,str.lastIndexOf(' ')));
                    data.put(classification, list);
                }
            }
            for(String s:data.keySet()){
                topics.add(s);
            }

        }catch(IOException e){
            e.printStackTrace();
        }
    }
    static private void get_keywords(){
        try{
            BufferedWriter bw = new BufferedWriter(new FileWriter(new File("resource/keywords.txt")));
            Frequency frequency = new Frequency();
            for(ArrayList<String> list:data.values()){
                Map<String, Integer> word = new HashMap<>();
                for(int i=0;i<list.size();i++){
                    ArrayList<String> w = frequency.process(list.get(i));
                    for(int j=0;j<w.size();j++){
                        if(word.containsKey(w.get(j))){
                            word.put(w.get(j), word.get(w.get(j))+1);
                        }
                        else{
                            word.put(w.get(j),1);
                        }
                    }
                }
                //取前20个
                ArrayList<String> keyword = new ArrayList<>();
                List<Map.Entry<String,Integer>> l =new ArrayList<Map.Entry<String,Integer>>(word.entrySet());
                Collections.sort(l, new Comparator<Map.Entry<String, Integer>>() {
                    public int compare(Map.Entry<String, Integer> o1,
                                       Map.Entry<String, Integer> o2) {
                        return (o2.getValue() - o1.getValue());
                    }
                });
                int j=0;
                for(Map.Entry<String, Integer> entry:l){
                    if(++j>20)
                        break;
                    keyword.add(entry.getKey());
                    bw.write(entry.getKey()+" "+entry.getValue()+"\n");
                }
                keywords.add(keyword);
            }
            bw.close();
        }catch(IOException e){
            e.printStackTrace();
        }


    }
    static private void crawl_words(int depth, int page_num, int save_nums)throws IOException {
        BufferedWriter br = new BufferedWriter(new FileWriter("resource/resource_save.txt",false));
        Frequency f = new Frequency();
        for (int i = 0; i < keywords.size(); i++) {
            Crawler words_crawler = new Crawler(keywords.get(i), depth, page_num);
            ArrayList<String> result = words_crawler.crawler();//每个关键字所爬取的内容为一项
            for (int j = 0; j < result.size(); j++) {
                Map<String, Integer> frequency = f.pre_process(result.get(j), keywords.get(i).get(j));
                List<Map.Entry<String, Integer>> list = new ArrayList<Map.Entry<String, Integer>>(frequency.entrySet());
                Collections.sort(list, new Comparator<Map.Entry<String, Integer>>() {
                    public int compare(Map.Entry<String, Integer> o1,
                                       Map.Entry<String, Integer> o2) {
                        return (o2.getValue() - o1.getValue());
                    }
                });
                int k = 0;
                try {
                    File file = new File("resource/keywords/" + topics.get(i) + "_" + keywords.get(i).get(j) + ".txt");
                    System.out.println(file.getName());
                    if (!file.exists())
                        file.createNewFile();
                    BufferedWriter bw = new BufferedWriter(new FileWriter(file, false));
                    for (Map.Entry<String, Integer> entry : list) {
                        if (++k > save_nums)
                            break;
                        bw.write(entry.getKey() + " " + entry.getValue() + "\n");
                    }
                    bw.close();
                } catch (IOException e) {
                    System.out.println(e);
                }
            }
        }
        //插入到原文中
        int k = 0;
        for (Map.Entry<String, ArrayList<String>> entry : data.entrySet()) {
            ArrayList<String> list = entry.getValue();
            for (int i = 0; i < list.size(); i++) {
                list.set(i, list.get(i) + " / ");
                String[] str = list.get(i).split(" ");
                String s = list.get(i);
                for (int m = 0; m < str.length; m++) {
                    if (keywords.get(k).contains(str[m])) {
                        BufferedReader br_keywords = new BufferedReader(new InputStreamReader(new FileInputStream(new File("resource/keywords/" + entry.getKey() + "_" + str[m] + ".txt"))));
                        String d = "";
                        while ((d = br_keywords.readLine()) != null)
                            s =s+d+" ";
                        br_keywords.close();
                    }
                }
                list.set(i, s);
                br.write(list.get(i) + "\n");
            }
            k++;
        }
        br.close();
    }

    static void printMessage(String s){
        textArea.append(s+"\n");
    }
    static void weka(){
        try{
            J48 classifier = new J48();
           ArffLoader loaderTrainBefore = new ArffLoader();
           loaderTrainBefore.setFile(new File("resource/tf_before.arff"));
           Instances trainInstsBefore = loaderTrainBefore.getDataSet();
           printMessage("训练扩展之前，决策树。。。");
           trainInstsBefore.setClassIndex(trainInstsBefore.numAttributes()-1);
           classifier.buildClassifier(trainInstsBefore);
           printMessage(classifier.toString());
           Evaluation evaluation = new Evaluation(trainInstsBefore);
           Random rand = new Random(1);
           int folds = 10;
            evaluation.crossValidateModel(classifier, trainInstsBefore, folds, rand);
            printMessage(evaluation.toMatrixString());
            printMessage(evaluation.toClassDetailsString());

            //after
            printMessage("训练扩展之后，决策树。。。");
            ArffLoader loaderTrainAfter = new ArffLoader();
            loaderTrainAfter.setFile(new File("resource/tf_after.arff"));
            Instances trainInstAfter = loaderTrainAfter.getDataSet();
            trainInstAfter.setClassIndex(trainInstAfter.numAttributes()-1);
            classifier.buildClassifier(trainInstAfter);
            printMessage(classifier.toString());
            evaluation.crossValidateModel(classifier,trainInstAfter,10,new Random(1));
            printMessage(evaluation.toMatrixString());
            printMessage(evaluation.toClassDetailsString());

            NaiveBayes naiveBayes = new NaiveBayes();
            printMessage("训练扩展之前，朴素贝叶斯。。。");
            naiveBayes.buildClassifier(trainInstsBefore);
            printMessage(naiveBayes.toString());
            evaluation.crossValidateModel(naiveBayes,trainInstsBefore,10,new Random(1));
            printMessage(evaluation.toMatrixString());
            printMessage(evaluation.toClassDetailsString());

            //after
            printMessage("训练扩展之后，朴素贝叶斯。。。");
            naiveBayes.buildClassifier(trainInstAfter);
            printMessage(naiveBayes.toString());
            evaluation.crossValidateModel(naiveBayes,trainInstAfter,10,new Random(1));
            printMessage(evaluation.toMatrixString());
            printMessage(evaluation.toClassDetailsString());

        }catch(Exception e){
            e.printStackTrace();
        }
    }
    private static ArrayList<ArrayList<String>> keywords = new ArrayList<>();
    private static Map<String, ArrayList<String>> data = new HashMap<>();
    private static ArrayList<String> topics = new ArrayList<>();

    private static int screenWidth;
    private static int screenHeight;
    private static int windowWidth;
    private static int windowHeight;

    static JTextArea textArea;

    static TFIDF tfidf;
}