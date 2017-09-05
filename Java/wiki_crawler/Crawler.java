package wiki_crawler;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Queue;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.FutureTask;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.htmlparser.beans.StringBean;
import org.htmlparser.util.ParserException;

class Crawler {
    Crawler(String[] t, int depth, int page_num){
        for(int i=0;i<t.length;i++)
            topic.add(t[i]);
        max_depth = depth;
        max_page_num = page_num;
    }
    Crawler(ArrayList<String> t, int depth, int page_num){
        topic = t;
        max_depth = depth;
        max_page_num = page_num;
    }
    {
        base_link = "https://en.wikipedia.org/wiki/";
        queue = new LinkedList<>();
        topic = new ArrayList<>();
        topic_articles = new ArrayList<>();
        visited_url = new ArrayList<>();
    }
    public ArrayList<String> crawler(){
        String article;
        queue.clear();
        topic_articles.clear();
        for(int i=0;i<topic.size();i++){
            article = "";
            current_depth = 0;
            current_page_num = 0;
            queue.clear();
            visited_url.clear();
            if(!isValidURL(base_link+topic.get(i))){
                //System.out.println(base_link + topic.get(i)+" is not a valid url!");
                Main.printMessage(base_link + topic.get(i)+" is not a valid url!");
                continue;
            }else{
                queue.offer(base_link + topic.get(i));
                while(current_depth<max_depth && current_page_num<max_page_num){
                    article += crawl(topic.get(i));
                    current_depth ++;
                    try{
                        Thread.sleep(500);
                    }catch(InterruptedException e){
                        break;
                    }
                }
                topic_articles.add(article);
                //System.out.println(article);
                try{
                    File file = new File("resource/crawler/"+topic.get(i)+".txt");
                    if(!file.exists())
                        file.createNewFile();
                    BufferedWriter bw = new BufferedWriter(new FileWriter(file));
                    bw.write(article);
                    bw.close();
                }
                catch(IOException e){
                    e.printStackTrace();
                }
            }
        }
        return topic_articles;
    }
    private String crawl(String str){
        String article = "";
        int queue_size = queue.size();
        Queue<String> q = new LinkedList<>();
        while(queue_size--!=0 && current_page_num<max_page_num){
            String current_url = queue.poll();
            System.out.println(topic.toString());
            Main.printMessage(topic.toString());
            System.out.println("crawling "+str+" @"+current_url);
            Main.printMessage("crawling "+str+" @"+current_url);
            current_page_num++;
            ExecutorService executor = Executors.newSingleThreadExecutor();
            FutureTask<String> future = (FutureTask<String>) executor.submit(
                    ()->{
                        StringBean sb = new StringBean();
                        sb.setLinks(true);
                        sb.setURL(current_url);
                        return sb.getStrings();
                    }
            );
            String result;
            try{
                result = future.get(2, TimeUnit.MINUTES);
            } catch (InterruptedException|ExecutionException |TimeoutException e) {
                result = "";
                future.cancel(true);
            } finally {
                executor.shutdown();
            }
            if(!result.equals("")){
                if(!visited_url.contains(current_url))
                    visited_url.add(current_url);
                article += process_html(q, "\t"+result);
            }
        }
        queue = q;
        return article;
    }
    private boolean isValidURL(String urlStr){
        int counts = 0;
        if(urlStr == null || urlStr.length()<=0)
            return false;
        while(counts < 5){
            try{
                URL url = new URL(urlStr);
                HttpURLConnection con = (HttpURLConnection)url.openConnection();
                if(con.getResponseCode() == 200)
                    return true;
                else
                    counts++;
            }catch(Exception ex){
                counts++;
            }
        }
        return false;
    }
    private String process_html(Queue<String> q, String result){
        String url;
        Pattern pattern = Pattern.compile("https://[^>]*");
        Matcher matcher = pattern.matcher(result);
        while(matcher.find()){
            url = matcher.group();
            if(url.contains(".jpg"))
                continue;
            else if(url.contains(".JPG"))
                continue;
            else if(url.contains(".gif"))
                continue;
            else if(url.contains(".GIF"))
                continue;
            else if(url.contains("#"))
                continue;
            else if(url.contains("%"))
                //不是英文
                continue;
            else if(url.contains("="))
                continue;
            else if(url.substring(7,url.length()).contains(":"))
                continue;
            else if(url.contains("("))
                continue;
            else if(!url.contains("en.wikipedia.org"))
                continue;
            else if(!visited_url.contains(url)) {
                visited_url.add(url);
                q.offer(url);
                //System.out.println(url);
            }
        }
        return result.replaceAll("<[^>]*>", " ");
    }
    private ArrayList<String> topic;
    private String base_link;
    private int max_depth;
    private int max_page_num;
    private Queue<String> queue;
    private ArrayList<String> visited_url;
    private ArrayList<String> topic_articles;

    private int current_depth;
    private int current_page_num;


}