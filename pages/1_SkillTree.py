# pages/1_SkillTree.py

import streamlit as st
import json
# from pathlib import Path  # 現在使用されていないため削除

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
# クラス定義 (ご要望の並び順に修正しました)
# Hu, FI, Ra, Gu, Fo, Te, Br, Bo, Su, Hr, Ph, Et, Lu
# -------------------------------------------------------------------
ALL_CLASSES = ["Hu", "Fi", "Ra", "Gu", "Fo", "Te", "Br", "Bo", "Su", "Hr", "Ph", "Et", "Lu"]
SUB_CLASSES_CANDIDATES = [c for c in ALL_CLASSES if c != "Hr"] # サブクラス候補はHrを除く
# -------------------------------------------------------------------

st.title("📚 1. Skill Tree 設定")

# --- タブの作成 ---
tab1, tab2 = st.tabs(["myset", "skill tree"])

with tab1:
    st.subheader("クラス構成とデータ管理 (myset)")
    
    # --- クラス選択エリア ---
    
    # 選択肢はALL_CLASSESの新しい順序に従います
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
        # サブクラス候補はメインクラスを除いたもの + "None"
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
    
    # --- 動的スキルツリータブの生成 ---
    
    # 選択されているメインクラスとサブクラスを取得
    main_class_name = st.session_state.get('main_class_select', 'Hu')
    sub_class_name = st.session_state.get('sub_class_select', 'None')
    
    # タブのリストを Main / Sub の順で作成
    skill_tabs_list = [main_class_name]
    if sub_class_name != 'None':
        skill_tabs_list.append(sub_class_name)

    if skill_tabs_list:
        # st.tabs() を使用してタブオブジェクトを生成
        skill_tab_objects = st.tabs(skill_tabs_list)

        # 各タブの内容をループで生成
        for i, class_name in enumerate(skill_tabs_list):
            with skill_tab_objects[i]:
                st.header(f"{class_name} スキル設定")
                
                # ここに、スキル名とスライダーなどのUIが入ります
                st.write(f"現在、**{class_name}** のスキルツリー設定を表示しています。")
                st.info("スキル名、レベル入力（スライダーまたは数値入力）のUIをここに追加していきます。")
    else:
        # 本来ありえないが、念のため
        st.warning("クラスが選択されていません。mysetタブでクラスを選択してください。")
