import pandas as pd
import os
import streamlit as st
import openpyxl
from steamlitapp import adjust_column_width

def wdy_gcp():
    st.title("万得云GCP翻译")
    st.write("Create by Jackie Chen")
    # 定义输出文件名
    output_filename = "分析后文件.xlsx"
    
    st.info("当前客户名称表")
    # 加载客户名称文件

    # 客户名称表
    # 客户project-id	客户公司名称
    # translat202308	小黑鱼
    # atteam	玖邦数码
    # fengqi-439402	玖邦数码
    # gomo-439402	玖邦数码
    # qingbing	玖邦数码
    # xiahua-439402	玖邦数码
    # yinuo-439402	玖邦数码
    # yg-fish-wecloud-1	优聚大鱼
    # yg-fish-wecloud-2	优聚大鱼
    # yg-fish-wecloud-3	优聚大鱼
    # yg-fish-wecloud-4	优聚大鱼
    # translate-292306	优聚大鱼
    # graceful-fold-417204	优聚大鱼
    # woven-space-417204	优聚大鱼
    customerDf = pd.DataFrame({
        '客户project-id': ['translat202308', 'atteam', 'fengqi-439402', 'gomo-439402', 'qingbing', 'xiahua-439402', 'yinuo-439402', 'yg-fish-wecloud-1', 'yg-fish-wecloud-2', 'yg-fish-wecloud-3', 'yg-fish-wecloud-4', 'translate-292306', 'graceful-fold-417204', 'woven-space-417204'],
        '客户公司名称': ['小黑鱼', '玖邦数码', '玖邦数码', '玖邦数码', '玖邦数码', '玖邦数码', '玖邦数码', '优聚大鱼', '优聚大鱼', '优聚大鱼', '优聚大鱼', '优聚大鱼', '优聚大鱼', '优聚大鱼']
    })

    # customerDf = pd.read_excel("万得云/客户名称.xlsx")
    st.dataframe(customerDf) 
    # 上传EXCEL文件
    uploaded_file = st.file_uploader("上传万得云GCP报表", type="xlsx")

    if uploaded_file is not None:
        # 读取EXCEL文件
        df = pd.read_excel(uploaded_file)
        
        # 显示数据
        st.dataframe(df)

        # 按钮点击进行分析操作
        button_clicked = st.button("开始分析")

        if button_clicked:
            merged_df = pd.merge(df, 
                    customerDf,
                    left_on='Project ID',
                    right_on='客户project-id',
                    how='left')
            

            merged_df['new_cost'] = merged_df['Cost ($)'] / 0.3
            # 按客户公司名称筛选数据
            merged_df1 = merged_df[merged_df['客户公司名称'] =='小黑鱼']
            merged_df2 = merged_df[merged_df['客户公司名称'] =='优聚大鱼'] 
            merged_df3 = merged_df[merged_df['客户公司名称'] =='玖邦数码']
            # 每个表的Cost ($)字段除以0.3赋值到new_cost
            merged_df1['new_cost'] = merged_df1['Cost ($)'] / 0.3
            merged_df2['new_cost'] = merged_df2['Cost ($)'] / 0.3
            merged_df3['new_cost'] = merged_df3['Cost ($)'] / 0.3

                

            # 创建ExcelWriter对象
            with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
                # 将完整数据写入总表sheet
                merged_df.to_excel(writer, sheet_name='总表', index=False)
                # 将不同客户的数据写入不同的sheet
                merged_df1.to_excel(writer, sheet_name='小黑鱼', index=False)
                merged_df2.to_excel(writer, sheet_name='优聚大鱼', index=False)
                merged_df3.to_excel(writer, sheet_name='玖邦数码', index=False)

                # 调整每个sheet的列宽
                workbook = writer.book
                for sheet_name in workbook.sheetnames:
                    worksheet = workbook[sheet_name]
                    adjust_column_width(worksheet)
                    
            st.success(f"已生成多sheet文件: {output_filename}")
            print(f"已生成多sheet文件: {output_filename}")
            new_df = pd.read_excel(output_filename)
            st.dataframe(new_df)

            if os.path.exists(output_filename):
                with open(output_filename, "rb") as file:
                    st.download_button(
                        label="下载汇总文件",
                        data=file,
                        file_name=output_filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )