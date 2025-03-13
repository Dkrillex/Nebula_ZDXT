import pandas as pd
import os
import streamlit as st

from steamlitapp import adjust_column_width


#（1）lineItem/ProductCode列筛选：AmazonCloudFront且lineItem/LineItemDescription列筛选：Requests，将筛选出来的数据复制到另外一个表内，此为请求用量，给客户3折。
#（2）lineItem/ProductCode列筛选：AmazonCloudFront且lineItem/LineItemDescription列筛选GB，将筛选出来的数据复制到另外一个表内，将lineItem/UnblendedRate列改为0.0026，lineItem/LineItemDescription列的单价也需改为：0.0026，将筛选出来的数据复制到另外一个表内，此为流量的用量。
#（3）其他的数据为没有折扣的部分，筛选出来单独放一个Sheet表内。
#（4）每300k流量赠送一个请求，流量合计/1024/1024/300=赠送请求数
def xunlei_cdn_aws():
       uploaded_file = st.file_uploader("上传迅雷原始账单")
       if uploaded_file is not None:
           df = pd.read_excel(uploaded_file, sheet_name='590183662869')     
        # 获取工作表为590183662869的表格
        #    xls = pd.ExcelFile(uploaded_file)
        #    sheet_names = xls.sheet_names
        #    st.write("可用的工作表:", sheet_names)
        #    st.dataframe(df)
           #打印共有多少列，多少数据
           st.write(df.shape[0])
           # 第一步 把产品不是Amazon CloudFront的列出来 做一个表
           st.write("不含Amazon CloudFront的表格")
           df1 = df[df['product/ProductName'] != 'Amazon CloudFront']
           st.dataframe(df1)
           st.write("总行数：",df1.shape[0])

           # 第二步 把产品是Amazon CloudFront的列出来，且lineItem/LineItemDescription列包含GB不包含Origin
           df = df[df['product/ProductName'] == 'Amazon CloudFront']
           df2 = df[df['lineItem/LineItemDescription'].str.contains('GB', na=False) & ~df['lineItem/LineItemDescription'].str.contains('Origin', na=False)]
           st.write("Amazon CloudFront的DTO表格")
           st.dataframe(df2)
           st.write("总行数：",df2.shape[0])
           # 计算lineItem/UsageAmount总和
           df2['lineItem/UsageAmount'] = df2['lineItem/UsageAmount'].astype(float)
           total_usage = df2['lineItem/UsageAmount'].sum()
           st.write(f"总流量: {total_usage} GB")
           st.write(f"总流量: {total_usage*1000*1000} KB")
           # 计算总流量*1000*1000/300=赠送请求数
           send_total_usage = total_usage*1000*1000/300
           st.write(f"赠送请求数: {send_total_usage:,.0f} 次")

           # 第三步 把产品是Amazon CloudFront的列出来，且lineItem/LineItemDescription列包含Requests不包含TAX
           df3 = df[df['lineItem/LineItemDescription'].str.contains('Requests', na=False) & ~df['lineItem/LineItemDescription'].str.contains('TAX', na=False)]
           # 请求 lineItem/UsageAmount 并且做倒叙排列
           df3 = df3.sort_values(by='lineItem/UsageAmount', ascending=False)
           st.write("Amazon CloudFront的CDN表格")
           st.dataframe(df3)
           st.write("总行数：", df3.shape[0])

           # 计算累计值直到超过赠送请求数
           df3['累计请求数'] = df3['lineItem/UsageAmount'].cumsum()
           # 找到第一个超过赠送请求数的行
           target_row = df3[df3['累计请求数'] > send_total_usage].iloc[0] if not df3[df3['累计请求数'] > send_total_usage].empty else None
           
           if target_row is not None:
               row_index = df3[df3['累计请求数'] > send_total_usage].index[0]
               row_number = df3.index.get_loc(row_index) + 1
               st.write(f"赠送请求数 {send_total_usage:,.0f} 在第 {row_number} 行用完")
               st.write(f"该行累计请求数: {target_row['累计请求数']:,.0f}")
               超出部分 = target_row['累计请求数'] - send_total_usage
               st.write(f"超出部分: {超出部分:,.0f}")

               # 将0到104行的lineItem/UsageAmount设为0
               df3.iloc[0:row_number, df3.columns.get_loc('lineItem/UsageAmount')] = 0

               # 计算第row_number行需要扣除的部分
               if row_number < len(df3):
                   next_row = df3.iloc[row_number]
                   original_amount = next_row['lineItem/UsageAmount']
                   adjusted_amount = original_amount - 超出部分
                   st.write(f"第 {row_number + 1} 行原始请求数: {original_amount:,.0f}")
                   st.write(f"第 {row_number + 1} 行调整后请求数: {adjusted_amount:,.0f}")

                   # 更新DataFrame中的值
                   df3.iloc[row_number, df3.columns.get_loc('lineItem/UsageAmount')] = adjusted_amount
                   # 重新计算累计请求数
                   df3['累计请求数'] = df3['lineItem/UsageAmount'].cumsum()
                   st.write("更新后的CDN表格：")
                   st.dataframe(df3)
                   df3['lineItem/UnblendedCost'] = df3['lineItem/UsageAmount'] * df3['lineItem/UnblendedRate']
                   st.write("计算后的CDN表格：")
                   st.dataframe(df3)

           else:
               st.write("赠送请求数超过了所有请求的总和")
            
           # 创建ExcelWriter对象准备写入Excel文件
           output_filename = "迅雷CDN分析结果.xlsx"
           with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
               # 将不同类型的数据写入不同的sheet
               df1.to_excel(writer, sheet_name='非CloudFront服务', index=False)
               df2.to_excel(writer, sheet_name='CloudFront-DTO', index=False)
               df3.to_excel(writer, sheet_name='CloudFront-CDN', index=False)
               
               # 调整每个sheet的列宽
               workbook = writer.book
               for sheet_name in workbook.sheetnames:
                   worksheet = workbook[sheet_name]
                   adjust_column_width(worksheet)
           
           st.success(f"已生成分析文件: {output_filename}")
           
           # 添加下载按钮
           if os.path.exists(output_filename):
               with open(output_filename, "rb") as file:
                   st.download_button(
                       label="下载分析后文件",
                       data=file,
                       file_name=output_filename,
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                   )