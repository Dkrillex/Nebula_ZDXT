import streamlit as st
import pandas as pd
import os
import numpy as np
from openpyxl.utils import get_column_letter
import importlib

def adjust_column_width(worksheet):
    for column in worksheet.columns:
        max_length = 0
        column_letter = get_column_letter(column[0].column)
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = max_length + 2
        worksheet.column_dimensions[column_letter].width = adjusted_width

def home():
    st.title("星云财务账单工具包")
    st.write("Create by Jackie Chen")
    st.write(f"Streamlit 版本: {st.__version__}")

#main函数
def main():
    # 启动命令：streamlit run Script001/steamlitapp.py --server.runOnSave=true
    # 动态导入模块
    wdy_gcp = importlib.import_module('wdy_gcp').wdy_gcp
    xunlei_cdn_aws = importlib.import_module('xunlei_cdn_aws').xunlei_cdn_aws
    All_bill_microsoft = importlib.import_module('All_bill_microsoft').All_bill_microsoft
    tuo_bang_aws = importlib.import_module('tuo_bang_aws').tuo_bang_aws
    xunlei_smartchain_aws = importlib.import_module('xunlei_smartchain_aws').xunlei_smartchain_aws
    zhenghao_aws = importlib.import_module('zhenghao_aws').zhenghao_aws

    st.sidebar.title('星云财务工具包')
    
    pages = {
        "主页": home,
        "万得云GCP翻译(完成)": wdy_gcp,
        "迅雷-CDN-AWS（完成）": xunlei_cdn_aws,
        "总账单-微软云(完成)": All_bill_microsoft,
        "拓邦-AWS（完成）": tuo_bang_aws,
        "迅雷-Smartchain-AWS（完成）": xunlei_smartchain_aws,
        "正浩-AWS(需求不明显)": zhenghao_aws
    }
    
    page = st.sidebar.selectbox("选择功能页面", list(pages.keys()))
    pages[page]()

if __name__ == "__main__":
    main()



