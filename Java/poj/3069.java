import java.util.*;  

public class Main { 
    public static void main(String[] args) {  
    	Scanner in = new Scanner(System.in);
    	while(true){
    		int R = in.nextInt();
    		int N = in.nextInt();
    		if(N==-1 && R==-1)
    			break;
    		int[] X = new int[N];
    		for(int i=0;i<N;i++)
    			X[i] = in.nextInt();
    		Arrays.sort(X);
    		int i=0,ans = 0;
    		while(i<N){
    			int s = X[i++];
    			while(i<N&&X[i]<=s+R)
    				i++;
    			int p = X[i-1];
    			while(i<N && X[i]<=p+R)
    				i++;
    			ans++;
    		}
    		System.out.println(ans);
    	}
    	in.close();
    }
}
