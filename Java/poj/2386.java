import java.util.*;  

public class Main {  
	static char[][] field;
	static int M,N;
    public static void main(String[] args) {  
    	Scanner in = new Scanner(System.in);
    	int n = in.nextInt();
    	int m = in.nextInt();
    	N=n;
    	M=m;
    	int ponds = 0;
    	in.nextLine();
    	field =  new char[n][m];
    	for(int i=0;i<n;i++){
    		String str = in.nextLine().toString();
    		for(int j=0;j<m;j++){
    			field[i][j] = str.charAt(j);
    		}
    	}
    	for(int i=0;i<n;i++){
    		for(int j =0;j<m;j++){
    			if(field[i][j]=='W'){
    				dfs(i,j);
    				ponds++;
    			}
    		}
    	}
    	System.out.println(ponds);
    	in.close();
    }
    static void dfs(int i,int j){
    	field[i][j] = '.';
    	for(int n =i-1;n<=i+1;n++){
    		for(int m = j-1;m<=j+1;m++){
    			if(m<0||n<0||n>=N||m>=M){
    				continue;
    			}else if(field[n][m]=='W'){
    				dfs(n,m);
    			}
    		}
    	}
    }
}