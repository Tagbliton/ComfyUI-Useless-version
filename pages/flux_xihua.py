import streamlit as st
import random
import os



from translator import translator_data
from api_demo.Flux import flux

st.title("Flux模型")
with st.sidebar:
    api_key = st.text_input("API_KEY", type='password')
    text = st.text_area("中英切换")



    if st.toggle("AI润色"):
        role = ("你是一个精通中英文的自然语言大师，可以将用户输入的文本进行英汉互译，并在保持原文句意不变的情况下，根据文生图提示词的规则对文本进行润色，只回答润色后的英文结果，不回答任何额外的解释。\n"
                '''示例1：
                原文：一个孤独的树在夜晚的月光下。
                翻译：A solitary tree stands under the soft glow of the moon on a tranquil night. The silvery moonlight bathes the landscape, casting long, gentle shadows and highlighting the tree's lone figure against the dark sky.
                示例2：
                原文：The quick brown fox jumps over the lazy dog.。
                翻译：A swift brown fox, elegantly leaping over a lazy dog, in an open field, under a clear blue sky.''')
    else:
        role = "你是一个中英文翻译专家，对用户输入的内容进行英汉互译。确保翻译结果符合中英文语言习惯，并考虑到某些词语的文化内涵和地区差异。只回答翻译结果，不回答任何额外的解释。"

    if st.button("翻译"):
        with st.spinner("正在思考中..."):
            translator = translator_data(api_key, 1.3, role, text)
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
directory = './models/loras'
models = search_files(directory)


with st.container(border=True):
    col1, col2 = st.columns([5,2], vertical_alignment='center')

    with col1:
        lora1 = st.selectbox("lora选择", models, index=None, key=1, placeholder="flux_realism_lora.safetensors(默认)")
        lora2 = st.selectbox("lora选择", models, index=None, key=3, placeholder="其他可选lora")

    with col2:
        strength1 = st.slider("权重", 0.00, 1.00, 1.00, 0.01, key=2)
        strength2 = st.slider("权重", 0.00, 1.00, 0.00, 0.01, key=4)




flux_prompt = st.text_area("提示词")



SeedModel = ["随机", "固定"]
seed = st.segmented_control("种子", SeedModel)

if seed is "随机":
    col1, col2 = st.columns([1,2])
    with col1:
        # 生成一个 0 到 100 之间的随机整数
        seed = random.randint(0, 2147483647)
    with col2:
        st.write(seed)
else:
    seed = st.text_input("", placeholder=seed)
col1, col2 = st.columns([2,1])
with col1:
    denoise = st.slider("降噪幅度", 0.00, 1.00, 0.50, 0.01)
with col2:
    steps = st.number_input("迭代步数", 1, 100, 20, 1)

image_uploader = st.file_uploader("图片上传")

if image_uploader is not None:
    # 获取上传的文件名
    image_name = image_uploader.name

    # 构造保存路径
    save_path = os.path.join('./input',image_name)

    # 将文件保存到指定文件夹
    with open(save_path, "wb") as f:
        f.write(image_uploader.getbuffer())

    # 显示上传的图片
    st.image(image_uploader, caption=image_name, use_container_width=True)






state = st.button("开始生成")
if  state is True:
    with st.spinner("正在生成中..."):

        flux(flux_prompt, lora1, strength1, lora2, strength2, image_name, seed, denoise, steps)
        st.success("success!")
    state = False


