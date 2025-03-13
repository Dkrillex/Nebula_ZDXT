import streamlit as st
import pandas as pd

def zhenghao_aws():
    st.title("正浩-AWS(需求不明显)")
    st.write("Create by Jackie Chen")

    # 上传文件
    uploaded_file = st.file_uploader("上传正浩-AWS账单", type=["csv", "xlsx", "xls"])

