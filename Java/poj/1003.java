import java.util.Scanner;

public class Main {
	public static void main(String[] args){
		Scanner in = new Scanner(System.in);
		while(in.hasNext()){
			double f = in.nextFloat();
			if(f == 0.0){
				in.close();
				return;
			}
			if(f <= 0.5){
				System.out.println("1 card(s)");
				continue;
			}
			int ans = 1;
			double sum = 0.5;
			int base = 2;
			while(sum<f){
				base++;
				ans++;
				sum += 1.0/base;
			}
			System.out.println(ans + " card(s)");
		}
		in.close();
	}
}
