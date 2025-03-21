import streamlit as st
import pandas as pd
import numpy as np
import zipfile
import io
from steamlitapp import adjust_column_width

def xunlei_smartchain_aws():
    st.title("迅雷-Smartchain-AWS")
    st.write("Create by Jackie Chen")

    # 上传文件
    uploaded_file = st.file_uploader("上传迅雷-Smartchain-AWS账单", type=["csv", "xlsx", "xls"])

    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1].lower()
        st.write(file_type)
        if file_type == 'csv':
            df = pd.read_csv(uploaded_file, low_memory=False)
        elif file_type in ['xlsx', 'xls']: 
            df = pd.read_excel(uploaded_file, low_memory=False)
        st.dataframe(df)
        st.write(df.shape[0],"--正确")
        # 筛选出lineItem/UsageAccountId =730335617227 以及 lineItem/LineItemType 不为 SppDiscount
        df = df[df['lineItem/UsageAccountId'].astype(str).isin(['730335617227'])]
        st.write(df.shape[0],"--正确")
        df = df[~df['lineItem/LineItemType'].isin(['SppDiscount'])]
        st.write(df.shape[0],"--正确")
        st.dataframe(df)


        # 查找所有包含resourceTags的列
        resource_tags_columns = [col for col in df.columns if 'resourceTags' in col]
        # 删除resource_tags_columns中包含'Name'的列
        resource_tags_columns = [col for col in resource_tags_columns if 'Name' not in col]

        # 创建结果DataFrame
        results = []
        none_total = 0.0  # 用于统计所有未匹配的行的总和
        
        # 对每个resourceTags列进行处理
        for tag_col in resource_tags_columns:
            # 找到该标签列中值为'bill'或者含有字符的行
            matched_mask = df[tag_col].notna() & ((df[tag_col].str.contains('bill', case=False, na=False)) | (df[tag_col].str.len() > 0))
            # 找到未匹配的行（空值或没有任何字符的行）
            # none_mask = df[tag_col].isna() | (df[tag_col].str.len() == 0)
            
            # 计算匹配行的UnblendedCost总和
            total_cost = df[matched_mask]['lineItem/UnblendedCost'].astype(float).sum()
            results.append({
                '标签': tag_col,
                '金额（美金）': '{:.10f}'.format(total_cost)
            })
            
            # 累加未匹配行的费用到none_total
           # none_total += df[none_mask]['lineItem/UnblendedCost'].astype(float).sum()
        
        
               # 计算df中lineItem/UnblendedCost列的和
        total_cost = df['lineItem/UnblendedCost'].astype(float).sum()
        st.write(f"总费用: {total_cost}")
       
        # 添加None类别的统计
        # results.append({
        #     '标签': 'None',
        #     '金额（美金）': '{:.10f}'.format(none_total)
        # })
        
        # 转换结果为DataFrame
        df_cost = pd.DataFrame(results)
        total_sum = sum(float(x) for x in df_cost['金额（美金）'])
        none_total = total_cost-total_sum
        df_cost.loc[len(df_cost)] = ['None', '{:.10f}'.format(none_total)]

        df_cost.loc[len(df_cost)] = ['总计', '{:.10f}'.format(total_cost)]

        # 添加总和行，同样保持10位小数
        #total_sum = sum(float(x) for x in df_cost['金额（美金）'])
        # df_cost.loc[len(df_cost)] = ['总计', '{:.10f}'.format(total_sum)]
        

        st.write("标签费用统计:")
        st.dataframe(df_cost)

        # 创建ExcelWriter对象
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_cost.to_excel(writer, sheet_name="标签费用统计", index=False)
            df.to_excel(writer, sheet_name="原始数据", index=False)

            # 调整每个sheet的列宽
            workbook = writer.book
            for sheet_name in workbook.sheetnames:
                worksheet = workbook[sheet_name]
                adjust_column_width(worksheet)

        # 将输出流位置重置到起点
        output.seek(0)

        st.download_button(
            label="下载标签费用统计",
            data=output.getvalue(), 
            file_name="标签费用统计.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


        # 下载按钮
        # st.download_button(label="下载标签费用统计", data=df_cost.to_csv(index=False), file_name="标签费用统计.csv")





    # 筛选出相关列bill/PayerAccountId，lineItem/UsageAccountId，lineItem/UsageStartDate，lineItem/UsageEndDate，lineItem/ProductCode，lineItem/UsageAmount，lineItem/UnblendedRate，lineItem/UnblendedCost，lineItem/LineItemDescription，product/pricingUnit，product/region，resourceTags/user
    # df = df[['bill/PayerAccountId', 'lineItem/UsageAccountId', 'lineItem/UsageStartDate', 'lineItem/UsageEndDate', 'lineItem/ProductCode', 'lineItem/UsageAmount', 'lineItem/UnblendedRate', 'lineItem/UnblendedCost', 'lineItem/LineItemDescription', 'product/pricingUnit', 'product/region', 'resourceTags/user']]
    # st.dataframe(df)
        




