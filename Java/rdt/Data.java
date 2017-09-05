package com.yqg.rdt;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.io.File;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import jxl.Workbook;
import jxl.write.Label;
import jxl.write.WritableSheet;
import jxl.write.WritableWorkbook;
import jxl.write.WriteException;

//attribute types include numeric and discrete
enum Type{numeric,nominal}

/**
 * abstract class Attribute
 * implemented by Numeric and Nominal
 */
abstract class Attribute{
    //indicate this attribute is numeric or discrete
    Type t;

    //attribtue name
    String name="";

    //attribute id
    int id;
}

/**
 * class Numeric
 * implement Attribute
 * set t to numeric
 */
class Numeric extends Attribute{
    Numeric() {
        this.t=Type.numeric;
    }
}

/**
 * class Nominal
 * implement Attribute
 * set t to discrete
 */
class Nominal extends Attribute{
    /**
     * constructor method
     * set t to nominal
     * set isUsed to false
     */
    Nominal(){
        this.t = Type.nominal;
    }

    /**
     * set nominal attribute domain
     * @param s : string array, add array element to list
     */
    public void setDomain(String[] s){
        domain = new ArrayList<String>();
        for(int i=0;i<s.length;i++)
            domain.add(s[i]);
    }

    /**
     * set nominal attribute domain
     * @param list:set domain to list
     */
    public void setDomain(List<String> list){
        this.domain = list;
    }

    /**
     * get the domain of this attribute
     * @return domain
     */
    public List<String> getDomain() {
        return domain;
    }


    /**
     * list domain to store attribute's domain
     */
    private List<String> domain;

    boolean getIsUsed(){
        return isUsed;
    }

    void setIsUsed(boolean used) {
        isUsed = used;
    }

    /**
     * isUsed
     */
    private boolean isUsed;
}

/**
 * this class read arff file
 * parse the string from file to list
 * include train set and test set
 */
public class Data {

    /**
     * constructor method
     * call method to generate data
     */
    Data(Parameters param){
        this.param = param;
        attributes = new ArrayList<>();
        train = new ArrayList<>();
        test = new ArrayList<>();
        labels = new ArrayList<String>();

        // generate label
        Window.printMessageLn("reading label...");
        generateLabel();
        Window.printMessageLn("done");

        //generate attribute
        Window.printMessageLn("reading attributes...");
        generateAttribute();
        Window.printMessageLn("done");

        //generate train set
        Window.printMessageLn("reading train set...");
        generateTrain();
        Window.printMessageLn("done");

        // generate test set
        Window.printMessageLn("reading test set...");
        generateTest();
        Window.printMessageLn("done");
        // writeToXls();
    }

