承知いたしました。ご指示に従い、KeyError を防ぐためのセッションステート初期化ロジックを追加したうえで、現在の要件をすべて満たす pages/1_SkillTree.py の全コードを書き直して提示します。

このコードは、画像パスのエラーを避けるための相対パスと、st.image() のフォールバックに空文字列を使わない修正も含んでいます。

💻 pages/1_SkillTree.py スクリプト (最終修正版)
Python

# pages/1_SkillTree.py

import streamlit as st
import json
import base64

st.set_page_config(layout="wide")

# --- セッションステートの初期化 (KeyError対策) ---
if 'main_class_select' not in st.session_state:
    st.session_state['main_class_select'] = "Hu"
if 'sub_class_select' not in st.session_state:
    st.session_state['sub_class_select'] = "None"
if 'skills_data' not in st.session_state:
    st.session_state['skills_data'] = {}
# --------------------------------------------------

# -------------------------------------------------------------------
# クラス名と画像ファイルパスの対応付け (相対パスを使用)
# -------------------------------------------------------------------
CLASS_IMAGES = {
    # ファイル名と完全に一致させてください: images/Hu.png, images/Fi.png など
    "Bo": "images/Bo.png", "Br": "images/Br.png", "Et": "images/Et.png",
    "Fi": "images/Fi.png", "Fo": "images/Fo.png", "Gu": "images/Gu.png",
    "Hr": "images/Hr.png", "Hu": "images/Hu.png", "Lu": "images/Lu.png",
    "Ph": "images/Ph.png", "Ra": "images/Ra.png", "Su": "images/Su.png",
    "Te": "images/Te.png"
}
# Noneが選択された時、および画像が見つからない時のフォールバックパス
NONE_IMAGE_PATH = "images/None.png" 
# -------------------------------------------------------------------

# 全てのクラス定義
ALL_CLASSES = list(CLASS_IMAGES.keys())
# サブクラスとして選択可能なクラス (Hrはサブクラス設定不可のため除外)
SUB_CLASSES_CANDIDATES = [c for c in ALL_CLASSES if c != "Hr"]

st.title("📚 1. Skill Tree 設定")

# --- タブの作成 ---
tab1, tab2 = st.tabs(["myset", "skill tree"])

with tab1:
    st.subheader("クラス構成とデータ管理 (myset)")
    
    # --- クラス選択エリア ---
    
    col_main_img, col_main_select = st.columns([1, 4])
    
    with col_main_img:
        # メインクラスの画像表示 (フォールバックをNONE_IMAGE_PATHに設定)
        selected_main_class = st.session_state['main_class_select']
        image_to_display = CLASS_IMAGES.get(selected_main_class, NONE_IMAGE_PATH)
        st.image(image_to_display, width=64)
        
    with col_main_select:
        # メインクラスの選択
        main_class = st.selectbox(
            "メインクラス",
            options=ALL_CLASSES,
            key="main_class_select",
            label_visibility="collapsed"
        )
    
    # --- サブクラスのオプションロジック ---
    
    # Hr, Ph, Et, Lu がメインクラスの場合 (サブクラス不可)
    if main_class in ["Hr", "Ph", "Et", "Lu"]:
        st.info(f"{main_class}は後継クラスのため、サブクラスを設定できません。")
        
        col_sub_img, col_sub_select = st.columns([1, 4])
        with col_sub_img:
            st.image(NONE_IMAGE_PATH, width=64)
        with col_sub_select:
            # サブクラスは"None"固定、選択不可
            st.selectbox(
                "サブクラス",
                options=["None"],
                index=0,
                key="sub_class_select",
                disabled=True,
                label_visibility="collapsed"
            )
        st.session_state['sub_class_select'] = "None" 
    else:
        # メインクラスが後継クラスではない場合
        # サブクラスの候補は、Hrを除いた全クラスから、メインクラス自身を除外
        sub_class_options_filtered = ["None"] + [c for c in SUB_CLASSES_CANDIDATES if c != main_class]

        col_sub_img, col_sub_select = st.columns([1, 4])
        
        with col_sub_img:
            # サブクラスの画像表示 (フォールバックをNONE_IMAGE_PATHに設定)
            selected_sub_class = st.session_state.get('sub_class_select', 'None')
            if selected_sub_class == "None":
                 image_to_display = NONE_IMAGE_PATH
            else:
                 # ここでも、フォールバックを NONE_IMAGE_PATH に指定
                 image_to_display = CLASS_IMAGES.get(selected_sub_class, NONE_IMAGE_PATH)
            st.image(image_to_display, width=64)

        with col_sub_select:
            st.selectbox(
                "サブクラス",
                options=sub_class_options_filtered,
                key="sub_class_select",
                label_visibility="collapsed"
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

