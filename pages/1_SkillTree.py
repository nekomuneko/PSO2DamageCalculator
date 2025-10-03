# pages/1_SkillTree.py

import streamlit as st
import json
# pathlibは現在使用されていないため削除しました
# from pathlib import Path 

st.set_page_config(layout="wide")

# --- セッションステートの初期化 ---
if 'main_class_select' not in st.session_state:
    st.session_state['main_class_select'] = "Hu"
if 'sub_class_select' not in st.session_state:
    st.session_state['sub_class_select'] = "None"
if 'skills_data' not in st.session_state:
    st.session_state['skills_data'] = {}
if 'gear_weapon_atk' not in st.session_state:
    st.session_state['gear_weapon_atk'] = 2000
if 'enemy_def' not in st.session_state:
    st.session_state['enemy_def'] = 1000
# --------------------------------------------------

# -------------------------------------------------------------------
# クラス定義 (画像関連のコードはすべて削除されました)
# -------------------------------------------------------------------
ALL_CLASSES = ["Bo", "Br", "Et", "Fi", "Fo", "Gu", "Hr", "Hu", "Lu", "Ph", "Ra", "Su", "Te"]
SUB_CLASSES_CANDIDATES = [c for c in ALL_CLASSES if c != "Hr"]
# -------------------------------------------------------------------

st.title("📚 1. Skill Tree 設定")

# --- タブの作成 ---
tab1, tab2 = st.tabs(["myset", "skill tree"])

with tab1:
    st.subheader("クラス構成とデータ管理 (myset)")
    
    # --- クラス選択エリア (画像表示なしのシンプルな形) ---
    
    main_class = st.selectbox(
        "メインクラス",
        options=ALL_CLASSES,
        key="main_class_select",
    )
    
    # --- サブクラスのオプションロジック ---
    
    if main_class in ["Hr", "Ph", "Et", "Lu"]:
        st.info(f"{main_class}は後継クラスのため、サブクラスを設定できません。")
        
        st.selectbox(
            "サブクラス",
            options=["None"],
            index=0,
            key="sub_class_select",
            disabled=True,
        )
        st.session_state['sub_class_select'] = "None" 
    else:
        sub_class_options_filtered = ["None"] + [c for c in SUB_CLASSES_CANDIDATES if c != main_class]

        st.selectbox(
            "サブクラス",
            options=sub_class_options_filtered,
            key="sub_class_select",
        )

    st.markdown("---")

    # --- エクスポート/インポート機能 (mysetno) ---
    st.subheader("mysetno (エクスポート/インポート)")

    export_data = {
        "main_class": st.session_state['main_class_select'],
        "sub_class": st.session_state['sub_class_select'],
        "skills": st.session_state['skills_data'], 
        "version": "pso2_dmg_calc_v1"
    }
    
    export_json = json.dumps(export_data, indent=4, ensure_ascii=False)
    
    st.download_button(
        label="⬇️ JSONファイルをエクスポート",
        data=export_json,
        file_name=f"pso2_set_{st.session_state['main_class_select']}_{st.session_state['sub_class_select']}.json",
        mime="application/json"
    )

    uploaded_file = st.file_uploader("⬆️ JSONファイルをインポート", type=["json"])

    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)
            if "main_class" in data and "sub_class" in data and "skills" in data:
                st.session_state['main_class_select'] = data["main_class"]
                st.session_state['sub_class_select'] = data["sub_class"]
                st.session_state['skills_data'] = data["skills"]
                st.success(f"設定をインポートしました。")
                st.rerun() 
            else:
                st.error("インポートされたJSONファイルが必要なキーを含んでいません。")
        except json.JSONDecodeError:
            st.error("ファイルが有効なJSON形式ではありません。")
        except Exception as e:
            st.error(f"ファイルの処理中にエラーが発生しました: {e}")

with tab2:
    st.subheader("スキルツリー詳細設定")
    st.write("スキル配分などの詳細設定をここに追加します。")