    /**
     * reads file train.arff
     * splits input string by space and stores into list
     */
    private void generateTrain(){
        String data = null;
        BufferedReader br_train;
        try {
            br_train = new BufferedReader(new InputStreamReader(new FileInputStream(param.trainFile)));
            while((data = br_train.readLine())!=null){
                if(!data.equals("@data"))
                    continue;
                break;
            }
            int i=1;
            while((data = br_train.readLine())!=null){
//                Window.printMessageLn("reading line "+i);
                i++;
                if(data.equals(""))
                    continue;
                String[] s = data.split(",");
                ArrayList<String> arrayList=new ArrayList<String>(Arrays.asList(s));
                train.add(arrayList);
            }
//            Window.printMessageLn("total features number "+i);
            br_train.close();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    /**
     * read file label.xml
     * parse xml and stores into list label
     */
    private void generateLabel(){
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        try {
            DocumentBuilder db=dbf.newDocumentBuilder();
            Document document = db.parse(param.labelFile);
            NodeList labelList =document.getElementsByTagName("label");
            for(int i=0;i<labelList.getLength();i++){
                labels.add(((Element)labelList.item(i)).getAttribute("name"));
//                Window.printMessageLn("reading label "+labels.get(i));
            }
            param.label_num = labels.size();
//            Window.printMessageLn("total labels number "+param.label_num);
        } catch (ParserConfigurationException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (SAXException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }catch (IOException e){
            e.printStackTrace();
        }
    }

    /**
     * read file test.arff
     * splits input string by space and stores into list test
     */
    private void generateTest(){
        String data = null;
        BufferedReader br_test;
        try {
            br_test = new BufferedReader(new InputStreamReader(new FileInputStream(param.testFile)));
            while((data = br_test.readLine())!=null){
                if(!data.equals("@data"))
                    continue;
                break;
            }
            int i=1;
            while((data = br_test.readLine())!=null){
//                Window.printMessageLn("reading line "+i);
                i++;
                if(data.equals(""))
                    continue;
                String[] s = data.split(",");
                ArrayList<String> arrayList=new ArrayList<String>(Arrays.asList(s));
                test.add(arrayList);
            }
//            Window.printMessageLn("total features number "+i);
            br_test.close();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    /**
     * generate list attribute
     */
    private void generateAttribute(){
        BufferedReader br_attribute;
        String data=null;
        int id = 0;
        try {
            br_attribute = new BufferedReader(new InputStreamReader(new FileInputStream("resource/train.arff")));
            while((data=br_attribute.readLine())!=null){
                String[] str=data.split(" ");
                if(str[0].equals("@attribute") && !labels.contains(str[1])){
//                    Window.printMessageLn("reading attribute "+str[1]);
                    if(str[2].equals("numeric")){
                        Numeric numeric=new Numeric();
                        numeric.name=str[1];
                        numeric.id = id;
                        attributes.add(numeric);
                    }else{
                        Nominal nominal=new Nominal();
                        String domainString=str[2].substring(str[2].indexOf('{')+1, str[2].indexOf('}'));
                        nominal.setDomain(domainString.split(","));
                        nominal.name=str[1];
                        nominal.id = id;
                        attributes.add(nominal);
                    }
                    id++;
                }else if(str[0].equals("@data")) {
                    param.attribute_num = id;
                    return;
                }
            }
//            Window.printMessageLn("total attribtues number" + param.attribute_num);
            br_attribute.close();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    /**
     * write data to xls file
     */
    private void writeToXls(){
        WritableWorkbook wwb=null;
        String path="resource/data.xls";
        File file=new File(path);
        try{
            wwb = Workbook.createWorkbook(file);
            WritableSheet sheet=wwb.createSheet("train",0);
            //train
            for(int i=0;i<attributes.size();i++){
                Label label=new Label(i,0,attributes.get(i).name);
                sheet.addCell(label);
            }
            for(int j=0;j<this.labels.size();j++){
                Label label=new Label(attributes.size()+j,0,this.labels.get(j));
                sheet.addCell(label);
            }
            for(int i=0;i<train.size();i++){
                for(int j=0;j<train.get(i).size();j++){
                    sheet.addCell(new Label(j,i+1,train.get(i).get(j)));
                }
            }
            //test
            sheet=wwb.createSheet("test",1);
            for(int i=0;i<attributes.size();i++){
                Label label=new Label(i,0,attributes.get(i).name);
                sheet.addCell(label);
            }
            for(int j=0;j<this.labels.size();j++){
                Label label=new Label(attributes.size()+j,0,this.labels.get(j));
                sheet.addCell(label);
            }
            for(int i=0;i<test.size();i++){
                for(int j=0;j<test.get(i).size();j++){
                    sheet.addCell(new Label(j,i+1,test.get(i).get(j)));
                }
            }
            wwb.write();
            wwb.close();
        }catch(IOException|WriteException e){
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    /**
     * get train set
     * @return train set
     */
    List<ArrayList<String>> getTrainSet(){
        return train;
    }

    /**
     * get test set
     * @return test set
     */
    public List<ArrayList<String>> getTestSet(){
        return test;
    }

    /**
     * get attribtes
     * @return attributes
     */
    List<Attribute> getAttributes(){
        return attributes;
    }

    /**
     * get labels
     * @return labels
     */
    List<String> getLabels(){
        return labels;
    }

    //train set
    private List<ArrayList<String>> train;

    //test set
    private List<ArrayList<String>> test;

    //attribute set
    private List<Attribute> attributes;

    //label set
    private List<String> labels;

    private Parameters param;
}

