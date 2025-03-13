import streamlit as st
import pandas as pd
import numpy as np
from steamlitapp import adjust_column_width
import os


def All_bill_microsoft():
    st.title("总账单-微软云")
    uploaded_file = st.file_uploader("上传微软云原始账单", type=["csv", "xlsx","xls"])
    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1].lower()
        if file_type == 'csv':
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.dataframe(df)
        # 打印共有多少列，多少数据
        st.write(df.shape[0])

        # st.write(df.shape[1])


    #  将人民币账单改成美元账单（汇率）：4o以及4o之后的模型都是7.3314，其他一直都是6.8512
    # 将以下产品单价改成合同约定的单价
    # GPT-4o mini Training  0.0033
    # GPT-4o mini 部署 1.7
    # GPT-4o mini 输入令牌 0.000165    Inp-glbl Tokens
    # GPT-4o mini 输出令牌 0.00066     Outp-glbl Tokens

    # 将人民币账单改成美元账单（汇率）：
    # 列为"产品 (Product)"中含有4o以及4o之后的模型都是7.3314，其他一直都是6.8512
    # 创建条件判断
    # 筛选出"计量名称 (MeterName)"中含有4o以及4o之后的数据
    # df_4o = df[df['计量名称 (MeterName)'].str.contains('4o', na=False)]
     # 计量名称 (MeterName)含有"Outp-glbl Tokens"将"有效价格 (EffectivePrice)"改为0.00066
        # # 将有效价格列移到第一列
        # cols = df.columns.tolist()
        # cols.remove('有效价格 (EffectivePrice)')
        # cols = ['有效价格 (EffectivePrice)'] + cols
        # df = df[cols]

        # 将有效价格列移到最后一列
        cols = df.columns.tolist()
        cols.remove('有效价格 (EffectivePrice)')
        cols.remove('计量名称 (MeterName)')
        cols = cols + ['有效价格 (EffectivePrice)']
        cols = cols + ['计量名称 (MeterName)']
        df = df[cols]

        df['有效价格 (EffectivePrice)']= np.where(df['计量名称 (MeterName)'].str.contains('Inp', na=False), 0.000165, df['有效价格 (EffectivePrice)'])

        # df['token类型']=np.where(df['计量名称 (MeterName)'].str.contains('Inp', na=False), 'Inp-glbl Tokens', 'Outp-glbl Tokens')
        df['有效价格 (EffectivePrice)']= np.where(df['计量名称 (MeterName)'].str.contains('Outp', na=False), 0.00066, df['有效价格 (EffectivePrice)'])
        # 0.00066 df['有效价格 (EffectivePrice)']显示小数点后5位
        df['有效价格 (EffectivePrice)'] = df['有效价格 (EffectivePrice)'].apply(lambda x: "{:.5f}".format(x))

        st.write("处理Inp-glbl Tokens和Outp-glbl Tokens后的数据：")
        st.dataframe(df)
     # 计量名称 (MeterName)含有"Inp-glbl Tokens"将"有效价格 (EffectivePrice)"改为0.000165
        condition_4o = df['计量名称 (MeterName)'].str.contains('4o', na=False)

        # 根据条件应用不同汇率

        df['汇率'] = np.where(condition_4o, 7.3314, 6.8512)
    
    # 将人民币金额转换为美元
       
        df['美元金额'] = df['成本 (Cost)'] / df['汇率']
        st.write("处理4o以及4o之后的模型后的数据：")
        st.dataframe(df)
        # 根据"帐户名 (AccountName)"分组,拆成不同的sheet
        df_grouped = df.groupby('帐户名 (AccountName)')
        output_filename = "微软云计算后的账单.xlsx"
        with pd.ExcelWriter(output_filename,engine='openpyxl') as writer:
            for account_name, group in df_grouped:
                st.write(f"Sheet: {account_name}")
                #  将不同客户的数据写入不同的sheet
                group.to_excel(writer, sheet_name=account_name, index=False)
                st.dataframe(group)


        if os.path.exists(output_filename):
            with open(output_filename, "rb") as file:
                    st.download_button(
                        label="下载处理后的账单",
                        data=file,
                        file_name=output_filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    ) 

       
      
       