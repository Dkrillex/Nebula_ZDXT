import streamlit as st
import pandas as pd
import numpy as np
import zipfile


def xunlei_smartchain_aws():
    st.title("迅雷-Smartchain-AWS")
    st.write("Create by Jackie Chen")

    # 上传文件
    uploaded_file = st.file_uploader("上传迅雷-Smartchain-AWS账单", type=["csv", "xlsx", "xls"])

    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1].lower()
        if file_type == 'csv':
            # df = pd.read_csv(uploaded_file)
            # 获取工作表为2025.2(7303)的表
            df = pd.read_excel(uploaded_file, sheet_name='2025.2(7303)')     
        elif file_type in ['xlsx', 'xls']:
            # df = pd.read_excel(uploaded_file)
            # 获取工作表为2025.2(7303)的表
            df = pd.read_excel(uploaded_file, sheet_name='2025.2(7303)')
            # 去掉第一行,把第二行作为列头
            df.columns = df.iloc[0]
            df = df.iloc[1:]
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

        # 下载按钮
        st.download_button(label="下载标签费用统计", data=df_cost.to_csv(index=False), file_name="标签费用统计.csv")





    # 筛选出相关列bill/PayerAccountId，lineItem/UsageAccountId，lineItem/UsageStartDate，lineItem/UsageEndDate，lineItem/ProductCode，lineItem/UsageAmount，lineItem/UnblendedRate，lineItem/UnblendedCost，lineItem/LineItemDescription，product/pricingUnit，product/region，resourceTags/user
    # df = df[['bill/PayerAccountId', 'lineItem/UsageAccountId', 'lineItem/UsageStartDate', 'lineItem/UsageEndDate', 'lineItem/ProductCode', 'lineItem/UsageAmount', 'lineItem/UnblendedRate', 'lineItem/UnblendedCost', 'lineItem/LineItemDescription', 'product/pricingUnit', 'product/region', 'resourceTags/user']]
    # st.dataframe(df)
        




