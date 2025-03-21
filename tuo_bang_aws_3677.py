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
                # bill/PayerAccountId	lineItem/UsageAccountId	lineItem/UsageStartDate	lineItem/UsageEndDate	lineItem/ProductCode	lineItem/UsageAmount	lineItem/UnblendedRate	lineItem/UnblendedCost	lineItem/LineItemDescription	pricing/unit	product/region
                DJ_df=DJ_df[['bill/PayerAccountId','lineItem/UsageAccountId','lineItem/UsageStartDate','lineItem/UsageEndDate','lineItem/ProductCode','lineItem/UsageAmount','lineItem/UnblendedRate','lineItem/UnblendedCost','lineItem/LineItemDescription','pricing/unit','product/region']]
                st.write(f"东京数据行数: {len(DJ_df)}")
                st.write(DJ_df['lineItem/UnblendedCost'].sum())
                st.write("东京数据预览:")
                st.dataframe(DJ_df)

                #--------------------其他资源单独修改的----------------------------------------------------
                # Other_df= df[df['product/region'] != 'ap-northeast-1']
                #   #pricing/unit列筛选：Hrs
                # Other_df =Other_df[Other_df['pricing/unit'] == 'Hrs']
                # st.write(f"Hrs数据行数: {len(Other_df)}")
                # st.write("Hrs数据预览:")
                # st.dataframe(Other_df.head(1000))
                  #lineItem/ProductCode列筛选：AmazonRDS和AmazonEC2
        #         EC2_df = Other_df[Other_df['lineItem/ProductCode'].isin(['AmazonEC2'])]
        #         st.write(f"AmazonRDS和AmazonEC2数据行数: {len(EC2_df)}")
        #         st.write("AmazonRDS和AmazonEC2数据预览:")
        #         st.dataframe(EC2_df.head(1000))
        #         EC2_numeric_cols = ['lineItem/UsageAmount', 'lineItem/UnblendedRate', 'lineItem/UnblendedCost', 'pricing/publicOnDemandRate', 'pricing/publicOnDemandCost']
        #         EC2_new_df = EC2_df[EC2_numeric_cols + ['product/region','product/instanceType']+ ['product/deploymentOption']+['lineItem/ProductCode']+['pricing/term']+['lineItem/LineItemDescription']+['product/databaseEngine']].copy()
        #         EC2_new_df[EC2_numeric_cols] = EC2_new_df[EC2_numeric_cols].astype(float)
        #         EC2_new_df['lineItem/UnblendedCost'] = EC2_new_df['pricing/publicOnDemandCost']
        #         EC2_new_df['lineItem/UnblendedRate'] = EC2_new_df['pricing/publicOnDemandRate']

        #         EC2_new_df['lineItem/UnblendedRate'] = np.where(EC2_new_df['lineItem/LineItemDescription'].str.contains('reserved') & EC2_new_df['pricing/term'].str.contains('Reserved'), EC2_new_df['pricing/publicOnDemandRate'], EC2_new_df['lineItem/UnblendedRate'])
        #         EC2_new_df['lineItem/UnblendedCost'] = np.where(EC2_new_df['lineItem/LineItemDescription'].str.contains('reserved') & EC2_new_df['pricing/term'].str.contains('Reserved'), EC2_new_df['pricing/publicOnDemandCost'], EC2_new_df['lineItem/UnblendedCost'])
        

        # # 判断lineItem/ProductCode是AmazonRDS的话且pricing/term包含'Reserved'的话
        # # lineItem/LineItemDescription :Aurora MySQL, db.r5.large reserved instance applied
        # # lineItem/LineItemDescription修改后： USD 0.70 per RDS db.r5.xlarge Single-AZ instance hour (or partial hour) running Aurora MySQL
        # # lineItem/LineItemDescription = USD + df[pricing/publicOnDemandRate] +per RDS +df[product/instanceType] +df[product/deploymentOption] +instance hour (or partial hour) running Aurora MySQL
        #         EC2_new_df['lineItem/LineItemDescription'] = np.where(
        #         (EC2_new_df['lineItem/ProductCode'] == 'AmazonRDS') & (EC2_new_df['pricing/term'].str.contains('Reserved')), 
        #         'USD ' + EC2_new_df['pricing/publicOnDemandRate'].astype(str) + ' per RDS ' + EC2_new_df['product/instanceType'] + ' ' + EC2_new_df['product/deploymentOption'] + ' instance hour (or partial hour) running ' + EC2_new_df['product/databaseEngine'], 
        #         EC2_new_df['lineItem/LineItemDescription']
        #         )
        # # 判断lineItem/ProductCode是AmazonEC2的话且pricing/term包含'Reserved'的话
        # # lineItem/LineItemDescription :Linux/UNIX (Amazon VPC), t2.xlarge reserved instance applied
        # # lineItem/LineItemDescription修改后： $0.192 per On Demand Linux t3.xlarge Instance Hour
        # # lineItem/LineItemDescription = $ + df[pricing/publicOnDemandRate] + per On Demand Linux + df[product/instanceType] + Instance Hour
        #         EC2_new_df['lineItem/LineItemDescription'] = np.where(
        #         (EC2_new_df['lineItem/ProductCode'] == 'AmazonEC2') & (EC2_new_df['pricing/term'].str.contains('Reserved')),
        #         '$' + EC2_new_df['pricing/publicOnDemandRate'].astype(str) + ' per On Demand Linux ' + EC2_new_df['product/instanceType'] + ' Instance Hour', 
        #         EC2_new_df['lineItem/LineItemDescription']
        #         )
        #         st.write(f"数据预览:{len(EC2_new_df)}")
        #         st.dataframe(EC2_new_df)
        #         # 筛选出lineItem/UnblendedRate 为 0.194 的数据
        #         single_df = EC2_new_df[EC2_new_df['lineItem/UnblendedRate'] == 0.194]
        #         insert_df=single_df

        #         st.write(f"EC2insert_df新增资源数据行数: {len(insert_df)}")
        #         st.dataframe(insert_df)


        #         st.write(f"lineItem/UnblendedRate 为 0.194 数据行数: {len(single_df)}")
        #         st.write("lineItem/UnblendedRate 为 0.194 数据预览:")
        #         st.dataframe(single_df.head(1000))
        #         # new_df去掉single_df
        #         EC2_new_df = EC2_new_df[EC2_new_df['lineItem/UnblendedRate'] != 0.194]
        #         st.write(f"lineItem/UnblendedRate 为 0.194 数据行数: {len(EC2_new_df)}")
        #         st.write("lineItem/UnblendedRate 为 0.194 数据预览:")
        #         st.dataframe(EC2_new_df.head(1000))


        #         RDS_df = Other_df[Other_df['lineItem/ProductCode'].isin(['AmazonRDS'])]
        #         st.write(f"AmazonRDS数据行数: {len(RDS_df)}")
        #         st.write("AmazonRDS数据预览:")
        #         st.dataframe(RDS_df.head(1000))
        #         RDS_numeric_cols = ['lineItem/UsageAmount', 'lineItem/UnblendedRate', 'lineItem/UnblendedCost', 'pricing/publicOnDemandRate', 'pricing/publicOnDemandCost']
        #         RDS_new_df = RDS_df[RDS_numeric_cols + ['product/region','product/instanceType']+ ['product/deploymentOption']+['lineItem/ProductCode']+['pricing/term']+['lineItem/LineItemDescription']+['product/databaseEngine']].copy()
        #         RDS_new_df[RDS_numeric_cols] = RDS_new_df[RDS_numeric_cols].astype(float)
        #         RDS_new_df['lineItem/UnblendedCost'] = RDS_new_df['pricing/publicOnDemandCost']
        #         RDS_new_df['lineItem/UnblendedRate'] = RDS_new_df['pricing/publicOnDemandRate']

        #         RDS_new_df['lineItem/UnblendedRate'] = np.where(RDS_new_df['lineItem/LineItemDescription'].str.contains('reserved') & RDS_new_df['pricing/term'].str.contains('Reserved'), RDS_new_df['pricing/publicOnDemandRate'], RDS_new_df['lineItem/UnblendedRate'])
        #         RDS_new_df['lineItem/UnblendedCost'] = np.where(RDS_new_df['lineItem/LineItemDescription'].str.contains('reserved') & RDS_new_df['pricing/term'].str.contains('Reserved'), RDS_new_df['pricing/publicOnDemandCost'], RDS_new_df['lineItem/UnblendedCost'])
        

        # # 判断lineItem/ProductCode是AmazonRDS的话且pricing/term包含'Reserved'的话
        # # lineItem/LineItemDescription :Aurora MySQL, db.r5.large reserved instance applied
        # # lineItem/LineItemDescription修改后： USD 0.70 per RDS db.r5.xlarge Single-AZ instance hour (or partial hour) running Aurora MySQL
        # # lineItem/LineItemDescription = USD + df[pricing/publicOnDemandRate] +per RDS +df[product/instanceType] +df[product/deploymentOption] +instance hour (or partial hour) running Aurora MySQL
        #         RDS_new_df['lineItem/LineItemDescription'] = np.where(
        #         (RDS_new_df['lineItem/ProductCode'] == 'AmazonRDS') & (RDS_new_df['pricing/term'].str.contains('Reserved')), 
        #         'USD ' + RDS_new_df['pricing/publicOnDemandRate'].astype(str) + ' per RDS ' + RDS_new_df['product/instanceType'] + ' ' + RDS_new_df['product/deploymentOption'] + ' instance hour (or partial hour) running ' + RDS_new_df['product/databaseEngine'], 
        #         RDS_new_df['lineItem/LineItemDescription']
        #         )
        #         st.write(f"数据预览:{len(RDS_new_df)}")
        #         st.dataframe(RDS_new_df)
        #         single_df = RDS_new_df[RDS_new_df['lineItem/UnblendedRate'] != 0.35]
        #         st.write(f"lineItem/UnblendedRate 不为 0.35 数据行数: {len(single_df)}")
        #         st.write("lineItem/UnblendedRate 不为 0.35 数据预览:")
        #         st.dataframe(single_df.head(1000))
        #         # 将single_df添加到insert_df
        #         insert_df = pd.concat([insert_df, single_df], ignore_index=True)
        #         st.write(f"RDSinsert_df新增资源数据行数: {len(insert_df)}")
        #         st.dataframe(insert_df)
        
        #         # new_df去掉single_df
        #         RDS_new_df = RDS_new_df[RDS_new_df['lineItem/UnblendedRate'] == 0.35]
        #         st.write(f"lineItem/UnblendedRate 为 0.35 数据行数: {len(RDS_new_df)}")
        #         st.write("lineItem/UnblendedRate 为 0.35 数据预览:")
        #         st.dataframe(RDS_new_df.head(1000))

                #--------------------新增资源--------------------------------
                insert_df=[]
                #------------------其他修改后的资源----------------------------------------------------
                Other_new_df = df[(df['product/region'] != 'ap-northeast-1') & (df['lineItem/LineItemType'] != 'SppDiscount')]
                EC2_condition = Other_new_df['lineItem/ProductCode'].isin(['AmazonEC2']) & Other_new_df['pricing/unit'].isin(['Hrs'])
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
                EC2_update_condition_672 = EC2_update_condition & (Other_new_df['lineItem/UsageAmount'] == 672)
                st.write(f"EC2_update_condition_672数据行数: {len(Other_new_df[EC2_update_condition_672])}")
                st.write("EC2_update_condition_672数据预览:")
                st.dataframe(Other_new_df[EC2_update_condition_672].head(1000))
                # Other_new_df筛选出RDS_update_condition 且lineItem/UsageAmount 为 672 的数据
                RDS_update_condition_672 = RDS_update_condition & (Other_new_df['lineItem/UsageAmount'] == 672)
                st.write(f"RDS_update_condition_672数据行数: {len(Other_new_df[RDS_update_condition_672])}")
                st.write("RDS_update_condition_672数据预览:")
                st.dataframe(Other_new_df[RDS_update_condition_672].head(1000))
                

                
                
                
                
                # Other_new_df去掉条件为EC2_update_condition 且lineItem/UnblendedRate 为 0.194 的数据
                Other_new_df = Other_new_df[~((EC2_update_condition & (Other_new_df['lineItem/UnblendedRate'] == 0.194)) | (RDS_update_condition & (Other_new_df['lineItem/UnblendedRate'] == 0.35)))]
                st.write(f"其他资源数据行数: {len(Other_new_df)}")
                st.write("其他资源数据预览:")
                st.dataframe(Other_new_df.head(1000))
               

                st.write(f"新增资源数据行数: {len(insert_df)}")
                st.dataframe(insert_df)
               
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
                file_name="processed_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.success("文件已准备好，请点击上方按钮下载")

                
                
        except Exception as e:
            st.error(f"处理文件时出错: {str(e)}")
            st.error("请确保文件格式正确且包含必要的列")
                
                
                
                
                
