import java.util.*;  

public class Main {  
	static int n,k;
	static int[] a;
    public static void main(String[] args) {  
    	Scanner in = new Scanner(System.in);
    	n = in.nextInt();
    	a = new int[n];
    	int i=0;
    	while(i++ !=n-1){
    		a[i] = in.nextInt();
    	}
    	k = in.nextInt();
    	if(dfs(0,0))
    		System.out.println("yes");
    	else
    		System.out.println("no");
    	
    	in.close();
    }
    static boolean dfs(int i,int sum){
    	if(i == n-1)
    		return sum==k;
    	if(dfs(i+1,sum))
    		return true;
    	if(dfs(i+1,sum+a[i]))
    		return true;
    	return false;
    }
}