import java.util.*;  

public class Main { 
    public static void main(String[] args) {  
    	Scanner in = new Scanner(System.in);
    	int[] coin = new int[6];
    	int[] V = {1,5,10,50,100,500};
    	for(int i=0;i<6;i++){
    		coin[i]=in.nextInt();
    	}
    	int A = in.nextInt();
    	int num=0;
    	
    	for(int i=5;i>=0;i--){
    		int t = min(A/V[i],coin[i]);
    		A-=t*V[i];
    		num+=t;
    	}
    	System.out.println(num);
    	in.close();
    }
    static int min(int a,int b){
    	if(a>=b)
    		return b;
    	return a;
    }
}
