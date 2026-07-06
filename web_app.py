# streamlit run web_app.py
import streamlit as st
from true_agent import IsaacWikiAgent  # 直接引入你写好的 Agent

# 设置网页标题和布局
st.set_page_config(page_title="以撒 Wiki 智能助手", page_icon="👼", layout="centered")

st.title("👼 以撒的结合 Wiki 智能助手")
st.caption("基于 DeepSeek 与 Tool-Calling 架构，直接检索中文 HuijiWiki。")

# 初始化或获取 session_state 中的 Agent 实例
if "agent" not in st.session_state:
    st.session_state.agent = IsaacWikiAgent()

# 初始化聊天历史记录
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "你好！我是以撒 Wiki 助手。想查什么道具、Boss 或机制？直接问我吧！"}
    ]

# 渲染历史聊天记录
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 接收用户输入
if prompt := st.chat_input("例如：打通里以撒解锁的那个换道具的叫什么？"):
    # 1. 把用户的问题显示在界面上
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. 调用你的 Agent 生成回答
    with st.chat_message("assistant"):
        with st.spinner("Agent 正在翻阅 Wiki 思考中，请稍候..."):
            try:
                # 调用 true_agent.py 中的 answer 方法
                result = st.session_state.agent.answer(prompt)
                response_text = result.answer
                
                # 如果你想在网页上展示它查了哪些网页，可以加上下面这段（可选）
                if result.pages:
                    sources = "\n\n**参考页面：**\n" + "\n".join([f"- [{p.title}]({p.url})" for p in result.pages])
                    response_text += sources

            except Exception as e:
                response_text = f"抱歉，查询时出现了错误：{e}"
        
        # 显示回答
        st.markdown(response_text)
    
    # 保存助手的回答到历史记录
    st.session_state.messages.append({"role": "assistant", "content": response_text})