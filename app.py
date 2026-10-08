import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
st.set_page_config(
    page_title="AI 简历岗位匹配助手",
    page_icon="📄",
    layout="centered"
)

st.title("📄 AI 简历岗位匹配助手")
st.caption("分析岗位要求，发现能力差距，明确求职改进方向")

st.subheader("01 · 输入信息")

resume = st.text_area(
    "个人简历",
    placeholder="请粘贴你的简历，包括教育背景、技能和项目经历……",
    height=220
)

job = st.text_area(
    "目标岗位",
    placeholder="请粘贴招聘岗位的职责、任职要求和学历要求……",
    height=220
)
prompt = f"""
请根据下面的岗位描述和简历，分析两者的匹配情况。

简历：
{resume}

岗位：
{job}

请严格按照以下 JSON 格式返回，不要输出 JSON 之外的其他文字：

{{
    "score": 70,
    "skills": ["Python", "Excel"],
    "noskills": ["Git"],
    "result": "简要说明匹配情况"
}}

字段要求：
- score：整数，表示匹配分数，范围为 0 到 100
- skills：列表，列出简历中已有且与岗位相关的技能
- noskills：列表，列出岗位要求但简历未体现的技能
- result：字符串，简要总结匹配情况

只能根据提供的信息分析，不要编造简历中不存在的经历。
"""
load_dotenv()
client=OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
def chat(prompt):
    response=client.responses.create ( 
        model="deepseek-flash",
     input=prompt)
    answer=response.output_text
    return answer

st.divider()

if st.button("开始分析", type="primary", use_container_width=True):
    if not resume.strip() or not job.strip():
        st.warning("请先填写简历和目标岗位。")
    else:
        # 把你原来的分析逻辑放在这里
        answer=chat(prompt)
        try:
            data=json.loads(answer)

        except json.JSONDecodeError:
            st.error("AI返回的数据格式不正确,请重试。")
        else:
            score=data["score"]
            skills=data["skills"]
            noskills=data["noskills"]
            result=data["result"]

            st.write("匹配分数",score)
            st.subheader("匹配技能")
            for skill in skills:
                st.markdown(f'- {skill}')
            st.subheader("缺失技能")
            for skill in noskills:
                st.markdown(f'- {skill}')
            
            st.write("分析总结",result)

