import streamlit as st
import pandas as pd
import numpy as np
import zipfile
import io
from steamlitapp import adjust_column_width


def tuo_bang_aws_3677():
    st.title("拓邦-AWS-3677")
    st.write("Create by Jackie Chen")
    uploaded_file = st.file_uploader("上传拓邦-AWS-3677原始账单", type=["csv", "xlsx", "xls", "zip"], accept_multiple_files=False)
    
    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1].lower()
        
        # 设置pandas选项以优化内存使用
        pd.options.mode.chained_assignment = None
        
        try:
            if file_type == 'csv':
                df = pd.read_csv(uploaded_file)
                st.write(df.shape[1])                
                # 显示数据统计信息
                st.write(f"数据行数: {len(df)}")
                st.write("数据预览:")
                st.dataframe(df.head(1000))
                # lineItem/UsageAccountId转数字再过滤 =367754112809
                df = df[df['lineItem/UsageAccountId'].astype(str) == '367754112809']
                st.write(f"数据行数: {len(df)}")
                st.write("数据预览:")
                st.dataframe(df.head(1000))
                # 东京的表 product/region = ap-northeast-1
                DJ_df = df[df['product/region'] == 'ap-northeast-1']
                #我只需要这些列  bill/PayerAccountId	lineItem/UsageAccountId	lineItem/UsageStartDate	lineItem/UsageEndDate	lineItem/ProductCode	lineItem/UsageAmount	lineItem/UnblendedRate	lineItem/UnblendedCost	lineItem/LineItemDescription	pricing/unit	product/region
                DJ_df=DJ_df[['bill/PayerAccountId','lineItem/UsageAccountId','lineItem/UsageStartDate','lineItem/UsageEndDate','lineItem/ProductCode','lineItem/UsageAmount','lineItem/UnblendedRate','lineItem/UnblendedCost','lineItem/LineItemDescription','pricing/unit','product/region']]
                st.write(f"东京数据行数: {len(DJ_df)}")
                st.write(f"东京数据总费用: {DJ_df['lineItem/UnblendedCost'].sum()}")
                st.write("东京数据预览:")
                st.dataframe(DJ_df)

                #------------------其他修改后的资源----------------------------------------------------
                Other_new_df = df[(df['product/region'] != 'ap-northeast-1') & (df['lineItem/LineItemType'] != 'SppDiscount')]
                EC2_condition = Other_new_df['lineItem/ProductCode'].isin(['AmazonEC2']) & Other_new_df['pricing/unit'].isin(['Hrs'])
                GP3_condition = Other_new_df['lineItem/ProductCode'].isin(['AmazonEC2']) & Other_new_df['pricing/unit'].isin(['GB-Mo'])
                RDS_condition = Other_new_df['lineItem/ProductCode'].isin(['AmazonRDS']) & Other_new_df['pricing/unit'].isin(['Hrs'])
                # testdf=Other_new_df[Other_new_df['lineItem/ProductCode'].isin(['AmazonEC2'])& Other_new_df['pricing/unit'].isin(['Hrs'])]
                # st.dataframe(testdf)
                
                # 查看EC2_condition数据
                st.write(f"未修改的EC2_condition数据行数: {len(Other_new_df[EC2_condition])}")
                st.write("未修改的EC2_condition数据预览:")
                st.dataframe(Other_new_df[EC2_condition].head(1000))
                # 查看RDS_condition的数据
                st.write(f"未修改的RDS_condition数据行数: {len(Other_new_df[RDS_condition])}")
                st.write("未修改的RDS_condition数据预览:")
                st.dataframe(Other_new_df[RDS_condition].head(1000))
                 # 查看GP3_condition的数据
                st.write(f"未修改的GP3_condition数据行数: {len(Other_new_df[GP3_condition])}")
                st.write("未修改的GP3_condition数据预览:")
                st.dataframe(Other_new_df[GP3_condition].head(1000))

                Other_new_df.loc[EC2_condition, 'lineItem/UnblendedRate'] = Other_new_df.loc[EC2_condition, 'pricing/publicOnDemandRate']
                Other_new_df.loc[EC2_condition, 'lineItem/UnblendedRate'] = Other_new_df.loc[EC2_condition, 'pricing/publicOnDemandRate'].fillna(0)
                Other_new_df.loc[EC2_condition, 'lineItem/UnblendedCost'] = Other_new_df.loc[EC2_condition, 'pricing/publicOnDemandCost']
                Other_new_df.loc[RDS_condition, 'lineItem/UnblendedRate'] = Other_new_df.loc[RDS_condition, 'pricing/publicOnDemandRate']
                Other_new_df.loc[RDS_condition, 'lineItem/UnblendedCost'] = Other_new_df.loc[RDS_condition, 'pricing/publicOnDemandCost']
                EC2_update_condition = EC2_condition & Other_new_df['lineItem/LineItemDescription'].str.contains('reserved') & Other_new_df['pricing/term'].str.contains('Reserved')    
                RDS_update_condition = RDS_condition & Other_new_df['lineItem/LineItemDescription'].str.contains('reserved') & Other_new_df['pricing/term'].str.contains('Reserved')
                Other_new_df.loc[EC2_update_condition, 'lineItem/LineItemDescription'] = '$' + Other_new_df.loc[EC2_update_condition, 'pricing/publicOnDemandRate'].astype(str) + ' per On Demand Linux ' + Other_new_df.loc[EC2_update_condition, 'product/instanceType'] + ' Instance Hour'
                Other_new_df.loc[RDS_update_condition, 'lineItem/LineItemDescription'] = 'USD ' + Other_new_df.loc[RDS_update_condition, 'pricing/publicOnDemandRate'].astype(str) + ' per RDS ' + Other_new_df.loc[RDS_update_condition, 'product/instanceType'] + ' ' + Other_new_df.loc[RDS_update_condition, 'product/deploymentOption'] + ' instance hour (or partial hour) running ' + Other_new_df.loc[RDS_update_condition, 'product/databaseEngine']
                
                # 查看修改后的EC2_update_condition数据
                st.write(f"修改后的EC2_update_condition数据行数: {len(Other_new_df[EC2_update_condition])}")
                st.write("修改后的EC2_update_condition数据预览:")
                st.dataframe(Other_new_df[EC2_update_condition].head(1000))
                # 查看修改后的RDS_update_condition数据  
                st.write(f"修改后的RDS_update_condition数据行数: {len(Other_new_df[RDS_update_condition])}")
                st.write("修改后的RDS_update_condition数据预览:")
                st.dataframe(Other_new_df[RDS_update_condition].head(1000))
                # Other_new_df筛选出EC2_update_condition 且lineItem/UsageAmount 为 672 的数据
                EC2_update_condition_672 = EC2_condition & (Other_new_df['lineItem/ResourceId'] == 'i-0b60b7c5f1520f34c')& (Other_new_df['product/region'] == 'eu-central-1')
                st.write(f"EC2_update_condition_672数据行数: {len(Other_new_df[EC2_update_condition_672])}")
                st.write("EC2_update_condition_672数据预览:")
                st.dataframe(Other_new_df[EC2_update_condition_672].head(1000))
                # Other_new_df筛选出RDS_update_condition 且lineItem/UsageAmount 为 672 的数据
                RDS_update_condition_672 = RDS_condition & (Other_new_df['lineItem/ResourceId'] == 'arn:aws:rds:eu-central-1:367754112809:db:p1bu-instance-1')& (Other_new_df['product/region'] == 'eu-central-1')
                st.write(f"RDS_update_condition_672数据行数: {len(Other_new_df[RDS_update_condition_672])}")
                st.write("RDS_update_condition_672数据预览:")
                st.dataframe(Other_new_df[RDS_update_condition_672].head(1000))
                # Other_new_df筛选出GP3_update_condition 且lineItem/UsageAmount 为 672 的数据
                GP3_update_condition_672 = GP3_condition & (Other_new_df['lineItem/ResourceId'] == 'vol-00c1dc7e10e3fa97a')& (Other_new_df['product/region'] == 'eu-central-1')
                st.write(f"GP3_update_condition_672数据行数: {len(Other_new_df[GP3_update_condition_672])}")
                st.write("GP3_update_condition_672数据预览:")
                st.dataframe(Other_new_df[GP3_update_condition_672].head(1000))
                #--------------------新增资源--------------------------------
                insert_df = pd.DataFrame()  # 创建一个空的 DataFrame
                insert_df=pd.concat([insert_df,Other_new_df[EC2_update_condition_672],Other_new_df[RDS_update_condition_672],Other_new_df[GP3_update_condition_672]],ignore_index=True)
                #bill/PayerAccountId	lineItem/UsageAccountId	lineItem/UsageStartDate	lineItem/UsageEndDate	lineItem/ProductCode	lineItem/UsageAmount	lineItem/UnblendedRate	lineItem/UnblendedCost	lineItem/LineItemDescription	product/region	pricing/unit
                insert_df=insert_df[['bill/PayerAccountId','lineItem/UsageAccountId','lineItem/UsageStartDate','lineItem/UsageEndDate','lineItem/ProductCode','lineItem/UsageAmount','lineItem/UnblendedRate','lineItem/UnblendedCost','lineItem/LineItemDescription','product/region','pricing/unit']]
                st.write(f"新增资源数据行数: {len(insert_df)}")
                st.write(f"新增资源数据总费用: {insert_df['lineItem/UnblendedCost'].sum()}")
                st.dataframe(insert_df)

                Other_new_df=Other_new_df[~((EC2_update_condition_672) | (RDS_update_condition_672)|(GP3_update_condition_672))]
                #我只需要这些列 bill/PayerAccountId	lineItem/UsageAccountId	lineItem/UsageStartDate	lineItem/UsageEndDate	lineItem/ProductCode	lineItem/UsageAmount	lineItem/UnblendedRate	lineItem/UnblendedCost	lineItem/LineItemDescription	pricing/unit	product/region
                Other_new_df=Other_new_df[['bill/PayerAccountId','lineItem/UsageAccountId','lineItem/UsageStartDate','lineItem/UsageEndDate','lineItem/ProductCode','lineItem/UsageAmount','lineItem/UnblendedRate','lineItem/UnblendedCost','lineItem/LineItemDescription','pricing/unit','product/region']]
                st.write(f"其他资源数据行数: {len(Other_new_df)}")
                st.write("其他资源数据预览:")
                st.dataframe(Other_new_df.head(1000))
                st.write(f"其他数据总费用: {Other_new_df['lineItem/UnblendedCost'].sum()}")
              
                

               

                # st.write(f"新增资源数据行数: {len(insert_df)}")
                # st.dataframe(insert_df)
               
                # 添加数据下载按钮
                # csv = EC2_new_df.to_csv(index=False)
                # st.download_button(
                #     label="下载处理后的数据",
                #     data=csv,
                #     file_name="processed_data.csv",
                #     mime="text/csv"
                # )
            output = io.BytesIO()

              # 创建ExcelWriter对象
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # 写入各个数据表
                DJ_df.to_excel(writer, sheet_name="东京", index=False)
                Other_new_df.to_excel(writer, sheet_name="其他资源", index=False)
                # RDS_new_df.to_excel(writer, sheet_name="RDS", index=False)
                insert_df.to_excel(writer, sheet_name="新增资源", index=False)

                # 调整每个sheet的列宽
                workbook = writer.book  
                for sheet_name in workbook.sheetnames:
                    worksheet = workbook[sheet_name]
                    adjust_column_width(worksheet)


                 # 将输出流位置重置到起点
            output.seek(0)

            st.download_button(
                label="下载处理后的数据",
                data=output.getvalue(),
                file_name="拓邦-AWS-3677.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.success("文件已准备好，请点击上方按钮下载")

                
                
        except Exception as e:
            st.error(f"处理文件时出错: {str(e)}")
            st.error("请确保文件格式正确且包含必要的列")
                
                
                
                
                
