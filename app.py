import streamlit as st
import random

st.set_page_config(page_title="半導體英單挑戰", page_icon="🧪", layout="centered")

# --- 1. 初始化資料庫 ---
if 'word_pool' not in st.session_state:
    st.session_state.word_pool = [
        {"en": "Equipment", "zh": "機台"}, {"en": "Yield", "zh": "良率"},
        {"en": "Recipe", "zh": "製程配方"}, {"en": "Wafer", "zh": "晶圓"},
        {"en": "FAB", "zh": "無塵室"}, {"en": "WIP", "zh": "在製品"},
        {"en": "Status", "zh": "狀態"}, {"en": "Priority", "zh": "派工等級"},
        {"en": "AMHS", "zh": "自動化物料傳輸系統"}, {"en": "Particle", "zh": "微塵/粒子"},
        {"en": "Alarm", "zh": "警告"}, {"en": "Idle", "zh": "閒置/開路"},
        {"en": "PM", "zh": "預防保養"}, {"en": "MO", "zh": "人為疏失"},
        {"en": "Stocker", "zh": "物品保管庫"}, {"en": "Thin Film", "zh": "薄膜"},
        {"en": "Etch", "zh": "蝕刻"}, {"en": "Photo", "zh": "黃光/微影"},
        {"en": "Diffusion", "zh": "擴散"}, {"en": "Down", "zh": "故障/停機"},
        {"en": "Wait", "zh": "等待"}, {"en": "Run", "zh": "製程中"},
        {"en": "Maintenance", "zh": "維修/保養"}, {"en": "Operator", "zh": "作業員"},
        {"en": "Automation", "zh": "自動化"}, {"en": "Cycle Time", "zh": "週期時間"},
        {"en": "Throughput", "zh": "生產量"}, {"en": "Defect", "zh": "缺陷"}
        # ... 此處可依據 PDF 內容持續擴充至 100 題
    ]

# --- 2. 初始化遊戲狀態 ---
TOTAL_Q = 10
if 'score' not in st.session_state:
    st.session_state.update({
        'score': 0, 'q_idx': 0, 'game_over': False, 'wrong_list': []
    })

def next_question():
    q = random.choice(st.session_state.word_pool)
    wrong_opts = random.sample([w['zh'] for w in st.session_state.word_pool if w['zh'] != q['zh']], 3)
    opts = wrong_opts + [q['zh']]
    random.shuffle(opts)
    return q, opts

if 'current_q' not in st.session_state:
    st.session_state.current_q, st.session_state.options = next_question()

# --- 3. 遊戲介面 ---
st.title("💡 半導體英單隨身測")

if not st.session_state.game_over:
    st.write(f"### 答題進度：{st.session_state.q_idx + 1} / {TOTAL_Q}")
    st.progress((st.session_state.q_idx) / TOTAL_Q)
    st.markdown("---")
    st.write("#### 請選出正確的中文意思：")
    st.info(f"# **{st.session_state.current_q['en']}**")

    for opt in st.session_state.options:
        if st.button(opt, use_container_width=True):
            # 判斷對錯
            if opt == st.session_state.current_q['zh']:
                st.session_state.score += 10
                st.toast("✅ 答對囉！", icon="🎉")
            else:
                # 紀錄錯題內容
                st.session_state.wrong_list.append({
                    "word": st.session_state.current_q['en'],
                    "correct": st.session_state.current_q['zh'],
                    "your_answer": opt
                })
                st.toast(f"❌ 答錯了！答案是：{st.session_state.current_q['zh']}", icon="⚠️")
            
            # 進入下一題
            st.session_state.q_idx += 1
            if st.session_state.q_idx >= TOTAL_Q:
                st.session_state.game_over = True
            else:
                st.session_state.current_q, st.session_state.options = next_question()
            st.rerun()

else:
    # --- 4. 結算畫面與錯題顯示 ---
    st.balloons()
    st.header("🎊 挑戰完成！")
    st.metric("最終總分", f"{st.session_state.score} 分")
    
    # 顯示錯題本
    if st.session_state.wrong_list:
        st.subheader("📝 錯題檢討區")
        st.write("複習一下這些容易搞混的單字：")
        for item in st.session_state.wrong_list:
            with st.expander(f"❌ 單字：{item['word']}"):
                st.write(f"**正確答案：** :green[{item['correct']}]")
                st.write(f"**你的選擇：** :red[{item['your_answer']}]")
    else:
        st.success("完美！你全部都答對了，太厲害了！🔥")

    if st.button("重新開始挑戰", use_container_width=True):
        st.session_state.update({'score': 0, 'q_idx': 0, 'game_over': False, 'wrong_list': []})
        st.session_state.current_q, st.session_state.options = next_question()
        st.rerun()

st.markdown("---")
st.caption("自動化工程師專屬複習工具")