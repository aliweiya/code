import java.util.*;  

public class Main { 
    public static void main(String[] args) {  
    	Scanner in = new Scanner(System.in);
    	int N = in.nextInt();
    	in.nextLine();
    	String S = "";
    	for(int i=0;i<N;i++){
    		S+=in.nextLine().toString();
    	}
    	String T = "";
    	
    	int a=0,b=N-1,cnt=0;
    	while(a<=b){
    		boolean left = false;
    		for(int i=0;a+i<=b;i++){
    			if(S.charAt(a+i)<S.charAt(b-i)){
    				left = true;
    				break;
    			}
    			else if(S.charAt(a+i)>S.charAt(b-i)){
    				left = false;
    				break;
    			}
    		}
    		if(left == true)
				T+=S.charAt(a++);
			else
				T+=S.charAt(b--);
    		cnt++;
    		if(cnt%80==0)
    			T+="\n";
    	}
    	System.out.println(T);
    	in.close();
    }
}