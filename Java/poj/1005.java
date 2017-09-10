import java.util.Scanner;

public class Main {
	public static void main(String[] args){
		Scanner in = new Scanner(System.in);
		int n = in.nextInt();
		for(int i=1;i<=n;i++){
			int year = 0;
			double area = 0;
			double x = in.nextDouble();
			double y = in.nextDouble();
			while((x*x+y*y)*Math.PI/2 > area){
				area += 50;
				year ++;
			}
			System.out.println("Property "+i+": This property will begin eroding in year "+year+".");
		}
		System.out.println("END OF OUTPUT.");
		in.close();
	}
}
