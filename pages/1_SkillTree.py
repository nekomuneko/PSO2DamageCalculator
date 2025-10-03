# pages/1_SkillTree.py

import streamlit as st
import json
import base64
import os
from pathlib import Path 

st.set_page_config(layout="wide")

# --- セッションステートの初期化 (KeyError対策) ---
if 'main_class_select' not in st.session_state:
    st.session_state['main_class_select'] = "Hu"
if 'sub_class_select' not in st.session_state:
    st.session_state['sub_class_select'] = "None"
if 'skills_data' not in st.session_state:
    st.session_state['skills_data'] = {}
# メインページで使用される他のセッションステートも初期化
if 'gear_weapon_atk' not in st.session_state:
    st.session_state['gear_weapon_atk'] = 2000
if 'enemy_def' not in st.session_state:
    st.session_state['enemy_def'] = 1000
# --------------------------------------------------

# --- ファイルパスの基点を設定 (Streamlit Cloud対応) ---
# スクリプトの親ディレクトリ（プロジェクトルート）を特定
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.resolve() 
# --------------------------------------------------------

# -------------------------------------------------------------------
# クラス名とファイル名のみの対応付け
# -------------------------------------------------------------------
CLASS_IMAGES = {
    # 値はファイル名のみ
    "Bo": "Bo.png", "Br": "Br.png", "Et": "Et.png",
    "Fi": "Fi.png", "Fo": "Fo.png", "Gu": "Gu.png",
    "Hr": "Hr.png", "Hu": "Hu.png", "Lu": "Lu.png",
    "Ph": "Ph.png", "Ra": "Ra.png", "Su": "Su.png",
    "Te": "Te.png"
}
NONE_IMAGE_FILENAME = "None.png" 
# -------------------------------------------------------------------

# --- 画像をバイトデータとして読み込むヘルパー関数 ---
@st.cache_data
def get_image_bytes(filename: str):
    """画像を絶対パスで読み込み、バイトデータを返す"""
    image_path = PROJECT_ROOT / "images" / filename
    
    if not image_path.exists():
        return None
    
    try:
        with open(image_path, "rb") as f:
            return f.read()
    except Exception:
        return None

# 全てのクラス定義
ALL_CLASSES = list(CLASS_IMAGES.keys())
SUB_CLASSES_CANDIDATES = [c for c in ALL_CLASSES if c != "Hr"]

st.title("📚 1. Skill Tree 設定")

# --- タブの作成 ---
tab1, tab2 = st.tabs(["myset", "skill tree"])

with tab1:
    st.subheader("クラス構成とデータ管理 (myset)")
    
    # --- クラス選択エリア ---
    
    col_main_img, col_main_select = st.columns([1, 4])
    
    with col_main_img:
        selected_main_class = st.session_state['main_class_select']
        image_filename = CLASS_IMAGES.get(selected_main_class)
        
        # バイトデータを取得
        image_to_display = get_image_bytes(image_filename)
            
        # 取得に失敗した場合、ダミー画像を使用
        if image_to_display is None:
            image_to_display = get_image_bytes(NONE_IMAGE_FILENAME)
            
        # 🚨 最終修正点: output_format="PNG" を追加 
        st.image(image_to_display, width=64, output_format="PNG")
        
    with col_main_select:
        main_class = st.selectbox(
            "メインクラス",
            options=ALL_CLASSES,
            key="main_class_select",
            label_visibility="collapsed"
        )
    
    # --- サブクラスのオプションロジック ---
    
    if main_class in ["Hr", "Ph", "Et", "Lu"]:
        st.info(f"{main_class}は後継クラスのため、サブクラスを設定できません。")
        
        col_sub_img, col_sub_select = st.columns([1, 4])
        with col_sub_img:
            # 🚨 最終修正点: output_format="PNG" を追加
            st.image(get_image_bytes(NONE_IMAGE_FILENAME), width=64, output_format="PNG")
        with col_sub_select:
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
        sub_class_options_filtered = ["None"] + [c for c in SUB_CLASSES_CANDIDATES if c != main_class]

        col_sub_img, col_sub_select = st.columns([1, 4])
        
        with col_sub_img:
            selected_sub_class = st.session_state.get('sub_class_select', 'None')
            
            if selected_sub_class == "None":
                 image_to_display = get_image_bytes(NONE_IMAGE_FILENAME)
            else:
                 image_filename = CLASS_IMAGES.get(selected_sub_class)
                 image_to_display = get_image_bytes(image_filename)
            
            # 取得に失敗した場合、ダミー画像を使用
            if image_to_display is None:
                image_to_display = get_image_bytes(NONE_IMAGE_FILENAME)
                
            # 🚨 最終修正点: output_format="PNG" を追加
            st.image(image_to_display, width=64, output_format="PNG")

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


