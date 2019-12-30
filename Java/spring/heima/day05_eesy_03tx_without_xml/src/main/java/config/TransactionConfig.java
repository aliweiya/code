package config;

import org.springframework.context.annotation.Bean;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;
import org.springframework.transaction.PlatformTransactionManager;

import javax.sql.DataSource;

/**
 * 事务相关配置类
 */
public class TransactionConfig {

    /**
     * 事务管理器
     * @param dataSource
     * @return
     */
    @Bean("transactionManager")
    public PlatformTransactionManager createTransactionManager(DataSource  dataSource){
        return new DataSourceTransactionManager(dataSource);
    }
}
