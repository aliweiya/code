package wiki_crawler;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by Enrico's Ricardo on 2017/5/16.
 * this class calculate word frequency of an article
 */
public class Frequency {
    {
        sw = new LinkedList<>();
        word = new HashMap<String,Integer>();
        web_address = Pattern.compile("(http[^ ]*)|(www[^ ]*)");
        number = Pattern.compile("[0-9]*");
        english = Pattern.compile("[a-zA-Z]*");
    }
    Frequency(){
        setStopWord();
    }
    public HashMap<String, Integer> pre_process(String s, String t){
        word.clear();
        String[] resource = s.split("\r\n");
        String data;
        Matcher matcher;
        for(int i=0;i<resource.length;i++){
            System.out.println("processing "+t+" line "+i);
            Main.printMessage("processing "+t+" line "+i);
            data = resource[i];
            data = deletePunctuation(data);
            System.out.println(data);
            Main.printMessage(data);
            String[] dataArray = data.split(" ");
            for(int j=0;j<dataArray.length;j++){
                if(dataArray[j].equals(" "))
                    continue;
                if(dataArray[j].equals(""))
                    continue;
                matcher = web_address.matcher(dataArray[j]);
                if(matcher.matches())
                    //web address
                    continue;
                matcher = number.matcher(dataArray[j]);
                if(matcher.matches())
                    //number
                    continue;
                matcher = english.matcher(dataArray[j]);
                if(!matcher.matches())
                    continue;
                dataArray[j] = dataArray[j].toLowerCase();
                if(!isStopWord(dataArray[j])){
                    if(word.containsKey(dataArray[j])){
                        word.put(dataArray[j], word.get(dataArray[j])+1);
                    }else{
                        word.put(dataArray[j], 1);
                    }
                }
            }
        }

        return word;
    }
    public ArrayList<String> process(String str){
        str = deletePunctuation(str);
        String[] dataArray = str.split(" ");
        ArrayList<String> result=new ArrayList<>();
        Matcher matcher;
        for(int i=0;i<dataArray.length;i++){
            if(dataArray[i].equals(" "))
                continue;
            if(dataArray[i].equals(""))
                continue;
            matcher = web_address.matcher(dataArray[i]);
            if(matcher.matches())
                //web address
                continue;
            matcher = number.matcher(dataArray[i]);
            if(matcher.matches())
                //number
                continue;
            matcher = english.matcher(dataArray[i]);
            if(!matcher.matches())
                continue;
            dataArray[i] = dataArray[i].toLowerCase();
            if(!isStopWord(dataArray[i])){
                result.add(dataArray[i]);
            }
        }
        return result;
    }
    private void setStopWord(){
        BufferedReader stopWord=null;
        String data = null;
        try{
            stopWord=new BufferedReader(new InputStreamReader(new FileInputStream("resource/stopword.txt")));
            while((data = stopWord.readLine())!=null){
                sw.add(data);
            }
            stopWord.close();
        }catch(IOException e){
            System.out.print(e);;
        }
    }
    private boolean isStopWord(String str){
        for(int i=0;i<sw.size();i++){
            if(str.equals(sw.get(i)))
                return true;
        }
        return false;
    }
    private static String deletePunctuation(String s){
        String str = "";
        for(int i=0;i<s.length();i++){
            if(!isPunctutaion(s.charAt(i)))
                str=str+s.charAt(i);
            else
                str=str+' ';
        }
        return str;
    }
    private static boolean isPunctutaion(char c){
        if(c == ',')
            return true;
        if(c == '@')
            return true;
        if(c == ':')
            return true;
        if(c == '<')
            return true;
        if(c == '>')
            return true;
        if(c == ';')
            return true;
        if(c == '!')
            return true;
        if(c == '#')
            return true;
        if(c == '$')
            return true;
        if(c == '%')
            return true;
        if(c == '^')
            return true;
        if(c == '&')
            return true;
        if(c == '*')
            return true;
        if(c == '(')
            return true;
        if(c == ')')
            return true;
        if(c == '_')
            return true;
        if(c == '-')
            return true;
        if(c == '+')
            return true;
        if(c == '=')
            return true;
        if(c == '/')
            return true;
        if(c == '.')
            return true;
        if(c == '[')
            return true;
        if(c == ']')
            return true;
        if(c == '{')
            return true;
        if(c == '}')
            return true;
        if(c == '\\')
            return true;
        if(c == '|')
            return true;
        if(c == '"')
            return true;
        if(c == '?')
            return true;
        if(c == '\'')
            return true;
        if(c == '\t')
            return true;
        if(c == '–')
            return true;
        return false;
    }
    /*
    private void writeToFile(){
        FileWriter fw=null;
        BufferedWriter bw=null;
        try{
            fw=new FileWriter(new File(filePath),false);
            bw=new BufferedWriter(fw);
            List<Map.Entry<String,Integer>> list =new ArrayList<Map.Entry<String,Integer>>(word.entrySet());

            Collections.sort(list, new Comparator<Map.Entry<String, Integer>>() {
                public int compare(Map.Entry<String, Integer> o1,
                                   Map.Entry<String, Integer> o2) {
                    return (o2.getValue() - o1.getValue());
                }
            });

            for(Map.Entry<String, Integer> entry:list){
                bw.write(entry.getKey()+" "+entry.getValue()+"\n");
            }
            bw.close();
        }catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
    */
    private List<String> sw;
    private static HashMap<String,Integer> word;
    static Pattern web_address;
    static Pattern english;
    static Pattern number;
}
