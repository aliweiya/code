import java.sql.*;

public class ReflectionMysql {
    public static void main(String[] args) {
        try {
            Class.forName("com.mysql.jdbc.Driver");
            String url="jdbc:mysql://localhost:3306/test";
            String username = "root";
            String password = "root";
            Connection conn = DriverManager.getConnection(url, username, password);
            PreparedStatement stmt = conn.prepareStatement("select name,age from person");
            ResultSet rs = stmt.executeQuery();
            while(rs.next()){
                String name = rs.getString(1);
                Integer age = rs.getInt(2);
                System.out.println(name+"  "+age);
            }
            rs.close();
            stmt.close();
            conn.close();
        } catch (ClassNotFoundException e) {
            System.out.println("加载驱动失败");
        } catch (SQLException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
}