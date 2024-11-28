import streamlit as st
import pandas as pd

from News_generation import *
from SongCi_generation import *




def intro():

    st.write("# 欢迎来到**文本生成**! 👋")
    st.sidebar.success("请在上方选择一个演示")

    st.markdown(
        """
        文本生成是一种自然语言处理技术，旨在通过计算机算法自动生成符合语法规则和语义逻辑的文本内容。
        这种技术可以应用于多个领域，包括但不限于内容创作、自动问答、机器翻译、对话系统、摘要生成等。

        **👈 请从左侧的下拉框中选择您想查看的演示页面**

        ### 🧊 宋词生成

        - 选择词牌名：
        - 算法选择：带权重的2—gram模型 or 不带权重的2-gram模型 

        ### 🧊 新闻生成

        - 新闻最大长度
        - 新闻最小长度
        - 算法选择：带权重的2—gram模型 or 不带权重的2-gram模型 

        ### 🧊 词牌名库

         - 词牌名：如：`如梦令`
         - 词牌格式： 如：`6656226`
    """
    )

def songci_generation_demo():

    songci_title_format = load_Ci_title_format()
    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')

    st.markdown('--------------------')

    st.sidebar.markdown('--------------------')

    title = st.sidebar.selectbox('选择词牌名', list(songci_title_format.keys()))
    st.write(f'词牌名：{title}')
    st.write(f'词牌名格式：{songci_title_format[title]}')

    st.sidebar.markdown('--------------------')

    use_weights = st.sidebar.checkbox('是否使用权重')
    if use_weights:
        st.write('算法选择：使用权重的2-gram模型')
    else:
        st.write('算法选择：不使用权重:的2-gram模型')

    st.sidebar.markdown('--------------------')

    if st.sidebar.button('生成宋词'):
        st.write(f'生成内容：{generate_SongCi(title, use_weights)}')

    st.markdown('--------------------')


def news_generation_demo():

    st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")

    st.markdown('--------------------')

    st.sidebar.markdown('--------------------')
    
    min = st.sidebar.number_input('请输入文章最小长度', step=1)
    st.write(f'文章最小长度：{min}')

    st.sidebar.markdown('--------------------')

    max = st.sidebar.number_input('请输入文章最大长度', step=1)
    st.write(f'文章最大长度：{max}')

    st.sidebar.markdown('--------------------')

    use_weights = st.sidebar.checkbox('是否使用权重')
    if use_weights:
        st.write('算法选择：使用权重的2-gram模型')
    else:
        st.write('算法选择：不使用权重:的2-gram模型')

    st.sidebar.markdown('--------------------')

    if st.sidebar.button('生成新闻'):
        content = generate_news([min, max], use_weights=use_weights)
        st.write(f'生成内容：{content}')
        st.write(f'文章长度：{len(content)}')

    st.markdown('--------------------')

def show_ci_titles_demo():
    
    st.markdown(f'# {list(page_names_to_funcs.keys())[3]}')
    title_format = load_Ci_title_format()
    title = list(title_format.keys())[:100]
    format = list(title_format.values())[:100]
    title_format = [{'词牌名': t, '词牌格式': f} for t, f in zip(title, format)]
    title_format.append({'词牌名': '……', '词牌格式': '……'})
    df = pd.DataFrame(title_format)
    st.dataframe(df)


if __name__ == "__main__":

    page_names_to_funcs = {
    "首页": intro, 
    "宋词生成": songci_generation_demo,
    "新闻生成": news_generation_demo,
    "词牌名库": show_ci_titles_demo
    }

    demo_name = st.sidebar.selectbox("选择演示页面", page_names_to_funcs.keys())
    page_names_to_funcs[demo_name]()
# streamlit run ./e2/text_generation_2_gram/streamlit_app.py