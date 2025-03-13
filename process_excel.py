import pandas as pd
import os

# 如何让用户把文件导进来
input_file = input("请输入文件路径: ")


# 读取客户信息表
customerDf = pd.read_excel("客户名称.xlsx")
print("客户信息表:")
print(customerDf)
bill_file = input_file
# 读取账单明细表
# bill_file = "FTLCLOUD-2025年2月账单明细.xlsx"
df = pd.read_excel(bill_file)

# 将两张表按Project ID进行合并
merged_df = pd.merge(df, 
                    customerDf,
                    left_on='Project ID',
                    right_on='客户project-id',
                    how='left')

# 按客户公司名称筛选数据
merged_df1 = merged_df[merged_df['客户公司名称'] =='小黑鱼']
merged_df2 = merged_df[merged_df['客户公司名称'] =='优聚大鱼'] 
merged_df3 = merged_df[merged_df['客户公司名称'] =='玖邦数码']
# 每个表的Cost ($)字段除以0.3赋值到new_cost
merged_df1['new_cost'] = merged_df1['Cost ($)'] / 0.3
merged_df2['new_cost'] = merged_df2['Cost ($)'] / 0.3
merged_df3['new_cost'] = merged_df3['Cost ($)'] / 0.3

# 创建ExcelWriter对象
output_filename = "测试文件.xlsx"
with pd.ExcelWriter(output_filename) as writer:
    # 将不同客户的数据写入不同的sheet
    merged_df1.to_excel(writer, sheet_name='小黑鱼', index=False)
    merged_df2.to_excel(writer, sheet_name='优聚大鱼', index=False)
    merged_df3.to_excel(writer, sheet_name='玖邦数码', index=False)
    # 将完整数据写入总表sheet
    merged_df.to_excel(writer, sheet_name='总表', index=False)

print(f"已生成多sheet文件: {output_filename}")
# ---------------------------------------------------------------





# 将合并后的数据赋值给df继续使用
df = merged_df
print(df)

# 打印df数据
print(df.head())

# 创建新的列，将Cost ($)除以0.3
df['Adjusted Cost'] = df['Cost ($)'] / 0.3

print(df.head())

# 按Project ID分组并保存到不同的Excel文件
for project_id in df['Project ID'].unique():
    # 获取当前Project ID的数据
    project_df = df[df['Project ID'] == project_id]
    
    # 创建输出文件名
    output_filename = f"Project_{project_id}_账单明细.xlsx"
    
    # 保存到新的Excel文件
    project_df.to_excel(output_filename, index=False)
    print(f"已生成文件: {output_filename}")

print("所有文件处理完成！") 