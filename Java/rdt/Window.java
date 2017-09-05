package com.yqg.rdt;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTabbedPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.SwingConstants;
import javax.swing.WindowConstants;
import javax.swing.filechooser.FileFilter;

import java.awt.FlowLayout;
import java.awt.Graphics;
import java.awt.GridLayout;
import java.awt.Image;
import java.awt.Toolkit;

import java.io.File;
import java.util.Properties;

import org.python.util.PythonInterpreter;

class Window {

    {
        screenWidth = Toolkit.getDefaultToolkit().getScreenSize().width;
        screenHeight = Toolkit.getDefaultToolkit().getScreenSize().height;
        windowWidth = 960;
        windowHeight = 640;
    }

    /**
     * constructor method
     * genetate window and set menus
     * @param param parameters for the project
     */
    Window(Parameters param){
        this.param = param;
        JFrame jf=new JFrame("Random Decision Tree");
        jf.setBounds((screenWidth - windowWidth)/2,
                (screenHeight - windowHeight)/2, windowWidth, windowHeight);

        setMenu(jf);

        textArea = new JTextArea();
        textArea.setEditable(false);

        JScrollPane scrollPane = new JScrollPane(textArea);
        scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);
        scrollPane.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);

        jf.add(scrollPane);

        jf.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        jf.setVisible(true);
    }

    /**
     * method to set menu for the window
     * @param jf frame
     */
    private void setMenu(JFrame jf){
        JMenu fileMenu = new JMenu("File");
        JMenuItem openLabelFile = new JMenuItem("Open Label File");
        openLabelFile.addActionListener(e->{
            JFileChooser fileChooser = new JFileChooser("./resource");
            fileChooser.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);
            fileChooser.setAcceptAllFileFilterUsed(false);
            fileChooser.addChoosableFileFilter(new FileFilter() {
                @Override
                public boolean accept(File f) {
                    if(f.getName().endsWith(".xml"))
                        return true;
                    else if(f.isDirectory())
                        return true;
                    return false;
                }

                @Override
                public String getDescription() {
                    return "xml file";
                }
            });
            fileChooser.showDialog(new JLabel(), "Open");
            fileChooser.setVisible(true);
            param.labelFile = fileChooser.getSelectedFile().getPath();
            printMessageLn("label "+param.labelFile);
            //System.out.println(labelFile);
        });
        fileMenu.add(openLabelFile);
        JMenuItem openTrainFileMenuItem = new JMenuItem("Open Train File");
        openTrainFileMenuItem.addActionListener(openFile->{
            JFileChooser fileChooser = new JFileChooser("./resource");
            fileChooser.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);
            fileChooser.setAcceptAllFileFilterUsed(false);
            fileChooser.addChoosableFileFilter(new FileFilter() {
                @Override
                public boolean accept(File f) {
                    if(f.getName().endsWith(".arff"))
                        return true;
                    else if(f.isDirectory())
                        return true;
                    return false;
                }

                @Override
                public String getDescription() {
                    return "arff file";
                }
            });
            fileChooser.showDialog(new JLabel(), "Open");
            fileChooser.setVisible(true);
            param.trainFile = fileChooser.getSelectedFile().getPath();
            printMessageLn("train file "+param.trainFile);
            //System.out.println(trainFile);
        });
        fileMenu.add(openTrainFileMenuItem);
        JMenuItem openTestFileMenuItem = new JMenuItem("Open Test File");
        openTestFileMenuItem.addActionListener(openFile->{
            JFileChooser fileChooser = new JFileChooser("./resource");
            fileChooser.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);
            fileChooser.setAcceptAllFileFilterUsed(false);
            fileChooser.addChoosableFileFilter(new FileFilter() {
                @Override
                public boolean accept(File f) {
                    if(f.getName().endsWith(".arff"))
                        return true;
                    else if(f.isDirectory())
                        return true;
                    return false;
                }

                @Override
                public String getDescription() {
                    return "arff file";
                }
            });
            fileChooser.showDialog(new JLabel(), "Open");
            fileChooser.setVisible(true);
            param.testFile = fileChooser.getSelectedFile().getPath();
            printMessageLn("test file "+param.testFile);
            //System.out.println(testFile);
        });
        fileMenu.add(openTestFileMenuItem);
