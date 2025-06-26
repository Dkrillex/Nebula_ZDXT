import streamlit as st
import pandas as pd
import numpy as np
from steamlitapp import adjust_column_width
import os


def process_data_for_yunyan(df):
    """处理深圳市云燕信息技术有限公司的数据"""
    df = df.copy()
    # 先乘以1.06
    df['修改后的单价'] = df['单位价格 (UnitPrice)'] * 1.06
    df['修改后的单价'] = df['修改后的单价'].apply(lambda x: "{:.6f}".format(float(x)))
    # 根据是否包含4o使用不同汇率
    df['修改后的单价'] = np.where(df['计量名称 (MeterName)'].str.contains('4o', na=False)|df['计量名称 (MeterName)'].str.contains('mini', na=False)|df['计量名称 (MeterName)'].str.contains('4-turbo', na=False), 
                              df['修改后的单价'].astype(float) / 7.3314, 
                              df['修改后的单价'].astype(float) / 6.8512)
    # 显示小数点后六位
    # 计算修改后的成本
    df['修改后的成本'] = df['修改后的单价'].astype(float) * df['数量 (Quantity)']
    df['计费货币 (BillingCurrency)'] = 'USD'
    return df

def process_data_for_xuanna(df):
    """处理上海泫拿科技有限公司的数据"""
    df = df.copy()
    # 修改Inp-glbl Tokens的单价
    df['修改后的单价'] = np.where(df['计量名称 (MeterName)'].str.contains('Inp-glbl', na=False), 
                              0.00015, df['单位价格 (UnitPrice)'])
    
    # 修改Outp-glbl Tokens的单价
    df['修改后的单价'] = np.where(df['计量名称 (MeterName)'].str.contains('Outp-glbl', na=False), 
                              0.0006, df['修改后的单价'])
    
    # # 修改Batch Inp-glbl Tokens的单价
    # df['修改后的单价'] = np.where(df['计量名称 (MeterName)'].str.contains('Batch Inp-glbl', na=False),
    #                           0.000075, df['修改后的单价'])

    #  # 修改Batch Outp-glbl Tokens的单价
    # df['修改后的单价'] = np.where(df['计量名称 (MeterName)'].str.contains('Batch Outp-glbl', na=False),
    #                           0.0003, df['修改后的单价'])



    # 处理其他价格（根据是否包含4o使用不同汇率）
    df['修改后的单价'] = np.where(
        ~df['计量名称 (MeterName)'].str.contains('Inp-glbl', na=False) & 
        ~df['计量名称 (MeterName)'].str.contains('Outp-glbl', na=False),
        np.where(df['计量名称 (MeterName)'].str.contains('4o', na=False)|df['计量名称 (MeterName)'].str.contains('mini', na=False), 
                df['修改后的单价'].astype(float) / 7.3314, 
                df['修改后的单价'].astype(float) / 6.8512),
        df['修改后的单价'])
    
    # 显示小数点后六位
    df['修改后的单价'] = df['修改后的单价'].apply(lambda x: "{:.6f}".format(float(x)))
    # 计算修改后的成本
    df['修改后的成本'] = df['修改后的单价'].astype(float) * df['数量 (Quantity)']
    df['计费货币 (BillingCurrency)'] = 'USD'

    return df
def process_data_for_yixuan(df):
    """处理芜湖益炫网络科技有限公司的数据"""
    df = df.copy()
    df['含税单位价格'] = df['单位价格 (UnitPrice)']*1.06
    df['含税价格'] = df['含税单位价格']*df['数量 (Quantity)']
    df['计费货币 (BillingCurrency)'] = 'CNY'
    return df
def process_data_for_taipingyang(df):
    """处理广东太平洋互联网信息服务有限公司的数据"""
    df = df.copy()
    # 先乘以1.07
    # df['修改后的单价'] = df['单位价格 (UnitPrice)'] * 1.07
    # df['修改后的单价'] = df['修改后的单价'].apply(lambda x: "{:.6f}".format(float(x)))
    # 根据是否包含4o使用不同汇率
    # df['修改后的单价'] = np.where(df['计量名称 (MeterName)'].str.contains('4', na=False)|df['计量名称 (MeterName)'].str.contains('mini', na=False), 
    #                           df['修改后的单价'].astype(float) / 7.3314, 
    #                           df['修改后的单价'].astype(float) / 6.8512)
    # 显示小数点后六位
    # 计算修改后的成本
    # df['修改后的成本'] = df['修改后的单价'].astype(float) * df['数量 (Quantity)']
    df['计费货币 (BillingCurrency)'] = 'CNY'
    return df
