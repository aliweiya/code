import java.util.Scanner;

public class Main {
	public static void main(String[] args){
		Scanner in = new Scanner(System.in);
		int turn = 0;
		while(true){
			int p = in.nextInt();
			int e = in.nextInt();
			int i = in.nextInt();
			int d = in.nextInt();
			
			turn ++;
			
			if(p == -1 && e == -1 && i == -1 && d == -1){
				in.close();
				return;
			}
			int days = (5544 * p + 14421 * e + 1288 * i - d) % (21252);  
			if (days <= 0) {
			   days = 23 * 28 * 33 + days;
			}  
			System.out.println("Case "+turn+": the next triple peak occurs in "+days+" days.");
		}
		
	}
}
