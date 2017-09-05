package com.yqg.rdt;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.Random;
import java.util.Set;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.TreeMap;

/**
 * abstract class Node
 * extended by class NominalNode and NumericNode
 * defines basic attribute and method for a node
 */
abstract class Node{

    /**
     * set isLeaf attribute
     * @param isLeaf boolean value for isLeaf
     */
    void setIsLeaf(boolean isLeaf){
        this.isLeaf = isLeaf;
    }

    /**
     * return isLeaf attribute
     * @return isLeaf attribute
     */
    public boolean getIsLeaf(){
        return isLeaf;
    }

    /**
     * set classification attribute
     * @param classification the classification attribute
     */
    void setClassification(boolean classification){
        this.classification = classification;
    }

    /**
     * return classification of this node
     * @return classification of this node
     */
    public boolean getClassification(){
        return classification;
    }

    /**
     * set left child node
     * @param node left node
     */
    public void setLeftNode(Node node){
        this.leftNode = node;
    }

    /**
     * set right child node
     * @param node right node
     */
    public void setRightNode(Node node){
        this.rightNode = node;
    }

    /**
     * return left node
     * @return left node
     */
    public Node getLeftNode(){
        return leftNode;
    }

    /**
     * return right node
     * @return right node
     */
    public Node getRightNode(){
        return rightNode;
    }

    /**
     * set attribute id of this node
     * @param attr id of an attribute
     */
    void setAttribute(int attr){
        this.attribute = attr;
    }

    /**
     * return attribute id of this node
     * @return attribute
     */
    public int getAttribute() {
        return attribute;
    }

    public void setType(Type t){
        this.type = t;
    }

    public Type getType(){
        return type;
    }

    private boolean isLeaf = false;
    private boolean classification = true;
    private Node leftNode;
    private Node rightNode;
    private int attribute;
    private Type type;
}

/**
 * class for nominal node
 * extends class Node
 */
class NominalNode extends Node{
    /**
     * constructor method
     */
    NominalNode(){
        super();
        domain = new HashSet<String>();
    };

    /**
     * constructor method
     * @param domain domain of this node
     */
    public NominalNode(Set<String> domain){
        super();
        this.domain = domain;
    }

    /**
     * set domain of this node
     * @param domain domain of this node
     */
    public void setDomain(Set<String> domain){
        this.domain = domain;
    }

    /**
     * add a value to domain of this attribute
     * @param str value to add
     */
    void addValue(String str){
        this.domain.add(str);
    }

    /**
     * return domain of this attribute
     * @return domain of this attribute
     */
    public Set<String> getDomain(){
        return domain;
    }

    private Set<String> domain;
}

/**
 * class for numeric node
 * extends class Node
 */
class NumericNode extends Node{

    /**
     * constructor method
     */
    NumericNode(){
        super();
    }

    public NumericNode(int value){
        super();
        this.value = value;
    }

    void setValue(double value){
        this.value = value;
    }
    double getValue(){
        return value;
    }
    private double value;
}
class SingleLabelDecisionTree{

    {
        random = new Random();
        subTrainSet = new ArrayList<>();
    }

    /**
     * build a single label stochastic decision tree
     * @param param parameters to build a tree
     * @param label label id for this tree
     * @return root node for this tree
     */
    Node buildTree(Parameters param, int label){
        this.label = label;
        this.param = param;
        sample();
        generateRootNodes();
        generateChildNodes(rootNode, 1);
        return rootNode;
    }

    /**
     * features selection
     */
    private void sample(){
        subTrainSet.clear();
        for(int i=0;i<param.maxSampleNum;i++){
            int r = random.nextInt(param.data.getTrainSet().size());
            subTrainSet.add(r);
        }
    }

    /**
     * generate root node for decision tree
     * generate a random integer r first
     * if the attribute whose id is r is a nominal node, call generateNominalNode() method
     * else call generateNumericNode method
     */
    private void generateRootNodes(){
        int r = random.nextInt(param.attribute_num);
        if(param.data.getAttributes().get(r).t == Type.nominal){
            //choose a nominal attribute
            rootNode = new NominalNode();
            rootNode.setAttribute(r);
            rootNode.setType(Type.nominal);
            generateNominalNodes(rootNode,0,r);
        }else{
            //choose a numeric attribute
            rootNode = new NumericNode();
            rootNode.setAttribute(r);
            rootNode.setType(Type.numeric);
            generateNumericNodes(rootNode,0,r);
        }
    }

