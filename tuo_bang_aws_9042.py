import streamlit as st
import pandas as pd
import numpy as np
import zipfile
import io
from steamlitapp import adjust_column_width




# lineItem/UsageAmount  资源使用数量
# lineItem/UnblendedRate  实际单价
# lineItem/UnblendedCost  实际总价
# lineItem/LineItemDescription  描述
# pricing/publicOnDemandRate  按需单价
# pricing/publicOnDemandCost 按需总价
# pricing/term     计费类型
# pricing/unit  单位

def tuo_bang_aws_9042():
    st.title("拓邦-AWS-9042")
    st.write("Create by Jackie Chen")
    uploaded_file = st.file_uploader("上传拓邦-AWS原始账单", type=["csv", "xlsx", "xls", "zip"])
    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1].lower()
        
        if file_type == 'zip':
            # 处理zip文件
            with zipfile.ZipFile(uploaded_file) as z:
                # 获取zip中的所有文件名
                csv_files = [f for f in z.namelist() if f.endswith('.csv')]
                if not csv_files:
                    st.error("ZIP文件中没有找到CSV文件！")
                    return
                
                # 如果有多个CSV文件，让用户选择
                if len(csv_files) > 1:
                    selected_file = st.selectbox("请选择要处理的CSV文件：", csv_files)
                else:
                    selected_file = csv_files[0]
                
                # 读取选中的CSV文件
                with z.open(selected_file) as csv_file:
                    df = pd.read_csv(csv_file)
        elif file_type == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_type in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file)
        st.dataframe(df)
        st.write(df.shape[0])
      
        # 筛选 lineItem/UsageAccountId ==904213552531
        df9042 = df[df['lineItem/UsageAccountId'] == 904213552531]
        df9042 = df9042[df9042['lineItem/LineItemType'] != 'DistributorDiscount']
        st.write("904213552531数据")
        st.write(df9042.shape[0])
        st.dataframe(df9042)
  
        
        #pricing/unit列筛选：Hrs
        df_hrs = df9042[df9042['pricing/unit'] == 'Hrs']
        
        st.write("Hrs数据")
        st.write(df_hrs.shape[0])
        st.dataframe(df_hrs)

        #---------------------------------单独的数据---------------------------------  
        # 只对需要转换为浮点数的列进行转换
        numeric_cols = ['lineItem/UsageAmount', 'lineItem/UnblendedRate', 'lineItem/UnblendedCost', 'pricing/publicOnDemandRate', 'pricing/publicOnDemandCost']
        new_df = df_hrs[numeric_cols + ['product/instanceType']+ ['product/deploymentOption']+['lineItem/ProductCode']+['pricing/term']+['lineItem/LineItemDescription']+['product/databaseEngine']].copy()
        new_df[numeric_cols] = new_df[numeric_cols].astype(float)
        st.write("数据清洗")
        st.write(new_df.shape[0])
        st.dataframe(new_df)
        #lineItem/ProductCode列筛选：AmazonRDS和AmazonEC2
        new_df = new_df[new_df['lineItem/ProductCode'].isin(['AmazonRDS', 'AmazonEC2'])]
        st.write(new_df.shape[0])
        st.write("RDS和EC2数据")
        st.dataframe(new_df)
        #--------------------------过滤--------------------------------        
        #判断lineItem/LineItemDescription包含'reserved'且pricing/term包含'Reserved'的话，将该列的 'pricing/publicOnDemandRate'复制到lineItem/UnblendedRate, 'pricing/publicOnDemandCost'复制到'lineItem/UnblendedCost'
        new_df['lineItem/UnblendedRate'] = np.where(new_df['lineItem/LineItemDescription'].str.contains('reserved') & new_df['pricing/term'].str.contains('Reserved'), new_df['pricing/publicOnDemandRate'], new_df['lineItem/UnblendedRate'])
        new_df['lineItem/UnblendedCost'] = np.where(new_df['lineItem/LineItemDescription'].str.contains('reserved') & new_df['pricing/term'].str.contains('Reserved'), new_df['pricing/publicOnDemandCost'], new_df['lineItem/UnblendedCost'])
        

        # 判断lineItem/ProductCode是AmazonRDS的话且pricing/term包含'Reserved'的话
        # lineItem/LineItemDescription :Aurora MySQL, db.r5.large reserved instance applied
        # lineItem/LineItemDescription修改后： USD 0.70 per RDS db.r5.xlarge Single-AZ instance hour (or partial hour) running Aurora MySQL
        # lineItem/LineItemDescription = USD + df[pricing/publicOnDemandRate] +per RDS +df[product/instanceType] +df[product/deploymentOption] +instance hour (or partial hour) running Aurora MySQL
        new_df['lineItem/LineItemDescription'] = np.where(
            (new_df['lineItem/ProductCode'] == 'AmazonRDS') & (new_df['pricing/term'].str.contains('Reserved')), 
            'USD ' + new_df['pricing/publicOnDemandRate'].astype(str) + ' per RDS ' + new_df['product/instanceType'] + ' ' + new_df['product/deploymentOption'] + ' instance hour (or partial hour) running ' + new_df['product/databaseEngine'], 
            new_df['lineItem/LineItemDescription']
        )
        # 判断lineItem/ProductCode是AmazonEC2的话且pricing/term包含'Reserved'的话
        # lineItem/LineItemDescription :Linux/UNIX (Amazon VPC), t2.xlarge reserved instance applied
        # lineItem/LineItemDescription修改后： $0.192 per On Demand Linux t3.xlarge Instance Hour
        # lineItem/LineItemDescription = $ + df[pricing/publicOnDemandRate] + per On Demand Linux + df[product/instanceType] + Instance Hour
        new_df['lineItem/LineItemDescription'] = np.where(
            (new_df['lineItem/ProductCode'] == 'AmazonEC2') & (new_df['pricing/term'].str.contains('Reserved')),
            '$' + new_df['pricing/publicOnDemandRate'].astype(str) + ' per On Demand Linux ' + new_df['product/instanceType'] + ' Instance Hour', 
            new_df['lineItem/LineItemDescription']
        )
 
        st.write("保留数据")
        st.write(new_df.shape[0])
        st.dataframe(new_df)
        # 下载
        st.download_button(label="下载", data=new_df.to_csv(index=False), file_name="拓邦分析后的数据.csv")

        ## df9042表中数据如果pricing/unit列包含Hrs，lineItem/ProductCode包含AmazonRDS和AmazonEC2则要替换
        # 修复条件赋值语法错误，使用loc正确选择行并赋值
        # 更新 UnblendedRate
        condition = df9042['pricing/unit'].isin(['Hrs']) & df9042['lineItem/ProductCode'].isin(['AmazonRDS', 'AmazonEC2']) & df9042['lineItem/LineItemDescription'].str.contains('reserved') & df9042['pricing/term'].str.contains('Reserved')
        df9042.loc[condition, 'lineItem/UnblendedRate'] = df9042.loc[condition, 'pricing/publicOnDemandRate']
        
        # 更新 UnblendedCost
        df9042.loc[condition, 'lineItem/UnblendedCost'] = df9042.loc[condition, 'pricing/publicOnDemandCost']
        
        # 更新 AmazonRDS 的 LineItemDescription
        rds_condition = condition & (df9042['lineItem/ProductCode'] == 'AmazonRDS')
        df9042.loc[rds_condition, 'lineItem/LineItemDescription'] = 'USD ' + df9042.loc[rds_condition, 'pricing/publicOnDemandRate'].astype(str) + ' per RDS ' + df9042.loc[rds_condition, 'product/instanceType'] + ' ' + df9042.loc[rds_condition, 'product/deploymentOption'] + ' instance hour (or partial hour) running ' + df9042.loc[rds_condition, 'product/databaseEngine']
        
        # 更新 AmazonEC2 的 LineItemDescription
        ec2_condition = condition & (df9042['lineItem/ProductCode'] == 'AmazonEC2')
        df9042.loc[ec2_condition, 'lineItem/LineItemDescription'] = '$' + df9042.loc[ec2_condition, 'pricing/publicOnDemandRate'].astype(str) + ' per On Demand Linux ' + df9042.loc[ec2_condition, 'product/instanceType'] + ' Instance Hour'

        # 计算 总数 lineItem/UnblendedCost的第一列
        st.write()
        st.write("总数",df9042['lineItem/UnblendedCost'].sum())
        # 获取df9042的bill/PayerAccountId	lineItem/UsageAccountId	lineItem/UsageStartDate	lineItem/UsageEndDate	lineItem/ProductCode	lineItem/UsageAmount	lineItem/UnblendedRate	lineItem/UnblendedCost	lineItem/LineItemDescription	pricing/Unit
        df9042_new = df9042[['bill/PayerAccountId','lineItem/UsageAccountId','lineItem/UsageStartDate','lineItem/UsageEndDate','lineItem/ProductCode','lineItem/UsageAmount','lineItem/UnblendedRate','lineItem/UnblendedCost','lineItem/LineItemDescription','pricing/unit','lineItem/LineItemType']]
        # 调整每个sheet的列宽
        st.dataframe(df9042_new)
        st.download_button(
            label="下载汇总文件",
            data=df9042_new.to_csv(index=False),
            file_name="拓邦分析后的数据.csv",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # 添加成功提示
        st.success("文件已准备好，请点击上方按钮下载")
    
    
    
