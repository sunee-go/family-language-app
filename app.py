import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from deep_translator import GoogleTranslator
import re

st.set_page_config(page_title="Auto YouTube Subtitle Learning", layout="centered")

st.title("🎯 แอปเรียนภาษาจากลิงก์ YouTube (อัตโนมัติ)")
st.write("วางลิงก์วิดีโอ YouTube ที่ต้องการ ระบบจะดึงซับไตเติลและแปลให้อัตโนมัติครับ!")

youtube_url = st.text_input("🔗 วางลิงก์ YouTube ที่นี่:", placeholder="https://www.youtube.com/watch?v=...")

def extract_video_id(url):
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    return match.group(1) if match else None

if youtube_url:
    video_id = extract_video_id(youtube_url)
    
    if video_id:
        st.success(f"พบรหัสวิดีโอ: {video_id}")
        
        st.markdown(f"""
            <div style="display: flex; justify-content: center; margin-bottom: 20px;">
                <iframe width="100%" height="315" 
                    src="https://www.youtube.com/embed/{video_id}?enablejsapi=1" 
                    frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen>
                </iframe>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 ดึงซับไตเติลและแปลภาษาอัตโนมัติ"):
            with st.spinner("กำลังดึงข้อมูลซับไตเติลจาก YouTube..."):
                try:
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US'])
                    translator = GoogleTranslator(source='en', target='th')
                    processed_subtitles = []
                    
                    for item in transcript_list:
                        eng_text = item['text'].replace("\n", " ")
                        try:
                            thai_text = translator.translate(eng_text)
                        except:
                            thai_text = eng_text
                            
                        processed_subtitles.append({
                            "word": eng_text,
                            "translation": thai_text,
                            "start": item['start'],
                            "end": item['start'] + item['duration']
                        })
                    
                    st.session_state['subtitles'] = processed_subtitles
                    st.success(f"ดึงซับไตเติลสำเร็จ! ทั้งหมด {len(processed_subtitles)} รายการ")
                    
                except Exception as e:
                    st.error(f"ไม่สามารถดึงซับไตเติลของคลิปนี้ได้: {e}")
                    st.info("💡 ทริค: ลองเลือกคลิปที่มีซับไตเติลภาษาอังกฤษ (CC) เปิดอยู่บน YouTube ครับ")

        if 'subtitles' in st.session_state:
            st.markdown("### 📝 รายการซับไตเติลทั้งหมดในคลิป")
            for item in st.session_state['subtitles']:
                st.markdown(f"""
                    <div style='background-color: #f9f9f9; padding: 10px; margin-bottom: 8px; border-radius: 6px; border-left: 4px solid #28a745;'>
                        <span style='font-size: 14px; color: #666;'>🇹🇭 {item['translation']}</span><br>
                        <span style='font-size: 18px; font-weight: bold; color: #333;'>🇬🇧 {item['word']}</span>
                        <span style='float: right; font-size: 12px; color: #999;'>({item['start']:.1f}s)</span>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("กรุณากรอกลิงก์ YouTube ให้ถูกต้องครับ")
