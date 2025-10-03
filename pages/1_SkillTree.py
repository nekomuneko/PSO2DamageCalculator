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
    
# 種族 (Race)
if 'race_select' not in st.session_state:
    st.session_state['race_select'] = "ヒューマン男"

# マグ (Mag Stats)
if 'mag_stats' not in st.session_state:
    st.session_state['mag_stats'] = {field: 0 for field in MAG_STATS_FIELDS}
# --------------------------------------------------

# -------------------------------------------------------------------
# クラス定義 (ご要望の並び順: Hu, FI, Ra, Gu, Fo, Te, Br, Bo, Su, Hr, Ph, Et, Lu)
# -------------------------------------------------------------------
ALL_CLASSES = ["Hu", "Fi", "Ra", "Gu", "Fo", "Te", "Br", "Bo", "Su", "Hr", "Ph", "Et", "Lu"]
SUB_CLASSES_CANDIDATES = [c for c in ALL_CLASSES if c != "Hr"]
# -------------------------------------------------------------------

st.title("📚 1. Skill Tree 設定")

# =================================================================
# 1. クラス構成 (クラス / サブクラス)
# =================================================================

st.subheader("クラス構成")
col_main_class, col_sub_class = st.columns(2)

with col_main_class:
    main_class = st.selectbox(
        "メインクラス",
        options=ALL_CLASSES,
        key="main_class_select",
    )

with col_sub_class:
    # --- サブクラスのオプションロジック ---
    if main_class in ["Hr", "Ph", "Et", "Lu"]:
        st.selectbox(
            "サブクラス",
            options=["None"],
            index=0,
            key="sub_class_select",
            disabled=True,
        )
        st.session_state['sub_class_select'] = "None" 
        st.info(f"{main_class}は後継クラスのため、サブクラスはNone固定です。", icon="ℹ️")
    else:
        sub_class_options_filtered = ["None"] + [c for c in SUB_CLASSES_CANDIDATES if c != main_class]

        st.selectbox(
            "サブクラス",
            options=sub_class_options_filtered,
            key="sub_class_select",
        )

st.markdown("---")

# =================================================================
# 2. 基本ステータス設定 (種族 / マグ)
# =================================================================

st.subheader("種族とマグの設定")
col_race, col_mag_title = st.columns(2)

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
    st.markdown("##### マグステータス (合計 200 まで)")

# --- マグの数値入力 (2列で配置) ---
# 合計値の計算とチェック
current_total_mag = sum(st.session_state['mag_stats'].values())
MAG_MAX_TOTAL = 200

mag_cols_1, mag_cols_2, mag_cols_3, mag_cols_4 = st.columns([1, 1, 1, 1])

# 入力欄の生成
for i, field in enumerate(MAG_STATS_FIELDS):
    # 2列に分けて配置するために、打撃力と打撃防御を1列目/2列目...に交互に配置
    if i % 2 == 0: # 打撃力, 法撃力, 打撃防御, ...
        col = mag_cols_1
    else: # 射撃力, 技量, 射撃防御, ...
        col = mag_cols_2
        
    # 技量と防御ステータスの配置を調整（少し複雑になるため、ここでは元の3列配置を2列に調整するシンプルな方法を一旦維持します）
    # シンプルな2列配置
    if i < 4: # 0, 1, 2, 3 (打撃力, 射撃力, 法撃力, 技量)
        col = mag_cols_1 if i % 2 == 0 else mag_cols_2
    else: # 4, 5, 6 (打撃防御, 射撃防御, 法撃防御)
         col = mag_cols_3 if i % 2 == 0 else mag_cols_4
    
    # 技量と防御は特殊なので、再配置します
    if field in ["打撃力", "射撃力", "法撃力"]:
        col = mag_cols_1
    elif field in ["打撃防御", "射撃防御", "法撃防御"]:
        col = mag_cols_2
    elif field == "技量":
        col = mag_cols_3

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

# 合計値の表示とチェック (マグ入力の下に集約)
st.markdown(f"**現在のマグ合計値:** **`{current_total_mag} / {MAG_MAX_TOTAL}`**")

