import streamlit as st
from openai import OpenAI
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

@st.cache_resource
def get_openai_client():
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except (KeyError, FileNotFoundError, AttributeError):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None
    return OpenAI(api_key=api_key)

MBTI_LIST = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

def generate_character_description(client, mbti_type):
    prompt = f"""
당신은 창의적인 마법사 캐릭터 디자이너입니다.
사용자의 MBTI 성격 유형이 "{mbti_type}"일 때, 해리포터나 신비한 동물사전 같은 세계관에 등장할 법한 마법 캐릭터를 상상하여 만들어주세요.

출력 형식 (한국어로 작성):

1. 캐릭터 이름: (마법사다운 독창적인 이름)
2. 역할/직업: (예: 어둠 방어술 교수, 마법 생물 조련사, 마법 약초학자 등)
3. 종족/혈통: (예: 인간, 하프엘프, 늑대인간, 정령 등)
4. 성격 및 능력: (2~3문장. 성격과 마법 능력, 특이점 포함)
5. 외형 묘사: (머리카락, 의상, 소품, 동물 친구 등 마법적 요소 포함)

문체는 마법 세계 백과사전이나 호그와트 연감처럼, 상상력 풍부하고 몰입감 있게 써주세요.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 마법 세계 캐릭터 생성 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"❌ 캐릭터 설명 생성 실패: {str(e)}")
        return None

def generate_image_url(client, mbti_type, description):
    try:
        image_prompt = f"""
A full-body portrait of a magical character inspired by Harry Potter and Fantastic Beasts, based on MBTI type {mbti_type}.
The character is described as: {description}.
Outfit includes wizard robes, cloak, wand, magical accessories.
Background setting: wizard school, magical forest, potion room, or ancient library.
Style: detailed concept art, cinematic lighting, fantasy atmosphere.
"""
        response = client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        return response.data[0].url
    except Exception as e:
        st.error(f"❌ 이미지 생성 실패: {str(e)}")
        return None

st.set_page_config(
    page_title="MBTI 마법 캐릭터 생성기",
    page_icon="🔮",
    layout="centered"
)

st.title("🔮 MBTI 마법 캐릭터 생성기")
st.markdown("당신의 MBTI를 바탕으로 마법 세계의 독특한 캐릭터를 만들어드립니다.")

client = get_openai_client()
if not client:
    st.error("⚠️ OpenAI API 키가 설정되지 않았습니다.")
    st.stop()

mbti = st.selectbox("당신의 MBTI 유형을 선택하세요:", MBTI_LIST)

if st.button("🧪 캐릭터 생성하기"):
    with st.spinner("🧙 마법 캐릭터를 생성 중입니다..."):
        description = generate_character_description(client, mbti)

    if description:
        st.success("🎉 캐릭터 생성 완료!")
        st.markdown("### 📝 마법 캐릭터 설명")
        st.markdown(description)

        with st.spinner("🎨 이미지 생성 중..."):
            image_url = generate_image_url(client, mbti, description)
        
        if image_url:
            st.markdown("### 🖼️ 생성된 캐릭터 이미지")
            st.image(image_url, use_container_width=True)
        else:
            st.warning("이미지 생성에 실패했습니다. 다시 시도해주세요.")
