import streamlit as st
import random
import os
from translator import translator_data
from api_demo.T2I import T2I


with st.sidebar:

    col1, col2 = st.columns([2,1], vertical_alignment='bottom')
    with col1:
        api_key = st.text_input("API_KEY", type='password')
    with col2:
        if st.button("储存为环境变量"):
            os.environ["<DeepSeek API Key>"] = api_key
    text = st.text_area("中英切换")
    if st.button("翻译"):
        with st.spinner("正在思考中..."):
            translator = translator_data(api_key, 1.3, text)
            st.code(translator, language=None, wrap_lines=True)





"""COMFYUI"""
def search_files(directory):
    file_list = []  # 初始化一个空列表
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.safetensors'):  # 只添加.txt文件
                full_path = os.path.join(root, file)
                file_list.append(os.path.basename(full_path))

    return file_list

# 指定要搜索的文件夹路径
directory = './models/checkpoints'
models = search_files(directory)


Checkpoint = st.selectbox(
    "模型选择",
    models,
)
Positive_prompt = st.text_area("正面提示词")
Negative_prompt = st.text_area("负面提示词")

col1, col2 = st.columns([1,1], vertical_alignment='bottom')
with col1:
    SeedModel = ["随机", "固定"]
    seed = st.segmented_control("种子", SeedModel)

    if seed is "随机":
        # 生成一个 0 到 100 之间的随机整数
        seed = random.randint(0, 2147483647)
        st.code(seed)
    else:
        seed = st.text_input("", placeholder='请输入种子')
with col2:
    st.text_input("宽", value='512')
    st.text_input("高", value='512')

state = st.button("开始生成")
if  state is True:
    with st.spinner("正在生成中..."):

        T2I(Checkpoint, Positive_prompt, Negative_prompt, seed)
        st.success("success!")
    state = False


