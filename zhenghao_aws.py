import streamlit as st
import pandas as pd
import numpy as np
from steamlitapp import adjust_column_width
import io


def zhenghao_aws():
    st.title("正浩-AWS")
    st.write("Create by Jackie Chen")

    # 上传文件
    uploaded_file = st.file_uploader("上传正浩-AWS账单", type=["csv", "xlsx", "xls"])
    if uploaded_file is not None:
        # 添加 low_memory=False 参数来避免数据类型警告
        df = pd.read_csv(uploaded_file, low_memory=False)
        
        # 确保某些列被正确地处理为字符串类型
        string_columns = ['lineItem/UsageAccountId', 'product/ecu']  # 添加其他需要作为字符串处理的列
        df[string_columns] = df[string_columns].astype(str)
        
        st.write(df.shape[0],"--正确")
        # st.dataframe(df.head(1000))
        # 过滤 lineItem/UsageAccountId = 054732032387
        df = df[df['lineItem/UsageAccountId'].astype(str) == '54732032387']
        # st.dataframe(df.head(1000))
        # 过滤 lineItem/LineItemType 不等于 SppDiscount 和 SavingPlanNegation
        df = df[~df['lineItem/LineItemType'].isin(['SppDiscount', 'SavingsPlanNegation'])]
        st.write("54732032387的数据",df.shape[0],"--正确")
        st.dataframe(df)

        #这里重新做一份需求表的看看 20250320
        #（2）lineItem/LineItemDescription列：
