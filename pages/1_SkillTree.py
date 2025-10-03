# pages/1_SkillTree.py

import streamlit as st
import json

st.set_page_config(layout="wide")

# --- マグのステータス定義 ---
MAG_STATS_FIELDS = ["打撃力", "射撃力", "法撃力", "技量", "打撃防御", "射撃防御", "法撃防御"]

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
    
# 新規追加: 種族 (Race)
if 'race_select' not in st.session_state:
    st.session_state['race_select'] = "ヒューマン男"

# 新規追加: マグ (Mag Stats)
if 'mag_stats' not in st.session_state:
    st.session_state['mag_stats'] = {field: 0 for field in MAG_STATS_FIELDS}
# --------------------------------------------------

# -------------------------------------------------------------------
# クラス定義 (Hu, FI, Ra, Gu, Fo, Te, Br, Bo, Su, Hr, Ph, Et, Lu)
# -------------------------------------------------------------------
ALL_CLASSES = ["Hu", "Fi", "Ra", "Gu", "Fo", "Te", "Br", "Bo", "Su", "Hr", "Ph", "Et", "Lu"]
SUB_CLASSES_CANDIDATES = [c for c in ALL_CLASSES if c != "Hr"]
# -------------------------------------------------------------------

st.title("📚 1. Skill Tree 設定")

# =================================================================
# 1. 種族・マグ設定エリア
# =================================================================

st.markdown("---")
st.subheader("基本ステータス設定")

col_race, col_mag_title = st.columns([1, 2])

with col_race:
    # --- 種族選択 ---
    RACE_OPTIONS = [
        "ヒューマン男", "ヒューマン女",
        "ニューマン男", "ニューマン女",
        "キャスト男", "キャスト女",
        "デューマン男", "デューマン女"
    ]
    st.selectbox(
        "種族",
        options=RACE_OPTIONS,
        key="race_select",
    )

with col_mag_title:
    # マグ入力は右側のスペース全体を使用
    st.markdown("##### マグステータス (合計 200 まで)")

# --- マグの数値入力 (3列で配置) ---
# 合計値の計算とチェックを容易にするため、入力はセッションステートに直接反映させる
mag_cols = st.columns(3)
current_total_mag = sum(st.session_state['mag_stats'].values())
MAG_MAX_TOTAL = 200

# 入力欄の生成
for i, field in enumerate(MAG_STATS_FIELDS):
    col = mag_cols[i % 3]
    with col:
        # 入力値は0から200に制限
        st.number_input(
            field,
            min_value=0,
            max_value=MAG_MAX_TOTAL, 
            key=f"mag_input_{field}",
            value=st.session_state['mag_stats'].get(field, 0),
            step=1,
            label_visibility="visible",
            # コールバック: 値が変更されたらセッションステートを更新し、合計をチェック
            on_change=lambda f=field: st.session_state['mag_stats'].__setitem__(f, st.session_state[f"mag_input_{f}"])
        )

# 合計値の表示とチェック
st.markdown(f"**現在のマグ合計値:** **`{current_total_mag} / {MAG_MAX_TOTAL}`**")

if current_total_mag > MAG_MAX_TOTAL:
    st.error(f"マグの合計値が上限の {MAG_MAX_TOTAL} を超えています！ (現在: {current_total_mag})")
elif current_total_mag == MAG_MAX_TOTAL:
     st.success("マグの合計値が上限に達しました。")


st.markdown("---")
# =================================================================
# 2. クラス選択エリア
# =================================================================

st.subheader("クラス構成")
    
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

# =================================================================
# 3. エクスポート/インポート機能 (in / out)
# =================================================================

st.subheader("mysetno (エクスポート/インポート)")

export_data = {
    # 既存のデータ
    "main_class": st.session_state['main_class_select'],
    "sub_class": st.session_state['sub_class_select'],
    "skills": st.session_state['skills_data'], 
    
    # 新規追加のデータ (拡張性に対応)
    "race": st.session_state['race_select'],
    "mag_stats": st.session_state['mag_stats'], 
    
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
        
        # インポート処理: 拡張されたデータもチェックし、セッションステートにロード
        if "main_class" in data and "sub_class" in data and "skills" in data:
            st.session_state['main_class_select'] = data["main_class"]
            st.session_state['sub_class_select'] = data["sub_class"]
            st.session_state['skills_data'] = data["skills"]
            
            # 新規データがあればロード
            if "race" in data:
                st.session_state['race_select'] = data["race"]
            if "mag_stats" in data:
                st.session_state['mag_stats'] = data["mag_stats"]
                # マグ入力コンポーネントの表示値を更新するために、個別のキーも更新
                for field, value in data["mag_stats"].items():
                    if f"mag_input_{field}" in st.session_state:
                         st.session_state[f"mag_input_{field}"] = value
                
            st.success(f"設定をインポートしました。")
            st.rerun() 
        else:
            st.error("インポートされたJSONファイルが必要なキーを含んでいません。")
    except json.JSONDecodeError:
        st.error("ファイルが有効なJSON形式ではありません。")
    except Exception as e:
        st.error(f"ファイルの処理中にエラーが発生しました: {e}")

st.markdown("---")

# =================================================================
# 4. スキルツリー詳細設定
# =================================================================

st.subheader("スキルツリー詳細設定")

# 選択されているメインクラスとサブクラスを取得
main_class_name = st.session_state.get('main_class_select', 'Hu')
sub_class_name = st.session_state.get('sub_class_select', 'None')

# タブのリストを Main / Sub の順で作成
skill_tabs_list = [main_class_name]
if sub_class_name != 'None':
    skill_tabs_list.append(sub_class_name)

if skill_tabs_list:
    # st.tabs() を使用してクラスごとのタブオブジェクトを生成
    skill_tab_objects = st.tabs(skill_tabs_list)

    # 各タブの内容をループで生成
    for i, class_name in enumerate(skill_tabs_list):
        with skill_tab_objects[i]:
            st.header(f"{class_name} スキル設定")
            
            # ここに、スキル名とスライダーなどのUIが入ります
            st.write(f"現在、**{class_name}** のスキルツリー設定を表示しています。")
            st.info("スキル名、レベル入力（スライダーまたは数値入力）のUIをここに追加していきます。")
else:
    st.warning("クラスが選択されていません。")