//        JMenuItem saveToXLSMenuItem = new JMenuItem("Save Data to XLS File");
//        saveToXLSMenuItem.addActionListener(e->{
//
//        });
//        fileMenu.add(saveToXLSMenuItem);
        JMenuItem exitMenuItem = new JMenuItem("Exit");
        exitMenuItem.addActionListener(e->{
            System.exit(0);
        });
        fileMenu.add(exitMenuItem);

        JMenu optionMenu = new JMenu("Option");
        JMenuItem setParameterMenuItem = new JMenuItem("Set Parameters");
        setParameterMenuItem.addActionListener(e->{
            JDialog parameterDialog = new JDialog(jf, "Set Parameters", true);

            int width = 320;
            int height = 220;

            parameterDialog.setBounds(jf.getBounds().x+(jf.getBounds().width-width)/2,
                    jf.getBounds().y+(jf.getBounds().height-height)/2,width,height);
            parameterDialog.setLayout(new FlowLayout());

            JPanel parameterPanel = new JPanel();
            parameterPanel.setLayout(new GridLayout(6,1));

            JLabel treeHeightLabel = new JLabel("Set Max Tree Height :");
            if(param.maxTreeHeight!=0)
                parameterPanel.add(treeHeightLabel);
            parameterPanel.add(treeHeightLabel);
            JTextField treeHeightTextField = new JTextField(26);
            if(param.maxTreeHeight!=0)
                treeHeightTextField.setText(param.maxTreeHeight+"");
            parameterPanel.add(treeHeightTextField);

            JLabel treeNumLabel = new JLabel("Set Max Tree Number :");
            parameterPanel.add(treeNumLabel);

            JTextField treeNumTextField = new JTextField(26);
            if(param.maxTreeNum!=0)
                treeNumTextField.setText(param.maxTreeNum+"");
            parameterPanel.add(treeNumTextField);

            JLabel treeSampleNumLabel = new JLabel("Set Max Sample Number :");
            parameterPanel.add(treeSampleNumLabel);

            JTextField treeSampleNumTextField = new JTextField(26);
            if(param.maxSampleNum!=0)
                treeSampleNumTextField.setText(param.maxSampleNum+"");
            parameterPanel.add(treeSampleNumTextField);

            JPanel buttonPanel = new JPanel();

            buttonPanel.setLayout(new FlowLayout(FlowLayout.RIGHT));
            JButton submitButton = new JButton("Submit");
            submitButton.addActionListener(sb->{
                if(!treeHeightTextField.getText().equals(""))
                    param.maxTreeHeight = Integer.parseInt(treeHeightTextField.getText());
                else
                    return;
                if(!treeNumTextField.getText().equals(""))
                    param.maxTreeNum = Integer.parseInt(treeNumTextField.getText());
                else
                    return;
                if(!treeSampleNumTextField.getText().equals(""))
                    param.maxSampleNum = Integer.parseInt(treeSampleNumTextField.getText());
                else
                    return;
                printMessageLn("set maxTreeHeight="+param.maxTreeHeight+", maxTreeNum="+param.maxTreeNum+", maxSampleNum="+param.maxSampleNum);
                parameterDialog.dispose();
            });
            buttonPanel.add(submitButton);

            JButton cancelButton = new JButton("Cancel");
            cancelButton.addActionListener(cb->{
                parameterDialog.dispose();
            });
            buttonPanel.add(cancelButton);

            parameterDialog.add(parameterPanel);
            parameterDialog.add(buttonPanel);
            parameterDialog.setVisible(true);
        });
        optionMenu.add(setParameterMenuItem);
        JMenuItem generateDecisionTreeMenuItem = new JMenuItem("Generate Decision Tree");
        generateDecisionTreeMenuItem.addActionListener(e->{
            if(param.trainFile.equals("")){
                JOptionPane.showMessageDialog(jf, "You didn't choose train set file!", "ERROR",JOptionPane.ERROR_MESSAGE);
            }
            else if(param.testFile.equals("")){
                JOptionPane.showMessageDialog(jf, "You didn't choose test set file!", "ERROR",JOptionPane.ERROR_MESSAGE);
            }
            else if(param.labelFile.equals("")){
                JOptionPane.showMessageDialog(jf, "You didn't choose label set file!", "ERROR",JOptionPane.ERROR_MESSAGE);
            }
            else if(param.maxSampleNum == 0){
                JOptionPane.showMessageDialog(jf, "You didn't set max sample number!", "ERROR",JOptionPane.ERROR_MESSAGE);
            }
            else if(param.maxTreeHeight == 0){
                JOptionPane.showMessageDialog(jf, "You didn't set max tree height!", "ERROR",JOptionPane.ERROR_MESSAGE);
            }
            else if(param.maxTreeNum == 0){
                JOptionPane.showMessageDialog(jf, "You didn't set max tree number!", "ERROR",JOptionPane.ERROR_MESSAGE);
            }
            else {

                Thread t = new Thread(new Runnable() {
                    @Override
                    public void run() {
                        algorithm = new Algorithm(param);
                        algorithm.random_decision_tree();
                    }
                });
                t.run();
            }
        });
        optionMenu.add(generateDecisionTreeMenuItem);

        JMenuItem drawDecisionTreeMenuItem = new JMenuItem("draw decision tree");
        drawDecisionTreeMenuItem.addActionListener(e->{
            if(algorithm == null){
                JOptionPane.showMessageDialog(jf, "decision tree not generated successfully", "ERROR",JOptionPane.ERROR_MESSAGE);
            }else{
               Thread t = new Thread(new Runnable() {
                   @Override
                   public void run() {
                       drawDecisionTree(jf);
                   }
               });
               t.start();
            }
            //drawDecisionTree(jf);
        });
        optionMenu.add(drawDecisionTreeMenuItem);

        JMenu aboutMenu = new JMenu("About");
        JMenuItem aboutMenuItem = new JMenuItem("About");
        aboutMenuItem.addActionListener(e->{
            JOptionPane.showMessageDialog(jf, "Author : Enrico's Ricardo\r\nVersion : 0.1\r\nContact me : yqgffm@163.com", "About",JOptionPane.PLAIN_MESSAGE);
        });
        aboutMenu.add(aboutMenuItem);

        JMenuBar menuBar = new JMenuBar();
        menuBar.add(fileMenu);
        menuBar.add(optionMenu);
        menuBar.add(aboutMenu);

        jf.setJMenuBar(menuBar);
    }

    /**
     * method to draw decision tree on the window
     */
    private void drawDecisionTree(JFrame jf){
        JTabbedPane labelTabbedPane = new JTabbedPane(JTabbedPane.TOP);
        for(int i=0;i<param.label_num;i++){
            JTabbedPane treeTabbedPane = new JTabbedPane(JTabbedPane.TOP);
            for(int j=0;j<param.maxTreeNum;j++){
                JPanel panel = new JPanel();
                panel.add(new JLabel("fdsff"));
                treeTabbedPane.addTab("tree "+(j+1), panel);
            }
            labelTabbedPane.addTab(param.data.getLabels().get(i), treeTabbedPane);
        }

        jf.setContentPane(labelTabbedPane);
        jf.validate();
        jf.repaint();
    }

    static void printMessage(String str){
        textArea.append(str);
    }

    static void printMessageLn(String str){
        textArea.append(str+"\n");
    }
    private int screenWidth;
    private int screenHeight;
    private int windowWidth;
    private int windowHeight;

    private Algorithm algorithm;
    private Parameters param;

    static JTextArea textArea;

}