# ①筛选：Redis, cache.r6g.large reserved instance applied并替换成$0.247 per Memory optimized r6g.large node hour running Redis
# ②筛选：MySQL, db.m6i.large reserved instance applied并替换成$ 0.203 per RDS db.m6i.large Single-AZ instance hour (or partial hour) running MySQL
# ③筛选：Aurora MySQL, db.r6g.2xl reserved instance applied并替换成$ 1.253 per RDS db.r6g.2xlarge Single-AZ instance hour (or partial hour) running Aurora MySQL
# 同时更新lineItem/UnblendedRate和lineItem/UnblendedCost列的数据lineItem/UnblendedCost列=lineItem/UsageAmount列*lineItem/UnblendedRate列
        df['lineItem/LineItemDescription'] = np.where(df['lineItem/LineItemDescription'].str.contains('Redis, cache.r6g.large reserved instance applied'), '$0.247 per Memory optimized r6g.large node hour running Redis', df['lineItem/LineItemDescription'])
        df['lineItem/LineItemDescription'] = np.where(df['lineItem/LineItemDescription'].str.contains('MySQL, db.m6i.large reserved instance applied'), '$ 0.203 per RDS db.m6i.large Single-AZ instance hour (or partial hour) running MySQL', df['lineItem/LineItemDescription'])
        df['lineItem/LineItemDescription'] = np.where(df['lineItem/LineItemDescription'].str.contains('Aurora MySQL, db.r6g.2xl reserved instance applied'), '$ 1.253 per RDS db.r6g.2xlarge Single-AZ instance hour (or partial hour) running Aurora MySQL', df['lineItem/LineItemDescription'])
        # df['lineItem/UnblendedRate']
        df['lineItem/UnblendedRate'] = np.where(df['lineItem/LineItemType'].isin(['DiscountedUsage']), df['pricing/publicOnDemandRate'], df['lineItem/UnblendedRate'])
        df['lineItem/UnblendedCost'] = np.where(df['lineItem/LineItemType'].isin(['DiscountedUsage']), df['pricing/publicOnDemandCost'], df['lineItem/UnblendedCost'])
        col = ['bill/PayerAccountId','lineItem/UsageAccountId','lineItem/UsageStartDate','lineItem/UsageEndDate','lineItem/ProductCode','lineItem/UsageAmount','lineItem/UnblendedRate','lineItem/UnblendedCost','lineItem/LineItemDescription','product/pricingUnit']
        
        df = df[col]
        # st.write("df[col]为str",df[col].dtypes)
        st.write(df.shape[0],"--正确")
        st.write(df['lineItem/UnblendedCost'].sum())
        st.dataframe(df)

        st.download_button(
            label="下载汇总文件",
            data=df.to_csv(index=False),
            file_name="正浩AWS账单.csv",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


        # 添加成功提示
        st.success("文件已准备好，请点击上方按钮下载")

        
        
        


        # 基于bill/BillingEntity 拆成AWS和  AWS Marketplace
        # AWS_df = df[df['bill/BillingEntity'] == 'AWS']
        
        # st.write("AWS类型的数据",AWS_df.shape[0],"--正确")
        # st.dataframe(AWS_df)
        # RI的类型折扣---》DiscountedUsage
        # AWS_DiscountedUsage_df = AWS_df[AWS_df['lineItem/LineItemType'].isin(['DiscountedUsage'])]
        # AWS_numeric_cols = ['lineItem/UsageAmount', 'lineItem/UnblendedRate', 'lineItem/UnblendedCost', 'pricing/publicOnDemandRate', 'pricing/publicOnDemandCost']
        # AWS_new_df = AWS_DiscountedUsage_df[AWS_numeric_cols + ['product/region','product/instanceType']+ ['product/deploymentOption']+['lineItem/ProductCode']+['pricing/term']+['lineItem/LineItemDescription']+['product/databaseEngine']].copy()
        # AWS_new_df[AWS_numeric_cols] = AWS_DiscountedUsage_df[AWS_numeric_cols].astype(float)
       
         #--------------------------过滤--------------------------------        
        #判断lineItem/LineItemDescription包含'reserved'且pricing/term包含'Reserved'的话，将该列的 'pricing/publicOnDemandRate'复制到lineItem/UnblendedRate, 'pricing/publicOnDemandCost'复制到'lineItem/UnblendedCost'
        # AWS_new_df['lineItem/UnblendedRate'] = np.where(AWS_new_df['lineItem/LineItemDescription'].str.contains('reserved') & AWS_new_df['pricing/term'].str.contains('Reserved'), AWS_new_df['pricing/publicOnDemandRate'], AWS_new_df['lineItem/UnblendedRate'])
        # AWS_new_df['lineItem/UnblendedCost'] = np.where(AWS_new_df['lineItem/LineItemDescription'].str.contains('reserved') & AWS_new_df['pricing/term'].str.contains('Reserved'), AWS_new_df['pricing/publicOnDemandCost'], AWS_new_df['lineItem/UnblendedCost'])
        # st.write("AWS_new_df为DiscountedUsage",AWS_new_df.shape[0],"--正确")
         # 计算 总 lineItem/UnblendedCost
        # st.write("AWS_new_df总lineItem/UnblendedCost",AWS_new_df['lineItem/UnblendedCost'].sum(),"--正确")
        # st.dataframe(AWS_new_df)

        # AWS_Other_df = AWS_df[~AWS_df['lineItem/LineItemType'].isin(['DiscountedUsage'])]
        # st.write("AWS_Other_df不为DiscountedUsage",AWS_Other_df.shape[0],"--正确")
        # st.write("AWS_Other_df总lineItem/UnblendedCost",AWS_Other_df['lineItem/UnblendedCost'].sum(),"--正确")
        # st.dataframe(AWS_Other_df)
        # 判断lineItem/ProductCode是AmazonRDS的话且pricing/term包含'Reserved'的话
        # lineItem/LineItemDescription :Aurora MySQL, db.r5.large reserved instance applied
        # lineItem/LineItemDescription修改后： USD 0.70 per RDS db.r5.xlarge Single-AZ instance hour (or partial hour) running Aurora MySQL
        # lineItem/LineItemDescription = USD + df[pricing/publicOnDemandRate] +per RDS +df[product/instanceType] +df[product/deploymentOption] +instance hour (or partial hour) running Aurora MySQL
        # AWS_new_df['lineItem/LineItemDescription'] = np.where(
        #     (AWS_new_df['lineItem/ProductCode'] == 'AmazonRDS') & (AWS_new_df['pricing/term'].str.contains('Reserved')), 
        #     'USD ' + AWS_new_df['pricing/publicOnDemandRate'].astype(str) + ' per RDS ' + AWS_new_df['product/instanceType'] + ' ' + AWS_new_df['product/deploymentOption'] + ' instance hour (or partial hour) running ' + AWS_new_df['product/databaseEngine'], 
        #     AWS_new_df['lineItem/LineItemDescription']
        # )
        # 判断lineItem/ProductCode是AmazonEC2的话且pricing/term包含'Reserved'的话
        # lineItem/LineItemDescription :Linux/UNIX (Amazon VPC), t2.xlarge reserved instance applied
        # lineItem/LineItemDescription修改后： $0.192 per On Demand Linux t3.xlarge Instance Hour
        # lineItem/LineItemDescription = $ + df[pricing/publicOnDemandRate] + per On Demand Linux + df[product/instanceType] + Instance Hour
        # AWS_new_df['lineItem/LineItemDescription'] = np.where(
        #     (AWS_new_df['lineItem/ProductCode'] == 'AmazonEC2') & (AWS_new_df['pricing/term'].str.contains('Reserved')),
        #    '$' + AWS_new_df['pricing/publicOnDemandRate'].astype(str) + ' per On Demand Linux ' + AWS_new_df['product/instanceType'] + ' Instance Hour', 
        #     AWS_new_df['lineItem/LineItemDescription']
        # )
        # st.write("AWS_new_df过滤后的数据",AWS_new_df.shape[0])
        # st.dataframe(AWS_new_df)

        # 进行AWS_new_df的lineItem/ProductCode 含有suppport 也要拆子表
        # AWS_support_df = AWS_Other_df[AWS_Other_df['lineItem/ProductCode'].str.contains('Su')]
        # st.write("AWS_support_df",AWS_support_df.shape[0],"--正确")
        # st.dataframe(AWS_support_df)
        # AWS_Other_df = AWS_Other_df[~AWS_Other_df['lineItem/ProductCode'].str.contains('Su')]
        # st.write("AWS_Other_df",AWS_Other_df.shape[0],"--正确")
        # st.dataframe(AWS_Other_df)
        



        # AWS_Marketplace_df = df[df['bill/BillingEntity'] == 'AWS Marketplace']
        # st.write("AWS_Marketplace_df",AWS_Marketplace_df.shape[0],"--正确")
        # st.dataframe(AWS_Marketplace_df)


        # AWS_new_df = pd.concat([AWS_Other_df,AWS_new_df])
        # st.write("AWS_Other_df",AWS_new_df.shape[0],"--正确")
        # st.dataframe(AWS_new_df)

       





