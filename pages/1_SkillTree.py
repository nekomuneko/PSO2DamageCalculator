# pages/1_Skill_Tree.py の冒頭部分を修正

import streamlit as st
import json
import base64
import os  # 追加
from pathlib import Path # 追加

st.set_page_config(layout="wide")

# --- ファイルパスの基点を設定 ---
# 1. 現在のスクリプトの絶対パスを取得
SCRIPT_DIR = Path(__file__).parent.resolve()

# 2. imagesフォルダがあるプロジェクトルートパスを特定
#    pages/1_SkillTree.py から見て、親ディレクトリ (pages) の親ディレクトリ (ルート) を指定
PROJECT_ROOT = SCRIPT_DIR.parent.resolve() 

def get_image_path(class_name):
    # プロジェクトルートから images フォルダ内の画像ファイルまでの絶対パスを構築
    # ※あなたの最新のファイル構造 images/Hu.png を想定しています
    return str(PROJECT_ROOT / "images" / f"{class_name}.png")

# -------------------------------------------------------------------
# クラス名と画像ファイルパスの対応付け
# -------------------------------------------------------------------
CLASS_IMAGES = {
    "Hu": get_image_path("Hu"), 
    "Fi": get_image_path("Fi"),
    "Ra": get_image_path("Ra"),
    "Gu": get_image_path("Gu"),
    "Fo": get_image_path("Fo"),
    "Te": get_image_path("Te"),
    "Br": get_image_path("Br"),
    "Bo": get_image_path("Bo"),
    "Su": get_image_path("Su"),
    "Hr": get_image_path("Hr"),
    "Ph": get_image_path("Ph"),
    "Et": get_image_path("Et"),
    "Lu": get_image_path("Lu"),
}
# -------------------------------------------------------------------

# 全てのクラス定義
ALL_CLASSES = list(CLASS_IMAGES.keys())
# サブクラスとして選択可能なクラス (Hrは除外)
SUB_CLASSES_CANDIDATES = [c for c in ALL_CLASSES if c != "Hr"]

st.title("📚 1. Skill Tree 設定")

# セッションステートの初期化 (前回のコードから変更なし)
if 'main_class_select' not in st.session_state:
    st.session_state['main_class_select'] = "Hu"
if 'sub_class_select' not in st.session_state:
    st.session_state['sub_class_select'] = "None"
if 'skills_data' not in st.session_state:
    st.session_state['skills_data'] = {}


# タブの作成
tab1, tab2 = st.tabs(["myset", "skill tree"])

with tab1:
    st.subheader("クラス構成とデータ管理 (myset)")
    
    # -----------------------------------------------------
    # 1. クラス選択エリア (画像表示を追加)
    # -----------------------------------------------------
    
    col_main_img, col_main_select = st.columns([1, 4])
    
    with col_main_img:
        # メインクラスの画像表示
        selected_main_class = st.session_state['main_class_select']
        st.image(CLASS_IMAGES.get(selected_main_class, ""), width=64)
        
    with col_main_select:
        # メインクラスの選択 (全クラスから選択可能)
        main_class = st.selectbox(
            "メインクラス",
            options=ALL_CLASSES,
            key="main_class_select",
            label_visibility="collapsed" # ラベルを非表示にし、画像と並べる
        )
    
    # サブクラスのオプションを動的に決定 (ロジックは前回と同じ)
    
    # Hr, Ph, Et, Lu がメインクラスの場合
    if main_class in ["Hr", "Ph", "Et", "Lu"]:
        st.info(f"{main_class}は後継クラスのため、サブクラスを設定できません。")
        
        # サブクラスは"None"固定、選択不可
        col_sub_img, col_sub_select = st.columns([1, 4])
        with col_sub_img:
            st.image("https://dummyimage.com/64x64/aaaaaa/000000&text=None", width=64) # Noneアイコン
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
        # メインクラスが後継クラスではない場合
        sub_class_options_filtered = ["None"] + [c for c in SUB_CLASSES_CANDIDATES if c != main_class]

        col_sub_img, col_sub_select = st.columns([1, 4])
        
        with col_sub_img:
            # サブクラスの画像表示 (選択中の値に基づく)
            selected_sub_class = st.session_state.get('sub_class_select', 'None')
            if selected_sub_class == "None":
                 st.image("https://dummyimage.com/64x64/aaaaaa/000000&text=None", width=64)
            else:
                 st.image(CLASS_IMAGES.get(selected_sub_class, ""), width=64)

        with col_sub_select:
            st.selectbox(
                "サブクラス",
                options=sub_class_options_filtered,
                key="sub_class_select",
                label_visibility="collapsed"
            )

    st.markdown("---")

    # -----------------------------------------------------
    # 2. エクスポート/インポート機能エリア (mysetno)
    # -----------------------------------------------------
    
    st.subheader("mysetno (エクスポート/インポート)")

    # (エクスポート/インポートのロジックは前回と同じため省略せず、そのまま残します)
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
                
                st.success(f"設定をインポートしました: メイン={data['main_class']}, サブ={data['sub_class']}")
                st.rerun() 
            else:
                st.error("インポートされたJSONファイルが必要なキーを含んでいません。")
        except json.JSONDecodeError:
            st.error("ファイルが有効なJSON形式ではありません。")
        except Exception as e:
            st.error(f"ファイルの処理中にエラーが発生しました: {e}")

with tab2:
    st.subheader("スキルツリー詳細設定")
    st.write("スキル配分などの設定は、ここに追加されます。")