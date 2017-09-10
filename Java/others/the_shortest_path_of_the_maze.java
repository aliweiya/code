import java.util.*;  
class Pos{
	int px,py;
	public Pos(int x, int y){
		this.px = x;
		this.py = y;
	}
}
public class Main { 
	
	static int N,M;
	static char[][] maze;
    public static void main(String[] args) {  
    	Scanner in = new Scanner(System.in);
    	N = in.nextInt();
    	M = in.nextInt();
    	maze = new char[N][M];
    	in.nextLine();
    	int i=0;
    	while(i<N){
    		int j=0;
    		String s = in.nextLine().toString();
    		while(j<M){
    			maze[i][j] = s.charAt(j);
    			j++;
    		}
    		i++;
    	}

    	System.out.println(bfs());
    	in.close();
    }
    static int bfs(){
    	int[][] dis = new int[N][M];
    	int Gx = 0,Gy = 0;
    	Queue<Pos> p = new LinkedList<Pos>();
    	for(int i=0;i<N;i++){
    		for(int j=0;j<M;j++){
    			dis[i][j] = 100000;
    			if(maze[i][j] == 'S'){
    				Pos pt = new Pos(i,j);
    				dis[i][j]=0;
    				p.add(pt);
    			}
    			if(maze[i][j] == 'G'){
    				Gx = i;
    				Gy = j;
    			}
    		}
    	}
    	while(!p.isEmpty()){
    		int px = p.element().px;
    		int py = p.element().py;
    		p.remove();
    		if(px == Gx && py == Gy)
    			break;
    		int[] dx = {0,-1,0,1};
    		int[] dy = {-1,0,1,0};
    		for(int i=0;i<4;i++){
    			int nx=px+dx[i];
				int ny = py+dy[i];
				if(0<=nx&&nx<N&&0<=ny&&ny<M&&maze[nx][ny]!='#'&&dis[nx][ny]==100000){
					Pos pt = new Pos(nx,ny);
					p.add(pt);
					dis[nx][ny] =dis[px][py]+1;
				}
    		}
    	}
    	return dis[Gx][Gy];
    }
}