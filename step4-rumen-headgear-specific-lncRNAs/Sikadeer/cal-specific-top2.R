df <- read.table("cal-specific-top2-input-new.txt",header=TRUE,sep="\t")
data <- data.matrix(df)
columns <- colnames(df)

columns <- colnames(df)
df2 <- data.frame()


for (i in 1:nrow(data)) {
    row <- data[i, ]
    max_value_index <- which.max(row)
    max_value <- row[max_value_index]
    
    # 将最大值置为负无穷，重新找最大值即为次大值
    row[max_value_index] <- -Inf
    second_max_value_index <- which.max(row)
    second_max_value <- row[second_max_value_index]
    
    # 打印结果
    cat(sprintf("  Max Value: %f, Column: %s", max_value, columns[max_value_index]))
    cat(sprintf("  Second Max Value: %f, Column: %s\n", second_max_value,columns[second_max_value_index]))
}
