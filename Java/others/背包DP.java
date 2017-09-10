import java.util.*;

public class test {
	static int[] w,v;
	static int[][] dp;
	static int n,W;
	public static void main(String[] args){
		Scanner in = new Scanner(System.in);
		n = in.nextInt();
		w = new int[n];
		v = new int[n];
		dp = new int[100][100];
		for(int i=0;i<100;i++){
			for(int j=0;j<100;j++){
				dp[i][j] = -1;
			}
		}
		for(int i=0;i<n;i++){
			w[i] = in.nextInt();
			v[i] = in.nextInt();
		}
		W = in.nextInt();
		System.out.println(rec(0,W));
		in.close();
	}
	static int rec(int i, int j){
		if(dp[i][j]>=0)
			return dp[i][j];
		int res=0;
		if(i == n){
			return 0;
		}else if(j < w[i]){
			res = rec(i+1,j);
		}else{
			res = max(rec(i+1,j),rec(i+1,j-w[i])+v[i]);
		}
		return dp[i][j] = res;
	}
	static int max(int i, int j){
		if(i>=j)
			return i;
		else
			return j;
	}
}
