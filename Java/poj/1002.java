import java.util.Scanner;
import java.util.Map;
import java.util.TreeMap;
import java.util.Set;
import java.util.Iterator;

public class Main {
	public static void main(String[] args){
		Map<String,Integer> m = new TreeMap<String,Integer>();
		Scanner in = new Scanner(System.in);
		int n;
		n = in.nextInt();
		for(int i=0;i<n;i = i+1){
			String str = in.next();
			StringBuffer sb = new StringBuffer();
			str = str.replace("-", "");
			sb.append(str);
			for(int j=0;j<str.length();j++){
				if(str.charAt(j)=='A' ||str.charAt(j)=='B'||str.charAt(j)=='C'){
					sb.replace(j, j+1, "2");
				}else if(str.charAt(j)=='D' ||str.charAt(j)=='E'||str.charAt(j)=='F'){
					sb.replace(j, j+1, "3");
				}else if(str.charAt(j)=='G' ||str.charAt(j)=='H'||str.charAt(j)=='I'){
					sb.replace(j, j+1, "4");
				}else if(str.charAt(j)=='J' ||str.charAt(j)=='K'||str.charAt(j)=='L'){
					sb.replace(j, j+1, "5");
				}else if(str.charAt(j)=='M' ||str.charAt(j)=='N'||str.charAt(j)=='O'){
					sb.replace(j, j+1, "6");
				}else if(str.charAt(j)=='P' ||str.charAt(j)=='R'||str.charAt(j)=='S'){
					sb.replace(j, j+1, "7");
				}else if(str.charAt(j)=='T' ||str.charAt(j)=='U'||str.charAt(j)=='V'){
					sb.replace(j, j+1, "8");
				}else if(str.charAt(j)=='W' ||str.charAt(j)=='X'||str.charAt(j)=='Y'){
					sb.replace(j, j+1, "9");
				}
			}
			if(m.containsKey(sb.toString())){
				int count = m.get(sb.toString())+1;
				m.put(sb.toString(), count);
			}else{
				m.put(sb.toString(), 1);
			}
		}
		Set<String> se =m.keySet();
		Iterator<String> it = se.iterator();
		boolean flag = false;
		while(it.hasNext()){
			String s = it.next().toString();
			int count = m.get(s);
			if(count > 1){
				flag = true;
				System.out.println(s.substring(0,3) + "-"+s.substring(3,s.length())+ " " + count);
			}
		}
		if(!flag){
			System.out.println("No duplicates. ");
		}
		in.close();
	}
}