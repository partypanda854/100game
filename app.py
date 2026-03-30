import streamlit as st
import random

# 設定網頁標題與手機優化佈局
st.set_page_config(page_title="半導體英單 100 題全挑戰", page_icon="🧪", layout="centered")

# --- 1. 完整 100 題資料庫 ---
if 'word_pool' not in st.session_state:
    st.session_state.word_pool = [
        {"en": "all", "zh": "全部"}, {"en": "animal", "zh": "動物"}, {"en": "answer", "zh": "答案、回答"},
        {"en": "ask", "zh": "問"}, {"en": "baby", "zh": "嬰兒"}, {"en": "basketball", "zh": "籃球"},
        {"en": "bite", "zh": "咬、啃"}, {"en": "boss", "zh": "老闆"}, {"en": "box", "zh": "盒子/箱子"},
        {"en": "breakfast", "zh": "早餐"}, {"en": "bus", "zh": "公車"}, {"en": "case", "zh": "案件"},
        {"en": "cell phone", "zh": "手機"}, {"en": "chair", "zh": "椅子"}, {"en": "chicken", "zh": "雞肉"},
        {"en": "city", "zh": "城市"}, {"en": "close", "zh": "關閉"}, {"en": "coat", "zh": "大衣"},
        {"en": "computer", "zh": "電腦"}, {"en": "cook", "zh": "煮、烹調、廚師"}, {"en": "count", "zh": "數(量)"},
        {"en": "danger", "zh": "危險"}, {"en": "date", "zh": "日期"}, {"en": "different", "zh": "不同的"},
        {"en": "down", "zh": "下/當(機)"}, {"en": "drink", "zh": "喝"}, {"en": "eat", "zh": "吃"},
        {"en": "elephant", "zh": "大象"}, {"en": "e-mail", "zh": "電子郵件"}, {"en": "enter", "zh": "輸入"},
        {"en": "excited", "zh": "刺激的、興奮的"}, {"en": "family", "zh": "家庭、家人"}, {"en": "fan", "zh": "電風扇"},
        {"en": "fast", "zh": "快的"}, {"en": "fruit", "zh": "水果"}, {"en": "go", "zh": "去"},
        {"en": "green", "zh": "綠色"}, {"en": "history", "zh": "歷史"}, {"en": "honest", "zh": "誠實的、正直的"},
        {"en": "jacket", "zh": "夾克"}, {"en": "kitchen", "zh": "廚房"}, {"en": "late", "zh": "遲到"},
        {"en": "left", "zh": "左邊"}, {"en": "library", "zh": "圖書館"}, {"en": "listen", "zh": "聽"},
        {"en": "lunch", "zh": "午餐"}, {"en": "machine", "zh": "機器"}, {"en": "motorcycle", "zh": "摩托車"},
        {"en": "music", "zh": "音樂"}, {"en": "name", "zh": "名字"}, {"en": "noodle", "zh": "麵條"},
        {"en": "north", "zh": "北方、北方的"}, {"en": "old", "zh": "老的、舊的"}, {"en": "only", "zh": "唯一"},
        {"en": "output", "zh": "輸/產出"}, {"en": "math", "zh": "數學"}, {"en": "sad", "zh": "悲傷的"},
        {"en": "sing", "zh": "唱"}, {"en": "six", "zh": "六"}, {"en": "smile", "zh": "微笑"},
        {"en": "snake", "zh": "蛇"}, {"en": "song", "zh": "歌曲"}, {"en": "sorry", "zh": "難過的、抱歉的"},
        {"en": "story", "zh": "故事"}, {"en": "street", "zh": "街道"}, {"en": "study", "zh": "讀"},
        {"en": "ten", "zh": "十"}, {"en": "time", "zh": "時間"}, {"en": "mouth", "zh": "嘴巴"},
        {"en": "white", "zh": "白色"}, {"en": "Alarm", "zh": "警告"}, {"en": "AMHS", "zh": "自動化物料傳輸系統"},
        {"en": "CMP", "zh": "化學機械研磨"}, {"en": "DF/Diffusion", "zh": "擴散"}, {"en": "Dummy", "zh": "檔片"},
        {"en": "EH/ Etch", "zh": "乾式蝕刻"}, {"en": "Equipment", "zh": "機台"}, {"en": "FAB", "zh": "無塵室"},
        {"en": "FOUP", "zh": "晶圓傳送盒"}, {"en": "Idle", "zh": "閒置"}, {"en": "Lend", "zh": "借機"},
        {"en": "Lot", "zh": "貨"}, {"en": "MO/ Miss Operation", "zh": "人為疏失"}, {"en": "Monitor", "zh": "控片"},
        {"en": "Particle", "zh": "微塵"}, {"en": "PH/ Photo", "zh": "黃光"}, {"en": "PM", "zh": "預防保養"},
        {"en": "Priority", "zh": "派工等級"}, {"en": "Recipe", "zh": "製程配方"}, {"en": "Run", "zh": "製程中"},
        {"en": "Status", "zh": "狀態"}, {"en": "Stocker", "zh": "晶圓保管庫"}, {"en": "TA", "zh": "助理技術員"},
        {"en": "TAC", "zh": "TA 認證系統"}, {"en": "TF/ Thin Film", "zh": "薄膜"}, {"en": "Wafer", "zh": "晶圓"},
        {"en": "Wait", "zh": "等待"}, {"en": "WET", "zh": "溼式蝕刻"}, {"en": "WIP", "zh": "在製品"},
        {"en": "Yield", "zh": "良率"}
    ]

