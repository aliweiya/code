import java.util.Scanner;

public class Main {
	public static void main(String[] args){
		Scanner in = new Scanner(System.in);
		double sum = 0;
		for(int i=0;i<12;i++){
			sum += in.nextFloat();
		}
		sum /= 12;
		System.out.println(String.format("$%.2f",sum));
		in.close();
	}
}