import java.util.*;  
class DNA  
{  
    private String str = null;  
    private int sortNum = 0;  
        
    public DNA(String input)  
    {  
        str = input;  
        int num = 0;  
        for(int i = 0; i < str.length()-1; i++)  
        {  
            for(int j = i+1; j < str.length(); j++)  
                if(str.charAt(i) > str.charAt(j))  
                    num++;  
        }  
        sortNum = num;  
    }  
    public int getSortNum()  
    {  
        return sortNum;  
    }  
    public String toString()  
    {  
        return str;  
    }  
}  
class DNAComparator implements Comparator<DNA>  
{  
    public int compare(DNA o1, DNA o2)  
    {  
        DNA d1 = o1;  
        DNA d2 = o2;  
        if(d1.getSortNum() > d2.getSortNum())  
            return 1;  
        else if(d1.getSortNum() == d2.getSortNum())  
            return 0;  
        else 
            return -1;  
    }  
}  

public class Main {  

    public static void main(String[] args) {  
        Scanner cin = new Scanner(System.in);  
        String[] str = cin.nextLine().split(" ");  
        int col = Integer.valueOf(str[0]).intValue();  
        int row = Integer.valueOf(str[1]).intValue();  
        List<DNA> list = new ArrayList<DNA>();          

        for(int i = 0; i < row; i++)  
        {  
            DNA dna = new DNA(cin.nextLine());  
            list.add(dna);  
        }  

        Collections.sort(list, new DNAComparator());  
        print(list);  
        cin.close();
    }  
    private static void print(List<DNA> list)  
    {  
        Iterator<DNA> iter = list.iterator();  
        while(iter.hasNext())  
        {  
            System.out.println(iter.next());  
        }  
    }  
}