# --- 2. 遊戲邏輯與狀態 ---
TOTAL_Q = 100 # 修改為 100 題全測驗
if 'score' not in st.session_state:
    st.session_state.update({
        'score': 0, 'q_idx': 0, 'game_over': False, 'wrong_list': [],
        'answered': False, 'last_feedback': None
    })

# 隨機打亂題目順序，確保每次挑戰順序不同
if 'question_order' not in st.session_state:
    indices = list(range(len(st.session_state.word_pool)))
    random.shuffle(indices)
    st.session_state.question_order = indices

def get_current_word():
    idx = st.session_state.question_order[st.session_state.q_idx]
    q = st.session_state.word_pool[idx]
    wrong_zh = [w['zh'] for w in st.session_state.word_pool if w['zh'] != q['zh']]
    options = random.sample(wrong_zh, 3) + [q['zh']]
    random.shuffle(options)
    return q, options

if 'curr_q' not in st.session_state:
    st.session_state.curr_q, st.session_state.opts = get_current_word()

# --- 3. 遊戲介面 ---
st.title("💡 半導體英單 100 題大挑戰")

if not st.session_state.game_over:
    st.write(f"### 目前進度：{st.session_state.q_idx + 1} / {TOTAL_Q}")
    st.progress((st.session_state.q_idx) / TOTAL_Q)
    st.markdown("---")
    
    st.write("#### 請選出正確的中文意思：")
    st.info(f"# **{st.session_state.curr_q['en']}**")

    for o in st.session_state.opts:
        if st.button(o, use_container_width=True, disabled=st.session_state.answered):
            st.session_state.answered = True
            if o == st.session_state.curr_q['zh']:
                st.session_state.score += 1
                st.session_state.last_feedback = ("success", "✅ 答對了！")
            else:
                st.session_state.last_feedback = ("error", f"❌ 答錯了！正確答案是：{st.session_state.curr_q['zh']}")
                st.session_state.wrong_list.append({
                    "word": st.session_state.curr_q['en'],
                    "correct": st.session_state.curr_q['zh'],
                    "yours": o
                })
            st.rerun()

    if st.session_state.answered:
        type, msg = st.session_state.last_feedback
        if type == "success": st.success(msg)
        else: st.error(msg)
        
        if st.button("下一題 ➡️", use_container_width=True):
            st.session_state.answered = False
            st.session_state.q_idx += 1
            if st.session_state.q_idx >= TOTAL_Q:
                st.session_state.game_over = True
            else:
                st.session_state.curr_q, st.session_state.opts = get_current_word()
            st.rerun()

else:
    # --- 4. 結算畫面 ---
    st.balloons()
    st.header("🎊 全數挑戰完成！")
    st.metric("答對題數", f"{st.session_state.score} / {TOTAL_Q}")
    
    if st.session_state.wrong_list:
        st.subheader("📝 錯題總複習")
        for item in st.session_state.wrong_list:
            with st.expander(f"❌ {item['word']}"):
                st.write(f"**正確答案：** :green[{item['correct']}]")
                st.write(f"**你的選擇：** :red[{item['yours']}]")
    else:
        st.success("超級厲害！100 題全對，你是單字王！🔥")

    if st.button("重新開始 100 題挑戰", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.markdown("---")
st.caption("自動化工程師專屬複習工具 - 亞東科技大學")