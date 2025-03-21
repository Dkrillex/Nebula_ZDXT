import pandas as pd
import os
import streamlit as st

from steamlitapp import adjust_column_width


#（1）lineItem/ProductCode列筛选：AmazonCloudFront且lineItem/LineItemDescription列筛选：Requests，将筛选出来的数据复制到另外一个表内，此为请求用量，给客户3折。
#（2）lineItem/ProductCode列筛选：AmazonCloudFront且lineItem/LineItemDescription列筛选GB，将筛选出来的数据复制到另外一个表内，将lineItem/UnblendedRate列改为0.0026，lineItem/LineItemDescription列的单价也需改为：0.0026，将筛选出来的数据复制到另外一个表内，此为流量的用量。
#（3）其他的数据为没有折扣的部分，筛选出来单独放一个Sheet表内。
#（4）每300k流量赠送一个请求，流量合计/1024/1024/300=赠送请求数
def xunlei_cdn_aws():
       st.title("迅雷-CDN-AWS")
       st.write("Create by Jackie Chen")
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
         #   df['lineItem/UsageAmount'] = df['lineItem/UsageAmount'].astype(float).round(10)

           df = df.sort_values(by='lineItem/UsageAmount', ascending=False)

           st.dataframe(df)
           # 第一步 把产品不是Amazon CloudFront的列出来且lineItem/UsageAccountId 为590183662869 做一个表
           st.write("不含Amazon CloudFront的表格")
           dfnoAC = df[~df['product/ProductName'].isin(['Amazon CloudFront']) & df['lineItem/UsageAccountId'].astype(str).str.contains('590183662869')]
           dfnoAC = dfnoAC[['bill/PayerAccountId','lineItem/UsageAccountId','lineItem/UsageStartDate','lineItem/UsageEndDate','lineItem/ProductCode','lineItem/UsageAmount','lineItem/UnblendedRate','lineItem/UnblendedCost','lineItem/LineItemDescription']]

           st.dataframe(dfnoAC)
           st.write("dfnoAC总行数：",dfnoAC.shape[0],"---正确")
           st.write('其他总费用',dfnoAC['lineItem/UnblendedCost'].sum())

           # 第二步 把产品是Amazon CloudFront的列出来，且lineItem/LineItemDescription列包含GB不包含Origin
           dfAC = df[df['product/ProductName'] == 'Amazon CloudFront']
           dfGBnoOrigin = dfAC[dfAC['lineItem/LineItemDescription'].str.contains('GB', na=False) & ~dfAC['lineItem/LineItemDescription'].str.contains('Origin', na=False)].copy()
           
           dfGBnoOrigin['lineItem/UsageAmount'] = dfGBnoOrigin['lineItem/UsageAmount'].astype(float).round(10)
           dfGBandOrigin = dfAC[dfAC['lineItem/LineItemDescription'].str.contains('GB', na=False)]
           dfGBandOrigin = dfGBandOrigin.sort_values(by='lineItem/UsageAmount', ascending=False)
           # dfGBandOrigin的lineItem/UnblendedRate列改为0.0026，lineItem/LineItemDescription列的单价
           dfGBandOrigin['lineItem/UnblendedRate'] = 0.0026
        #    dfGBandOrigin['lineItem/LineItemDescription'] = dfGBandOrigin['lineItem/LineItemDescription'].str.replace('GB', '0.0026')
           dfGBandOrigin['lineItem/UnblendedCost'] = dfGBandOrigin['lineItem/UsageAmount'] * dfGBandOrigin['lineItem/UnblendedRate']
           dfGBandOrigin = dfGBandOrigin[['bill/PayerAccountId','lineItem/UsageAccountId','lineItem/UsageStartDate','lineItem/UsageEndDate','lineItem/ProductCode','lineItem/UsageAmount','lineItem/UnblendedRate','lineItem/UnblendedCost','lineItem/LineItemDescription']]

           st.write("Amazon CloudFront的DTO表格")
           st.dataframe(dfGBandOrigin)
           st.write("dfGBnoOrigin总行数：",dfGBnoOrigin.shape[0],"---正确")
           st.write("dfGBandOrigin总行数：",dfGBandOrigin.shape[0],"---正确")
           # 计算lineItem/UsageAmount总和
           total_usage = dfGBnoOrigin['lineItem/UsageAmount'].sum()
         #   st.write(f"总流量: {total_usage} GB")
           st.write(f"总流量: {total_usage*1000*1000} KB---正确")
           # 计算总流量*1000*1000/300=赠送请求数
           send_total_usage = total_usage*1000*1000/300
           st.write(f"赠送请求数: {send_total_usage:,.0f} 次")
           st.write("dfGBandOrigin总费用：",dfGBandOrigin['lineItem/UnblendedCost'].sum(),"---正确")

           # 第三步 把产品是Amazon CloudFront的列出来，且lineItem/LineItemDescription列包含Requests不包含TAX
        #    dfACRequestsNoTax = dfAC[dfAC['lineItem/LineItemDescription'].str.contains('Requests', na=False) & ~dfAC['lineItem/LineItemDescription'].str.contains('Tax', na=False)]
        #    # 请求 lineItem/UsageAmount 并且做倒叙排列
        #    dfACRequestsNoTax = dfACRequestsNoTax.sort_values(by='lineItem/UsageAmount', ascending=False)
        #    st.dataframe(dfACRequestsNoTax)
        #    st.write("dfACRequestsNoTax总行数：", dfACRequestsNoTax.shape[0])
           st.write("----CDN计算正确-----------------")
           dfACRequestsandTax = dfAC[dfAC['lineItem/LineItemDescription'].str.contains('Requests', na=False)]
           dfACRequestsandTax = dfACRequestsandTax.sort_values(by='lineItem/UsageAmount', ascending=False)
        #    st.write("Amazon CloudFront的CDN表格")
           st.dataframe(dfACRequestsandTax)
        #    st.write("dfACRequestsNoTax总行数：", dfACRequestsNoTax.shape[0])
           st.write("dfACRequestsandTax总行数：", dfACRequestsandTax.shape[0],"---正确")
           st.write("总流量 ",dfACRequestsandTax['lineItem/UsageAmount'].sum())
        #    st.write("总流量 ",dfACRequestsandTax['lineItem/UsageAmount'].astype(float).sum()*1000*1000,"---正确")
           # 总费用：
           st.write("dfACRequestsandTax总费用：",dfACRequestsandTax['lineItem/UnblendedCost'].sum())

           st.dataframe(dfACRequestsandTax)


           # 计算累计值直到超过赠送请求数
           dfACRequestsandTax['累计请求数'] = dfACRequestsandTax['lineItem/UsageAmount'].cumsum()
           # 找到第一个超过赠送请求数的行
           target_row = dfACRequestsandTax[dfACRequestsandTax['累计请求数'] > send_total_usage].iloc[0] if not dfACRequestsandTax[dfACRequestsandTax['累计请求数'] > send_total_usage].empty else None
           st.write("target_row",target_row)
           if target_row is not None:
               row_index = dfACRequestsandTax[dfACRequestsandTax['累计请求数'] > send_total_usage].index[0]
               st.write("row_index",row_index)
               row_number = dfACRequestsandTax.index.get_loc(row_index)
               st.write(f"赠送请求数 {send_total_usage:,.0f} 在第 {row_number+1} 行用完")
               st.write(f"该行累计请求数: {target_row['累计请求数']:,.0f}")
               当行剩余部分 = target_row['累计请求数'] - send_total_usage
               st.write(f"超出部分: {当行剩余部分:,.0f}")

               # 将0到104行的lineItem/UsageAmount设为0
               dfACRequestsandTax.iloc[0:row_number, dfACRequestsandTax.columns.get_loc('lineItem/UsageAmount')] = 0
               dfACRequestsandTax.iloc[row_number, dfACRequestsandTax.columns.get_loc('lineItem/UsageAmount')] = 当行剩余部分
               st.write(f"第 {row_number + 1} 行调整后请求数: {当行剩余部分:,.0f}")
               dfACRequestsandTax['total累计请求数'] = dfACRequestsandTax['lineItem/UsageAmount'].cumsum()
               st.dataframe(dfACRequestsandTax)
               dfACRequestsandTax['lineItem/UnblendedCost'] = dfACRequestsandTax['lineItem/UsageAmount'] * dfACRequestsandTax['lineItem/UnblendedRate']

               st.write("计算后的CDN表格：")
               # 累计请求数：
               st.write("累计请求数：",dfACRequestsandTax['total累计请求数'].sum())
               st.write("总流量：",dfACRequestsandTax['lineItem/UsageAmount'].sum())
               st.write("总费用：",dfACRequestsandTax['lineItem/UnblendedCost'].sum())
               dfACRequestsandTax = dfACRequestsandTax[['bill/PayerAccountId','lineItem/UsageAccountId','lineItem/UsageStartDate','lineItem/UsageEndDate','lineItem/ProductCode','lineItem/UsageAmount','lineItem/UnblendedRate','lineItem/UnblendedCost','lineItem/LineItemDescription']]

               st.dataframe(dfACRequestsandTax)
           else:
               st.write("赠送请求数超过了所有请求的总和")
            
           # 创建ExcelWriter对象准备写入Excel文件
           output_filename = "迅雷CDN分析结果.xlsx"
           with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
               # 将不同类型的数据写入不同的sheet
               dfnoAC.to_excel(writer, sheet_name='非CloudFront服务', index=False)
               dfGBandOrigin.to_excel(writer, sheet_name='CloudFront-DTO', index=False)
               dfACRequestsandTax.to_excel(writer, sheet_name='CloudFront-CDN', index=False)
               
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