    /**
     * generate child nodes for a node
     * generate a random integer r first
     * if the attribute whose id is r is a nominal node, call generateNominalNode() method
     * else call generateNumericNode method
     * then recursively call generateChildNodes to build a tree
     * @param currentNode add child nodes generated to currentNode
     * @param currentHeight current tree height, if currentHeight is greater than maxTreeHeight, return
     */
    private void generateChildNodes(Node currentNode, int currentHeight){
        if(currentHeight > param.maxTreeHeight)
            return;
        int r = random.nextInt(param.attribute_num);
        if(param.data.getAttributes().get(r).t == Type.nominal){
            //choose a nominal attribute
            generateNominalNodes(currentNode,currentHeight, r);
        }else{
            //choose a numeric attribute
            generateNumericNodes(currentNode,currentHeight, r);
        }
        if(!currentNode.getIsLeaf()){
            currentNode.getLeftNode().setAttribute(r);
            currentNode.getRightNode().setAttribute(r);
            generateChildNodes(currentNode.getLeftNode(),currentHeight+1);
            generateChildNodes(currentNode.getRightNode(),currentHeight+1);
        }

    }

    /**
     * generate a nominal node
     * divide the domain into true and false, add to the domain of the nominal node
     * @param currentNode current node to generate
     * @param currentHeight current height of the tree, if the currentHeight is equal to maxTreeHeight, then set this node to a leaf node
     * @param r the attribute id
     */
    private void generateNominalNodes(Node currentNode, int currentHeight, int r){
        if(currentNode.getIsLeaf())
            return;
        if(!((Nominal)param.data.getAttributes().get(r)).getIsUsed()){
            if(currentHeight>param.maxTreeHeight)
                return;
            Set<String> train_true = new HashSet<>();
            Set<String> train_false = new HashSet<>();
            for(int i=0;i<subTrainSet.size();i++){
                if(param.data.getTrainSet().get(subTrainSet.get(i)).get(param.attribute_num+label).equals("1"))
                    train_true.add(param.data.getTestSet().get(subTrainSet.get(i)).get(r));
                else
                    train_false.add(param.data.getTestSet().get(subTrainSet.get(i)).get(r));
            }
            if(train_true.size() == 0){
                //all false
                NominalNode nominalNodeFalse = new NominalNode();
                nominalNodeFalse.setClassification(false);
                nominalNodeFalse.setAttribute(r);
                nominalNodeFalse.setIsLeaf(false);
                nominalNodeFalse.setType(Type.nominal);
                Iterator<String> iterator = train_false.iterator();
                while(iterator.hasNext())
                    nominalNodeFalse.addValue(iterator.next());
                currentNode.setRightNode(nominalNodeFalse);
            }
            else if(train_false.size() == 0){
                //all true
                NominalNode nominalNodeTrue = new NominalNode();
                nominalNodeTrue.setClassification(true);
                nominalNodeTrue.setAttribute(r);
                nominalNodeTrue.setIsLeaf(true);
                nominalNodeTrue.setType(Type.nominal);
                Iterator<String> iterator = train_true.iterator();
                while(iterator.hasNext())
                    nominalNodeTrue.addValue(iterator.next());
                currentNode.setLeftNode(nominalNodeTrue);
            }
            else{
                NominalNode nominalNodeTrue = new NominalNode();
                nominalNodeTrue.setClassification(true);
                nominalNodeTrue.setAttribute(r);
                nominalNodeTrue.setType(Type.nominal);
                if(currentHeight >= param.maxTreeHeight)
                    nominalNodeTrue.setIsLeaf(true);
                else
                    nominalNodeTrue.setIsLeaf(false);
                Iterator<String> iterator = train_true.iterator();
                while(iterator.hasNext())
                    nominalNodeTrue.addValue(iterator.next());
                currentNode.setLeftNode(nominalNodeTrue);

                NominalNode nominalNodeFalse = new NominalNode();
                nominalNodeFalse.setClassification(false);
                nominalNodeFalse.setAttribute(r);
                nominalNodeFalse.setType(Type.nominal);
                if(currentHeight >= param.maxTreeHeight)
                    nominalNodeFalse.setIsLeaf(true);
                else
                    nominalNodeFalse.setIsLeaf(false);
                iterator = train_false.iterator();
                while(iterator.hasNext())
                    nominalNodeFalse.addValue(iterator.next());
                currentNode.setRightNode(nominalNodeFalse);
            }
            ((Nominal) param.data.getAttributes().get(r)).setIsUsed(true);
        }
    }

    /**
     * generate a numeric node
     * sort the attribute value,
     * @param currentNode current node to generate
     * @param currentHeight current height of the tree, if the currentHeight is equal to maxTreeHeight, then set this node to a leaf node
     * @param r the attribute id
     */
    private void generateNumericNodes(Node currentNode, int currentHeight, int r){
        if(currentNode.getIsLeaf())
            return;
        Map<Double, Boolean> train = new TreeMap<>(new Comparator<Double>() {
            @Override
            public int compare(Double o1, Double o2) {
                if(o1>o2)
                    return 1;
                else if(o1<o2)
                    return -1;
                return 0;
            }
        });
        for(int i=0;i<subTrainSet.size();i++){
            train.put(Double.parseDouble(param.data.getTrainSet().get(subTrainSet.get(i)).get(r)), param.data.getTrainSet().get(subTrainSet.get(i)).get(param.attribute_num+label).equals("1"));
        }

        double info_gain = 0;
        double divide_point = 0;

        //calculate info(D)
        double total = train.size();
        double positive = 0;
        double negative = 0;
        for(boolean b:train.values()){
            if(b)
                positive++;
            else
                negative++;
        }
        double info_D = -(positive/total)*(Math.log(positive/total)/Math.log(2.0))-(negative/total)*(Math.log(negative/total)/Math.log(2.0));

        //calculate info_A_D
        double first = 0;
        int i=0;
        for(Map.Entry<Double, Boolean> entry:train.entrySet()){
            if(i == 0){
                first = entry.getKey();
            }
            else{
                int j=0;
                double first_total=0, second_total=0, positive_first=0, negative_first = 0, positive_second = 0, negative_second = 0;
                for(Map.Entry<Double, Boolean> entry1:train.entrySet()){
                    if(j<i){
                        if(entry1.getValue())
                            positive_first++;
                        else
                            negative_first++;
                    }else{
                        if(entry1.getValue())
                            positive_second++;
                        else
                            negative_second++;
                    }
                    j++;
                }

                first_total = positive_first + negative_first;
                second_total = positive_second + negative_second;
                double positive_first_ratio = positive_first/(first_total);
                double negative_first_ratio = negative_first/(first_total);
                double positive_second_ratio = positive_second/(second_total);
                double negative_second_ratio = negative_second/(second_total);

                double info_D_first, info_D_second, info_A_D;
                if(positive_first_ratio == 0)
                    info_D_first = -negative_first_ratio*(Math.log(negative_first_ratio)/Math.log(2));
                else if(negative_first_ratio == 0)
                    info_D_first = -positive_first_ratio*(Math.log(positive_first_ratio)/Math.log(2));
                else
                    info_D_first = -positive_first_ratio*(Math.log(positive_first_ratio)/Math.log(2))-negative_first_ratio*(Math.log(negative_first_ratio)/Math.log(2));

                if(positive_second_ratio == 0)
                    info_D_second = -negative_second_ratio*(Math.log(negative_second_ratio)/Math.log(2));
                else if(negative_second_ratio == 0)
                    info_D_second = -positive_second_ratio*(Math.log(positive_second_ratio)/Math.log(2));
                else
                    info_D_second = -positive_second_ratio*(Math.log(positive_second_ratio)/Math.log(2))-negative_second_ratio*(Math.log(negative_second_ratio)/Math.log(2));

                info_A_D = (first_total/total)*info_D_first+(second_total/total)*info_D_second;

                if(info_D-info_A_D>info_gain){
                    info_gain = info_D-info_A_D;
                    divide_point = (first+entry.getKey())/2;
                }
                first = entry.getKey();
            }
            i++;
        }
        int positive_first = 0, negative_first = 0, positive_second = 0, negative_second = 0;
        for(Map.Entry<Double, Boolean> entry:train.entrySet()){
            if(entry.getKey()<divide_point){
                if(entry.getValue())
                    positive_first++;
                else
                    negative_first++;
            }else{
                if(entry.getValue())
                    positive_second++;
                else
                    negative_second++;
            }
        }

        ((NumericNode)currentNode).setValue(divide_point);

        boolean classification_first = positive_first>negative_first;
        boolean classification_second = positive_second>negative_second;
        if(classification_first == classification_second){
            //leaf node
            //((NumericNode)currentNode).setValue(divide_point);
            currentNode.setClassification(classification_first);
            currentNode.setIsLeaf(true);
        }else{
            NumericNode numericNodeLeft = new NumericNode();
            numericNodeLeft.setClassification(classification_first);
            numericNodeLeft.setType(Type.numeric);
            if(currentHeight >= param.maxTreeHeight)
                numericNodeLeft.setIsLeaf(true);
            else
                numericNodeLeft.setIsLeaf(false);
            currentNode.setLeftNode(numericNodeLeft);

            NumericNode numericNodeRight = new NumericNode();
            numericNodeRight.setClassification(classification_second);
            numericNodeRight.setType(Type.numeric);
            if(currentHeight >= param.maxTreeHeight)
                numericNodeRight.setIsLeaf(true);
            else
                numericNodeRight.setIsLeaf(false);
            currentNode.setRightNode(numericNodeRight);
        }
    }

    private Random random;
    private Node rootNode;
    private int label;
    private Parameters param;

    private ArrayList<Integer> subTrainSet;
}