def process_data_for_aimo(df):
    """处理埃默科技（海南）有限公司的数据"""
    df = df.copy()
    # 先乘以1.07
    # df['修改后的单价'] = df['单位价格 (UnitPrice)'] * 1.07
    # df['修改后的单价'] = df['修改后的单价'].apply(lambda x: "{:.6f}".format(float(x)))
    # # 根据是否包含4o使用不同汇率
    # df['修改后的单价'] = np.where(df['计量名称 (MeterName)'].str.contains('4', na=False)|df['计量名称 (MeterName)'].str.contains('mini', na=False), 
    #                           df['修改后的单价'].astype(float) / 7.3314, 
    #                           df['修改后的单价'].astype(float) / 6.8512)
    # 显示小数点后六位
    # 计算修改后的成本
    # df['修改后的成本'] = df['修改后的单价'].astype(float) * df['数量 (Quantity)']
    df['计费货币 (BillingCurrency)'] = 'CNY'
    return df
 
# def process_data_for_others(df):
#     """处理其他公司的数据"""
#     df = df.copy()
#     df['修改后的单价'] = df['单位价格 (UnitPrice)']
#     df['修改后的成本'] = df['成本 (Cost)']
#     return df

def All_bill_microsoft():
    st.title("总账单-微软云")
    uploaded_file = st.file_uploader("上传微软云原始账单", type=["csv", "xlsx", "xls"])
    
    if uploaded_file is not None:
        # 读取文件
        file_type = uploaded_file.name.split('.')[-1].lower()
        df = pd.read_csv(uploaded_file) if file_type == 'csv' else pd.read_excel(uploaded_file)
        
        # 显示原始数据
        st.write("原始数据：")
        st.dataframe(df)
        st.write(f"总行数：{df.shape[0]}")
        
        # 选择需要的列
        selected_columns = [
            '计费周期开始日期 (BillingPeriodStartDate)',
            '计费周期结束日期 (BillingPeriodEndDate)',
            '帐户所有者ID (AccountOwnerId)',
            '帐户名 (AccountName)',
            '日期 (Date)',
            '产品 (Product)',
            '计量名称 (MeterName)',
            '数量 (Quantity)',
            '单位价格 (UnitPrice)',
            '成本 (Cost)',
            '有效价格 (EffectivePrice)',
        ]
        df = df[selected_columns]
        
        # 处理每个客户的数据
        processed_dfs = {}
        df_grouped = df.groupby('帐户名 (AccountName)')
        
        for account_name, group in df_grouped:
            st.write(f"处理 {account_name} 的数据")
            if account_name == '深圳市云燕信息技术有限公司':
                processed_df = process_data_for_yunyan(group)
            elif account_name == '上海泫拿科技有限公司':
                processed_df = process_data_for_xuanna(group)
            elif account_name == '芜湖益炫网络科技有限公司':
                processed_df = process_data_for_yixuan(group)
            elif account_name == '广东太平洋互联网信息服务有限公司':
                processed_df = process_data_for_taipingyang(group)
            elif account_name == '埃默科技（海南）有限公司':
                processed_df = process_data_for_aimo(group)
            processed_dfs[account_name] = processed_df
            st.write(f"{account_name} 处理后的数据：")
            st.dataframe(processed_df)
        
        # 保存到Excel文件
        output_filename = "微软云计算后的账单.xlsx"
        with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
            # 保存原始数据
            for account_name, group in df_grouped:
                group.to_excel(writer, sheet_name=f"{account_name}_原始数据", index=False)
            
            # 保存处理后的数据
            for account_name, processed_df in processed_dfs.items():
                processed_df.to_excel(writer, sheet_name=f"{account_name}_处理后", index=False)

            
                
            # 创建汇总表
            summary_df = pd.concat(processed_dfs.values())
            summary_df.to_excel(writer, sheet_name="汇总数据", index=False)
        
        # 提供下载按钮
        if os.path.exists(output_filename):
            with open(output_filename, "rb") as file:
                st.download_button(
                    label="下载处理后的账单",
                    data=file,
                    file_name=output_filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

       
      
       