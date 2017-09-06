package com.yqg.rdt;

class Algorithm {

    /**
     *  constructor method
     */
    Algorithm(Parameters param){
        Window.printMessageLn("reading data...");
        param.data = new Data(param);
        Window.printMessageLn("reading data done");
        param.decisionTree = new Node[param.label_num][param.maxTreeNum];
        this.param = param;
    }

    /**
     * instantiate single label decision trees for each label
     * then call buildTree() method to generate a single label decision tree
     */
    void random_decision_tree() {
        Window.printMessageLn("building trees for each label...");
        for(int i=0;i<param.label_num;i++){
            //build decision trees for each label
            Window.printMessageLn("label "+param.data.getLabels().get(i));
            for(int j=0;j<param.maxTreeNum;j++){
                //build many decision trees
                SingleLabelDecisionTree sldt = new SingleLabelDecisionTree();
                param.decisionTree[i][j] = sldt.buildTree(param, i);
            }
            Window.printMessageLn("done");
        }
        Window.printMessageLn("finished");
        Window.printMessageLn("start test...");
        test();
    }
    private void test(){
        int TP=0, TN=0, FP=0,FN=0;
        for(int i=0;i<param.data.getTestSet().size();i++){
            for(int j=0;j<param.label_num;j++){
                boolean classification = param.data.getTrainSet().get(i).get(param.attribute_num+j).equals("1");
                boolean classification_predict = testInstance(i, j);
                if(classification)
                    if(classification_predict)
                        TP++;
                    else
                        FN++;
                else
                    if(classification_predict)
                        FP++;
                    else
                        TN++;
            }
        }
       Window.printMessage("TP = "+TP);
       Window.printMessage(", TN = "+TN);
       Window.printMessage(", FP = "+ FP);
       Window.printMessageLn(", FN = "+FN);
       Window.printMessageLn("accuracy is "+((double)TP+TN)/(TP+TN+FP+FN));
    }
    private boolean testInstance(int f, int label){
        int classification_true = 0;
        int classification_false = 0;
        for(int i=0;i<param.decisionTree[label].length;i++){
            Node currentNode = param.decisionTree[label][i];
            while(!currentNode.getIsLeaf()){
                if(currentNode.getType() == Type.numeric){
                    //numeric attribute
                    int attribute_id = currentNode.getAttribute();
                    double val = Double.parseDouble(param.data.getTestSet().get(f).get(attribute_id));
                    double split_point = ((NumericNode)currentNode).getValue();
                    if(val<split_point)
                        currentNode = currentNode.getLeftNode();
                    else
                        currentNode = currentNode.getRightNode();
                }
                else{
                    //nominal

                }
            }
            if(currentNode.getClassification())
                classification_true++;
            else
                classification_false++;
        }
        return classification_true>classification_false;
    }


    private Parameters param;
}

