import pandas as pd
import os
import streamlit as st

from steamlitapp import adjust_column_width

def wdy_gcp():
    # 定义输出文件名
    output_filename = "分析后文件.xlsx"
    
    st.info("当前客户名称表")
    # 加载客户名称文件
    customerDf = pd.read_excel("Script001\万得云\客户名称.xlsx")
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
        # check_button = st.button("查看生成后的文件")
        # if check_button and os.path.exists(output_filename):
        #     try:
        #         new_df = pd.read_excel(output_filename)
        #         st.dataframe(new_df)
        #         st.success("文件已检查")
        #     except Exception as e:
        #         st.error(f"无法读取文件: {str(e)}")
        # elif check_button:
        #     st.warning("请先点击'开始分析'生成文件")

        if os.path.exists(output_filename):
            with open(output_filename, "rb") as file:
                st.download_button(
                    label="下载汇总文件",
                    data=file,
                    file_name=output_filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )