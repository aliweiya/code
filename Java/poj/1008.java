import java.util.*;  

public class Main {  
    public static void main(String[] args) {  
    	String[] Haab = new String[]{
    			"pop","no","zip","zotz","tzec","xul",
    			"yoxkin","mol","chen","yax","zac","ceh",
    			"mac","kankin","muan","pax","koyab","cumhu",
    			"uayet"
    	};
    	ArrayList<String> HaabList = new ArrayList<String>();  
        for (int i = 0; i < Haab.length; i++) {  
            HaabList.add(Haab[i]);  
        }  
    	String[] Tzolkin = new String[]{
    			"imix","ik","akbal","kan","chicchan",
    			"cimi","manik","lamat","muluk","ok",
    			"chuen","eb","ben","ix","mem",
    			"cib","caban","eznab","canac","ahau"
    	};
        Scanner in = new Scanner(System.in);  
        int n = in.nextInt();
        System.out.println(n);
        while(n-- != 0){
        	String hDay = in.next();
        	hDay = hDay.substring(0,hDay.length()-1);
            String hMonth = in.next();
            int hYear = in.nextInt();
            int Days = Integer.parseInt(hDay)+HaabList.indexOf(hMonth)*20+hYear*365;
            int tYear = Days / 260;
            String tMonth = Tzolkin[Days%20];
            int tDay = Days%13+1;
        	System.out.println(tDay + " " +tMonth + " " + tYear);  
        }
        in.close();
    }
}