if current_total_mag > MAG_MAX_TOTAL:
    st.error(f"マグの合計値が上限の {MAG_MAX_TOTAL} を超えています！ (現在: {current_total_mag})")
elif current_total_mag == MAG_MAX_TOTAL:
     st.success("マグの合計値が上限に達しました。", icon="✅")

st.markdown("---")

# =================================================================
# 3. 合計基礎ステータス表示 (新設: 計算結果プレースホルダー)
# =================================================================

st.subheader("合計基礎ステータス")

# 将来の計算のためのダミー値 (種族、クラス、装備補正などが反映される場所)
DUMMY_BASE_ATK = 1000 
DUMMY_BASE_DEF = 500
DUMMY_ACCURACY = 800

st.markdown("##### (このセクションは後で種族、クラス、装備の補正を反映します)")

col_atk, col_def = st.columns(2)

# 打撃力 / 打撃防御
with col_atk:
    st.metric(label="打撃力 (Mag + Base)", value=f"{DUMMY_BASE_ATK + st.session_state['mag_stats']['打撃力']}")
with col_def:
    st.metric(label="打撃防御 (Mag + Base)", value=f"{DUMMY_BASE_DEF + st.session_state['mag_stats']['打撃防御']}")

# 射撃力 / 射撃防御
col_atk, col_def = st.columns(2)
with col_atk:
    st.metric(label="射撃力 (Mag + Base)", value=f"{DUMMY_BASE_ATK + st.session_state['mag_stats']['射撃力']}")
with col_def:
    st.metric(label="射撃防御 (Mag + Base)", value=f"{DUMMY_BASE_DEF + st.session_state['mag_stats']['射撃防御']}")

# 法撃力 / 法撃防御
col_atk, col_def = st.columns(2)
with col_atk:
    st.metric(label="法撃力 (Mag + Base)", value=f"{DUMMY_BASE_ATK + st.session_state['mag_stats']['法撃力']}")
with col_def:
    st.metric(label="法撃防御 (Mag + Base)", value=f"{DUMMY_BASE_DEF + st.session_state['mag_stats']['法撃防御']}")

# 技量
st.metric(label="技量 (Mag + Base)", value=f"{DUMMY_ACCURACY + st.session_state['mag_stats']['技量']}")


st.markdown("---")

# =================================================================
# 4. エクスポート/インポート機能 (in / out)
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

col_export, col_import = st.columns(2)

with col_export:
    st.download_button(
        label="⬇️ JSONファイルをエクスポート",
        data=export_json,
        file_name=f"pso2_set_{st.session_state['main_class_select']}_{st.session_state['sub_class_select']}.json",
        mime="application/json",
        use_container_width=True
    )

with col_import:
    uploaded_file = st.file_uploader("⬆️ JSONファイルをインポート", type=["json"], key="import_uploader")

if uploaded_file is not None:
    try:
        data = json.load(uploaded_file)
        
        if "main_class" in data and "sub_class" in data and "skills" in data:
            st.session_state['main_class_select'] = data["main_class"]
            st.session_state['sub_class_select'] = data["sub_class"]
            st.session_state['skills_data'] = data["skills"]
            
            if "race" in data:
                st.session_state['race_select'] = data["race"]
            if "mag_stats" in data:
                st.session_state['mag_stats'] = data["mag_stats"]
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
# 5. スキルツリー詳細設定
# =================================================================

st.subheader("スキルツリー詳細設定")

main_class_name = st.session_state.get('main_class_select', 'Hu')
sub_class_name = st.session_state.get('sub_class_select', 'None')

# タブのリストを Main / Sub の順で作成
skill_tabs_list = [main_class_name]
if sub_class_name != 'None':
    skill_tabs_list.append(sub_class_name)

if skill_tabs_list:
    skill_tab_objects = st.tabs(skill_tabs_list)

    for i, class_name in enumerate(skill_tabs_list):
        with skill_tab_objects[i]:
            st.header(f"{class_name} スキル設定")
            
            st.write(f"現在、**{class_name}** のスキルツリー設定を表示しています。")
            st.info("ここにスキル名とレベル入力（スライダーまたは数値入力）のUIが入ります。")
else:
    st.warning("クラスが選択されていません。")
