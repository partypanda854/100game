import streamlit as st
import random

# 設定網頁標題與手機優化佈局
st.set_page_config(page_title="半導體英單 100 題挑戰", page_icon="🧪", layout="centered")

# 完整的 100 個單字資料庫 (包含 PDF 基礎與專業術語)
if 'word_pool' not in st.session_state:
    st.session_state.word_pool = [
        {"en": "Equipment", "zh": "機台"}, {"en": "Yield", "zh": "良率"},
        {"en": "Recipe", "zh": "製程配方"}, {"en": "Wafer", "zh": "晶圓"},
        {"en": "FAB", "zh": "無塵室"}, {"en": "WIP", "zh": "在製品"},
        {"en": "Status", "zh": "狀態"}, {"en": "Priority", "zh": "派工等級"},
        {"en": "AMHS", "zh": "自動化物料傳輸系統"}, {"en": "Particle", "zh": "微塵/粒子"},
        {"en": "Monitor", "zh": "控片"}, {"en": "Dummy", "zh": "假片"},
        {"en": "Alarm", "zh": "警告"}, {"en": "Idle", "zh": "閒置/開路"},
        {"en": "PM", "zh": "預防保養"}, {"en": "MO", "zh": "人為疏失"},
        {"en": "Stocker", "zh": "物品保管庫"}, {"en": "Thin Film", "zh": "薄膜"},
        {"en": "Etch", "zh": "蝕刻"}, {"en": "Photo", "zh": "黃光/微影"},
        {"en": "Diffusion", "zh": "擴散"}, {"en": "Machine", "zh": "機器"},
        {"en": "Computer", "zh": "電腦"}, {"en": "Enter", "zh": "輸入"},
        {"en": "Wait", "zh": "等待"}, {"en": "Down", "zh": "故障/停機"},
        {"en": "Run", "zh": "製程中"}, {"en": "Math", "zh": "數學"},
        {"en": "History", "zh": "歷史"}, {"en": "Honest", "zh": "誠實的"},
        # ... 此處可依據 PDF 內容持續擴充至 100 題
    ]

# 初始化遊戲參數
TOTAL_Q = 10 # 每次挑戰 10 題
if 'score' not in st.session_state:
    st.session_state.update({'score': 0, 'q_idx': 0, 'game_over': False})

def next_question():
    q = random.choice(st.session_state.word_pool)
    wrong = random.sample([w['zh'] for w in st.session_state.word_pool if w['zh'] != q['zh']], 3)
    opts = wrong + [q['zh']]
    random.shuffle(opts)
    return q, opts

if 'current_q' not in st.session_state:
    st.session_state.current_q, st.session_state.options = next_question()

# --- 手機介面設計 ---
st.title("💡 半導體英單隨身測")

if not st.session_state.game_over:
    st.write(f"進度：{st.session_state.q_idx + 1} / {TOTAL_Q}")
    st.progress((st.session_state.q_idx) / TOTAL_Q)
    st.info(f"題目：## **{st.session_state.current_q['en']}**")

    for opt in st.session_state.options:
        if st.button(opt, use_container_width=True):
            if opt == st.session_state.current_q['zh']:
                st.session_state.score += 10
                st.toast("✅ 正確！")
            else:
                st.toast(f"❌ 答錯！答案是 {st.session_state.current_q['zh']}")
            
            st.session_state.q_idx += 1
            if st.session_state.q_idx >= TOTAL_Q:
                st.session_state.game_over = True
            else:
                st.session_state.current_q, st.session_state.options = next_question()
            st.rerun()
else:
    st.balloons()
    st.header("🏁 挑戰結束！")
    st.metric("你的得分", f"{st.session_state.score} 分")
    if st.button("重新開始", use_container_width=True):
        st.session_state.update({'score': 0, 'q_idx': 0, 'game_over': False})
        st.session_state.current_q, st.session_state.options = next_question()
        st.rerun()