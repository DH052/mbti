import streamlit as st
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from langchain.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_embeddings_model(model_choice):
    """임베딩 모델 생성"""
    if "MiniLM" in model_choice:
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    else:
        model_name = "sentence-transformers/all-mpnet-base-v2"
    
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

MBTI_INFO = {
    "INTJ": {"emoji": "🏗️", "nickname": "건축가", "color": "#6B46C1"},
    "INTP": {"emoji": "🔬", "nickname": "논리술사", "color": "#7C3AED"},
    "ENTJ": {"emoji": "👑", "nickname": "통솔자", "color": "#DC2626"},
    "ENTP": {"emoji": "💡", "nickname": "변론가", "color": "#EA580C"},
    "INFJ": {"emoji": "🌙", "nickname": "옹호자", "color": "#059669"},
    "INFP": {"emoji": "📚", "nickname": "중재자", "color": "#0891B2"},
    "ENFJ": {"emoji": "🌟", "nickname": "선도자", "color": "#16A34A"},
    "ENFP": {"emoji": "🎠", "nickname": "활동가", "color": "#2563EB"},
    "ISTJ": {"emoji": "🛡️", "nickname": "현실주의자", "color": "#7C2D12"},
    "ISFJ": {"emoji": "🤗", "nickname": "수호자", "color": "#BE185D"},
    "ESTJ": {"emoji": "⚖️", "nickname": "경영자", "color": "#B91C1C"},
    "ESFJ": {"emoji": "💖", "nickname": "집정관", "color": "#DB2777"},
    "ISTP": {"emoji": "🔧", "nickname": "장인", "color": "#65A30D"},
    "ISFP": {"emoji": "🎨", "nickname": "모험가", "color": "#0D9488"},
    "ESTP": {"emoji": "🏃", "nickname": "사업가", "color": "#DC2626"},
    "ESFP": {"emoji": "🎉", "nickname": "연예인", "color": "#F59E0B"}
}

THEME_EMOJIS = {
    "감성": "💝",
    "유머": "😄", 
    "연애": "💕",
    "철학": "🤔"
}

def get_mbti_card(mbti_type):
    """MBTI 타입 카드 생성"""
    info = MBTI_INFO[mbti_type]
    return f"""
    <div style="
        background: linear-gradient(135deg, {info['color']}20, {info['color']}10);
        border: 2px solid {info['color']};
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <div style="font-size: 3rem; margin-bottom: 10px;">{info['emoji']}</div>
        <h3 style="color: {info['color']}; margin: 5px 0;">{mbti_type}</h3>
        <h4 style="color: {info['color']}; margin: 5px 0;">"{info['nickname']}"</h4>
        <p style="color: #666; font-style: italic;">{info['nickname']}</p>
    </div>
    """

def generate_mbti_message(mbti_type, theme):
    prompt = f"""
당신은 {mbti_type} 유형의 사람에게 오늘 하루를 위한 짧고 인사이트 있는 메시지를 주는 AI입니다.

테마는 "{theme}"입니다.

다음 형식으로 출력해주세요:
1. 오늘의 조언: (1줄)
2. 오늘의 대사: (1줄, 드라마/영화처럼)
3. 추천 행동: (1줄)

짧고 공감되며, 감성적으로 써주세요.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 공감 능력이 뛰어난 MBTI 전문가입니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8
    )

    return response.choices[0].message.content

st.set_page_config(
    page_title="MBTI 데일리 메시지", 
    page_icon="🌟",
    layout="wide"
)

st.markdown("""
<style>
    /* Gradient background for top and bottom */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 80px;
        background: linear-gradient(135deg, #0891B2, #16A34A, #2563EB);
        z-index: -1;
    }
    .stApp::after {
        content: '';
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 60px;
        background: linear-gradient(135deg, #2563EB, #16A34A, #0891B2);
        z-index: -1;
    }
    
    .stMarkdown {
        max-width: none;
    }
    .element-container {
        max-width: none;
    }
    .stCodeBlock {
        max-width: none;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    .main-header {
        text-align: center;
        color: #1e3a8a;
        font-size: 2rem;
        font-weight: bold;
        margin: 5px 0;
        padding-top: 20px;
    }
    .subtitle {
        text-align: center;
        font-size: 1rem;
        color: #666;
        margin: 5px 0 15px 0;
    }
    /* Remove default streamlit padding */
    .main .block-container {
        padding-top: 100px;
        padding-bottom: 80px;
    }
    /* Compact selectbox */
    .stSelectbox > div > div {
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🌟 MBTI 오늘의 메시지</h1>', unsafe_allow_html=True)
left_col, right_col = st.columns([1, 1])

with left_col:
    mbti_options = ["INTJ", "INTP", "ENTJ", "ENTP",
                    "INFJ", "INFP", "ENFJ", "ENFP", 
                    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
                    "ISTP", "ISFP", "ESTP", "ESFP"]
    
    mbti_type = st.selectbox("🧠 MBTI 선택:", mbti_options)
    
    theme_options = ["감성", "유머", "연애", "철학"]
    theme = st.selectbox("✨ 테마 선택:", theme_options, 
                        format_func=lambda x: f"{THEME_EMOJIS[x]} {x}")
    
    generate_button = st.button("🔮 메시지 생성", use_container_width=True)
    
    info = MBTI_INFO[mbti_type]
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {info['color']}20, {info['color']}10);
        border: 2px solid {info['color']};
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    ">
        <div style="font-size: 2rem; margin-bottom: 5px;">{info['emoji']}</div>
        <h4 style="color: {info['color']}; margin: 2px 0;">{mbti_type}</h4>
        <h5 style="color: {info['color']}; margin: 2px 0;">"{info['nickname']}"</h5>
    </div>
    """, unsafe_allow_html=True)

with right_col:
    if generate_button:
        with st.spinner("🤖 AI가 메시지를 작성하는 중..."):
            output = generate_mbti_message(mbti_type, theme)
            st.balloons()
            selected_info = MBTI_INFO[mbti_type]
            st.markdown(f"""
            <div style="text-align: center; margin: 10px 0;">
                <h3 style="color: {selected_info['color']}; margin: 5px 0;">
                    {selected_info['emoji']} {mbti_type} {selected_info['nickname']}님을 위한 {THEME_EMOJIS[theme]} {theme} 메시지
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {selected_info['color']}15, white);
                border: 2px solid {selected_info['color']};
                border-radius: 15px;
                padding: 20px;
                margin: 5px 0;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                font-size: 1.1rem;
                line-height: 1.6;
                height: 250px;
                overflow-y: auto;
                display: flex;
                align-items: center;
                text-align: left;
            ">
                <div style="width: 100%;">
                    {output.replace(chr(10), '<br>')}
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f0f0f0, #e0e0e0);
            border: 2px dashed #ccc;
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            margin: 20px 0;
            height: 400px;
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            <div>
                <div style="font-size: 3rem; margin-bottom: 20px;">🌟</div>
                <h3 style="color: #666; margin: 10px 0;">MBTI와 테마를 선택하고</h3>
                <h3 style="color: #666; margin: 10px 0;">메시지 생성 버튼을 눌러보세요!</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)