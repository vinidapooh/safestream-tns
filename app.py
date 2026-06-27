import streamlit as st
import os
import pandas as pd
from googleapiclient.discovery import build
from dotenv import load_dotenv
from transformers import pipeline

# 1. Load environment variables and configure page layout
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

st.set_page_config(page_title="SafeStream Dashboard", page_icon="🛡️", layout="wide")

# GOOGLE MATERIAL DESIGN CUSTOM CSS OVERLAY
st.markdown("""
    <style>
        /* Base typography & clean backgrounds similar to Google Workspace */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #f8f9fa !important;
            font-family: "Roboto", "Segoe UI", sans-serif !important;
        }
        
        /* Sidebar styling to resemble Google Admin console panels */
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #e0e0e0 !important;
        }
        
        /* Headers styling matching Google product headers */
        h1 {
            color: #202124 !important;
            font-weight: 400 !important;
            font-size: 28px !important;
        }
        h3, h4 {
            color: #3c4043 !important;
            font-weight: 500 !important;
        }
        
        /* Transforming standard Streamlit buttons into Google Primary Action elements */
        div.stButton > button:first-child {
            background-color: #1a73e8 !important;
            color: white !important;
            border: 1px solid #1a73e8 !important;
            border-radius: 4px !important;
            padding: 8px 24px !important;
            font-weight: 500 !important;
            transition: background-color 0.2s, box-shadow 0.2s;
        }
        div.stButton > button:first-child:hover {
            background-color: #1557b0 !important;
            box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15) !important;
        }
        
        /* Material Style Card Containers for stats and report outputs */
        .google-card {
            background-color: #ffffff;
            padding: 24px;
            border: 1px solid #dadce0;
            border-radius: 8px;
            margin-bottom: 16px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ SafeStream Workspace")
st.caption("Google Trust & Safety Internal Operations Suite — Live Content Moderation Engine")

# Sidebar Infrastructure Status Panel
st.sidebar.markdown("### 🖥️ Infrastructure Status")
if API_KEY:
    st.sidebar.markdown("<span style='color: #137333; font-weight: 500;'>● YouTube API Connected</span>", unsafe_allow_html=True)
else:
    st.sidebar.markdown("<span style='color: #c5221f; font-weight: 500;'>● API Connection Offline</span>", unsafe_allow_html=True)

# Cache AI Model resource to maximize execution performance
@st.cache_resource
def load_classifier():
    return pipeline("text-classification", model="unitary/toxic-bert", top_k=None)

with st.spinner("Initializing system framework..."):
    classifier = load_classifier()
st.sidebar.markdown("<span style='color: #137333; font-weight: 500;'>● ToxicBERT Model Active</span>", unsafe_allow_html=True)

# ENTERPRISE COMPLIANCE: Localized Trust & Safety Keyword Blacklist
REGIONAL_BLACKLIST = ["gatiya", "pisslami", "poptat", "terrorist", "scam"]

# 2. Asset Ingestion User Interface
st.markdown("<div class='google-card'>", unsafe_allow_html=True)
st.markdown("### 📥 Queue Asset Ingestion")
search_mode = st.radio("Select Source Framework:", ("Keyword Search Inventory", "Direct Resource URL (Video/Live/Short)"), horizontal=True)

# Maintain operational state parameters across browser interaction steps
if "selected_video_id" not in st.session_state:
    st.session_state.selected_video_id = None
if "selected_video_title" not in st.session_state:
    st.session_state.selected_video_title = None

def get_youtube_client():
    return build("youtube", "v3", developerKey=API_KEY)

if search_mode == "Keyword Search Inventory":
    query = st.text_input("Look up catalog items:", placeholder="e.g., 'Kashmir News Debate'")
    
    if query and API_KEY:
        with st.spinner("Searching indexing servers..."):
            try:
                youtube = get_youtube_client()
                search_response = youtube.search().list(
                    q=query, part="id,snippet", maxResults=3, type="video"
                ).execute()
                
                results = search_response.get("items", [])
                
                if results:
                    st.markdown("#### 📺 Select Resource Node for Moderation Evaluation:")
                    cols = st.columns(3)
                    
                    for idx, item in enumerate(results):
                        v_id = item["id"]["videoId"]
                        v_title = item["snippet"]["title"]
                        v_channel = item["snippet"]["channelTitle"]
                        v_thumb = item["snippet"]["thumbnails"]["medium"]["url"]
                        
                        with cols[idx]:
                            st.image(v_thumb, use_container_width=True)
                            st.markdown(f"**{v_title}**")
                            st.caption(f"Channel: {v_channel}")
                            
                            if st.button(f"Analyze Target Node {idx+1}", key=f"btn_{v_id}"):
                                st.session_state.selected_video_id = v_id
                                st.session_state.selected_video_title = v_title
                else:
                    st.error("No matching asset keys located.")
            except Exception as e:
                st.error(f"Search Error: {e}")

    if st.session_state.selected_video_id:
        st.markdown(f"<div style='background-color: #e8f0fe; color: #1a73e8; padding: 12px; border-radius: 4px; margin-top: 8px;'>🎯 <b>Targeting Active Node:</b> {st.session_state.selected_video_title} <code>({st.session_state.selected_video_id})</code></div>", unsafe_allow_html=True)

else:
    video_url = st.text_input("Resource URL entry point:", placeholder="https://www.youtube.com/watch?v=...")
    
    def extract_video_id(url):
        if "/live/" in url: return url.split("/live/")[1].split("?")[0]
        if "/shorts/" in url: return url.split("/shorts/")[1].split("?")[0]
        if "v=" in url: return url.split("v=")[1].split("&")[0]
        if "youtu.be/" in url: return url.split("youtu.be/")[1].split("?")[0]
        return url
        
    if video_url:
        st.session_state.selected_video_id = extract_video_id(video_url)

st.markdown("</div>", unsafe_allow_html=True)

# 3. Pipeline Processing Step
if st.button("Run Risk Assessment"):
    if not API_KEY:
        st.error("❌ System configurations invalid: Missing API key.")
    elif not st.session_state.selected_video_id:
        st.error("❌ Action item target missing. Please ingest an active stream context.")
    else:
        with st.spinner("Analyzing parameters across asset layers..."):
            try:
                youtube = get_youtube_client()
                response = youtube.commentThreads().list(
                    part="snippet", videoId=st.session_state.selected_video_id, maxResults=20, textFormat="plainText"
                ).execute()
                
                comments = [item["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for item in response.get("items", [])]
                
                if not comments:
                    st.warning("No interactive text metadata present on target resource node.")
                else:
                    scored_comments_data = []
                    flagged_count = 0
                    escalate_video = False
                    
                    for comment in comments:
                        model_output = classifier(comment)[0]
                        scores = {prediction['label']: prediction['score'] for prediction in model_output}
                        
                        ai_flagged = any(score > 0.5 for score in scores.values())
                        lexicon_triggered = [word for word in REGIONAL_BLACKLIST if word in comment.lower()]
                        lexicon_flagged = len(lexicon_triggered) > 0
                        
                        is_flagged = ai_flagged or lexicon_flagged
                        if is_flagged:
                            flagged_count += 1
                            
                        if scores.get('threat', 0) > 0.6 or scores.get('identity_hate', 0) > 0.6 or lexicon_flagged:
                            escalate_video = True
                            
                        reason = []
                        if ai_flagged:
                            reason.extend([f"{k} ({v*100:.1f}%)" for k, v in scores.items() if v > 0.5])
                        if lexicon_flagged:
                            reason.append(f"Lexicon Match: {lexicon_triggered}")
                            
                        scored_comments_data.append({
                            "Status": "🚨 FLAGGED" if is_flagged else "✅ CLEAN",
                            "Comment Text": comment,
                            "Enforcement Action": "Route to Queue" if is_flagged else "None (Auto-Pass)",
                            "Policy Violation Details": ", ".join(reason) if reason else "Compliant",
                            "Toxicity Score": f"{scores.get('toxic', 0)*100:.1f}%"
                        })
                    
                    # 4. Render Operational Metrics
                    st.markdown("<div class='google-card'>", unsafe_allow_html=True)
                    st.subheader("📊 Policy Evaluation Report")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(label="Total Data Signals Screened", value=len(comments))
                    with col2:
                        violation_rate = (flagged_count / len(comments)) * 100
                        st.metric(label="Queue Enforcement Rate", value=f"{violation_rate:.1f}%")
                    with col3:
                        if escalate_video:
                            st.markdown("<div style='background-color: #fce8e6; border: 1px solid #fad2cf; padding: 16px; border-radius: 4px; color: #c5221f; font-weight: bold;'>🚨 CRISIS ESCALATION TRIGGERED</div>", unsafe_allow_html=True)
                        elif flagged_count > (len(comments) * 0.2):
                            st.markdown("<div style='background-color: #fef7e0; border: 1px solid #feefc3; padding: 16px; border-radius: 4px; color: #b06000; font-weight: bold;'>⚠️ ELEVATED COMPLIANCE RISK</div>", unsafe_allow_html=True)
                        else:
                            st.markdown("<div style='background-color: #e6f4ea; border: 1px solid #ceead6; padding: 16px; border-radius: 4px; color: #137333; font-weight: bold;'>✅ PLATFORM COMPLIANT</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # 5. Display Moderation Data Table Queue
                    st.markdown("<div class='google-card'>", unsafe_allow_html=True)
                    st.subheader("🛡️ Content Moderation Terminal Queue")
                    
                    df = pd.DataFrame(scored_comments_data)
                    
                    def color_status(val):
                        if val == "🚨 FLAGGED": return "background-color: #fce8e6; color: #c5221f; font-weight: bold;"
                        if val == "✅ CLEAN": return "background-color: #e6f4ea; color: #137333;"
                        return ""
                    
                    styled_df = df.style.applymap(color_status, subset=['Status'])
                    st.dataframe(styled_df, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"Operational Execution Fault: {e}")