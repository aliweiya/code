package config;

import com.mchange.v2.c3p0.ComboPooledDataSource;
import org.apache.commons.dbutils.QueryRunner;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.*;

import javax.sql.DataSource;
import java.beans.PropertyVetoException;

/*
 * 该类是一个配置类，作用和 bean.xml 一样
 * `@Configuration` 用于指定当前类是一个配置类
 *      当配置类作为AnnotationCOnfigApplicationContext对象创建的参数时，该注解可以不写
 *      `@Import`注解用于导入其它的配置类，属性value用于指定其它配置类的字节码。有Import的类就是父配置类，导入的是子配置类
 * `@ComponentScan` 用于制定创建容器时要扫描的包
 *      values = basePackages = <context:component-scan base-package="com.itheima"></context:component-scan>
 *
 * `@PropertySource` 指定属性文件位置
 */
@Configuration
@ComponentScan(basePackages = "com.itheima")
@Import(JdbcConfig.class)
@PropertySource("classpath:jdbcConfig.properties")
public class SpringConfiguration {

    @Value("${jdbc.driver}")
    private String driver;

    @Value("${jdbc.url}")
    private String url;

    @Value("${jdbc.username}")
    private String username;

    @Value("${jdbc.password}")
    private String password;

    /*
     * 用于创建QueryRunner对象
     * `@Bean` 把当前方法的返回值作为bean对象存入spring的IOC容器
     *      name属性用于指定bean的id，默认值是当前方法名
     *
     * 当我们用注解配置方法时，如果方法有参数，Spring框架会去容器中查找有没有可用的bean对象，查找方式和Autowired一样。
     */
    @Bean(name="runner")
    @Scope("prototype")
    public QueryRunner createQueryRunner(DataSource dataSource){
        return new QueryRunner(dataSource);
    }

    /*
     * 创建数据源对象
     */
    @Bean(name="dataSource")
    public DataSource createDataSource(){
        try{
            ComboPooledDataSource ds = new ComboPooledDataSource();
            ds.setDriverClass(driver);
            ds.setJdbcUrl(url);
            ds.setUser(username);
            ds.setPassword(password);
            return ds;
        }catch(PropertyVetoException e){
            throw new RuntimeException(e);
        }
    }
}
