import streamlit as st
import json
import math

st.set_page_config(layout="wide")

# =================================================================
# 1. 補正データ定義 (確定版基礎値と補正率)
# =================================================================

# --- プレイヤー基礎ステータス (LV100固定値として設定) ---
NEW_BASE_STATS = {
    "HP": 650,
    "PP": 120,
    "打撃力": 540,
    "射撃力": 540,
    "法撃力": 540,
    "技量": 415,
    "打撃防御": 450,
    "射撃防御": 450,
    "法撃防御": 450
}

# --- 種族補正データ (乗算補正: 1.05 = +5%, 0.95 = -5%) ---
RACE_CORRECTIONS = {
    "ヒューマン男": {"HP": 1.05, "PP": 1.00, "打撃力": 1.04, "射撃力": 1.03, "法撃力": 1.00, "技量": 1.05, "打撃防御": 1.05, "射撃防御": 1.00, "法撃防御": 1.00},
    "ヒューマン女": {"HP": 1.04, "PP": 1.00, "打撃力": 1.00, "射撃力": 1.03, "法撃力": 1.04, "技量": 1.06, "打撃防御": 1.00, "射撃防御": 1.00, "法撃防御": 1.05},
    "ニューマン男": {"HP": 0.95, "PP": 1.00, "打撃力": 1.00, "射撃力": 1.02, "法撃力": 1.08, "技量": 1.04, "打撃防御": 1.00, "射撃防御": 1.05, "法撃防御": 1.00},
    "ニューマン女": {"HP": 0.94, "PP": 1.00, "打撃力": 1.00, "射撃力": 1.02, "法撃力": 1.10, "技量": 1.04, "打撃防御": 1.00, "射撃防御": 1.00, "法撃防御": 1.05},
    "キャスト男":   {"HP": 1.07, "PP": 1.00, "打撃力": 1.05, "射撃力": 1.04, "法撃力": 0.96, "技量": 1.07, "打撃防御": 1.05, "射撃防御": 1.00, "法撃防御": 0.95},
    "キャスト女":   {"HP": 1.06, "PP": 1.00, "打撃力": 1.04, "射撃力": 1.05, "法撃力": 0.96, "技量": 1.07, "打撃防御": 1.00, "射撃防御": 1.05, "法撃防御": 0.95},
    "デューマン男": {"HP": 0.96, "PP": 1.00, "打撃力": 1.07, "射撃力": 1.04, "法撃力": 1.05, "技量": 1.05, "打撃防御": 1.00, "射撃防御": 1.00, "法撃防御": 1.00},
    "デューマン女": {"HP": 0.95, "PP": 1.00, "打撃力": 1.06, "射撃力": 1.05, "法撃力": 1.05, "技量": 1.06, "打撃防御": 1.00, "射撃防御": 1.00, "法撃防御": 1.00},
}

# --- クラス補正データ (乗算補正) ---
CLASS_CORRECTIONS = {
    # 旧クラス
    "Hu": {"HP": 1.18, "PP": 1.00, "打撃力": 1.07, "射撃力": 1.00, "法撃力": 0.83, "技量": 1.00, "打撃防御": 1.29, "射撃防御": 1.00, "法撃防御": 1.00}, 
    "Fi": {"HP": 1.01, "PP": 1.00, "打撃力": 1.07, "射撃力": 0.83, "法撃力": 1.00, "技量": 1.00, "打撃防御": 1.29, "射撃防御": 1.00, "法撃防御": 1.00}, 
    "Ra": {"HP": 0.99, "PP": 1.00, "打撃力": 1.00, "射撃力": 1.07, "法撃力": 0.83, "技量": 1.00, "打撃防御": 1.00, "射撃防御": 1.29, "法撃防御": 1.00}, 
    "Gu": {"HP": 1.00, "PP": 1.00, "打撃力": 1.00, "射撃力": 1.07, "法撃力": 0.83, "技量": 1.00, "打撃防御": 1.00, "射撃防御": 1.29, "法撃防御": 1.00}, 
    "Fo": {"HP": 0.82, "PP": 1.00, "打撃力": 0.83, "射撃力": 1.00, "法撃力": 1.07, "技量": 1.00, "打撃防御": 1.00, "射撃防御": 1.00, "法撃防御": 1.29}, 
    "Te": {"HP": 0.82, "PP": 1.00, "打撃力": 1.00, "射撃力": 0.83, "法撃力": 1.07, "技量": 1.00, "打撃防御": 1.29, "射撃防御": 1.00, "法撃防御": 1.00}, 
    "Br": {"HP": 1.01, "PP": 1.00, "打撃力": 1.01, "射撃力": 1.01, "法撃力": 0.90, "技量": 1.01, "打撃防御": 1.08, "射撃防御": 1.08, "法撃防御": 1.08}, 
    "Bo": {"HP": 1.01, "PP": 1.00, "打撃力": 1.01, "射撃力": 0.90, "法撃力": 1.01, "技量": 1.01, "打撃防御": 1.08, "射撃防御": 1.08, "法撃防御": 1.08}, 
    "Su": {"HP": 0.99, "PP": 1.00, "打撃力": 1.01, "射撃力": 1.01, "法撃力": 1.01, "技量": 1.01, "打撃防御": 1.08, "射撃防御": 1.08, "法撃防御": 1.08}, 
    # 後継クラス
    "Hr": {"HP": 1.24, "PP": 1.00, "打撃力": 1.29, "射撃力": 1.29, "法撃力": 1.29, "技量": 1.32, "打撃防御": 1.55, "射撃防御": 1.55, "法撃防御": 1.55}, 
    "Ph": {"HP": 1.20, "PP": 1.00, "打撃力": 1.32, "射撃力": 1.32, "法撃力": 1.32, "技量": 1.36, "打撃防御": 1.46, "射撃防御": 1.46, "法撃防御": 1.46}, 
    "Et": {"HP": 1.26, "PP": 1.00, "打撃力": 1.25, "射撃力": 1.25, "法撃力": 1.25, "技量": 1.31, "打撃防御": 1.62, "射撃防御": 1.62, "法撃防御": 1.62}, 
    "Lu": {"HP": 1.22, "PP": 1.00, "打撃力": 1.27, "射撃力": 1.27, "法撃力": 1.27, "技量": 1.39, "打撃防御": 1.58, "射撃防御": 1.58, "法撃防御": 1.58}, 
}

# --- クラスブーストの固定値 (全クラスLv75達成時のボーナス) ---
CLASS_BOOST_BONUS = {
    "HP": 60, "PP": 10, "打撃力": 120, "射撃力": 120, "法撃力": 120, "技量": 60, "打撃防御": 90, "射撃防御": 90, "法撃防御": 90
}
# -------------------------------------------------------------------

# マグのステータス定義
MAG_STATS_FIELDS = ["打撃力", "射撃力", "法撃力", "技量", "打撃防御", "射撃防御", "法撃防御"]
ALL_CLASSES = ["Hu", "Fi", "Ra", "Gu", "Fo", "Te", "Br", "Bo", "Su", "Hr", "Ph", "Et", "Lu"]

# 【重要】サブクラスとして選択できないクラス (Hrのみ)
UNAVAILABLE_SUBCLASSES = ["Hr"]
# 【重要】メインクラスに設定した場合、サブクラスが強制的にNoneになるクラス
SUCCESSOR_MAIN_CLASSES = ["Hr", "Ph", "Et", "Lu"]

# --- セッションステートの初期化 ---
if 'main_class_select' not in st.session_state: st.session_state['main_class_select'] = "Hu" 
if 'sub_class_select' not in st.session_state: st.session_state['sub_class_select'] = "None"
if 'skills_data' not in st.session_state: st.session_state['skills_data'] = {}
if 'race_select' not in st.session_state: st.session_state['race_select'] = "ヒューマン男"
if 'mag_stats' not in st.session_state: 
    st.session_state['mag_stats'] = {field: 0 for field in MAG_STATS_FIELDS}
if 'class_boost_enabled' not in st.session_state: st.session_state['class_boost_enabled'] = True 

# =================================================================
# 2. 計算関数 (確定ロジック: 全ステップ切り捨て適用)
# =================================================================

def get_calculated_stats():
    """
    LV100基礎ステータスを起点に、種族、クラス、マグ、クラスブーストを合算した基本ステータスを計算します。
    【確定ロジック】すべての乗算補正ステップで「切り捨て (INT / FLOOR)」を適用します。
    
    ロジックの順序:
    1. メインクラス最終値 = Floor(Floor(基礎値 * メインクラス補正) * 種族補正)
    2. サブクラス貢献度 = Floor(Floor(Floor(基礎値 * サブクラス補正) * 種族補正) * 0.2)
    3. 合計 = メインクラス最終値 + マグ + サブクラス貢献度 + クラスブースト
    """
    
    # 選択されている設定の取得
    race = st.session_state['race_select']
    main_class = st.session_state['main_class_select']
    
    # 補正値/ボーナスを取得
    race_cor = RACE_CORRECTIONS.get(race, {})
    main_class_cor = CLASS_CORRECTIONS.get(main_class, {})
    mag_stats = st.session_state['mag_stats']
    sub_class_select = st.session_state['sub_class_select']
    
    # クラスブーストボーナス
    CB_BONUS = CLASS_BOOST_BONUS if st.session_state['class_boost_enabled'] else {k: 0 for k in CLASS_BOOST_BONUS.keys()}
    
    calculated_stats = {}

    for stat_name, base_val in NEW_BASE_STATS.items():
        # --- 1. メインクラスによるステータス計算 (HP/PP含む) ---
        
        # 1-1. メインクラス補正適用 (切り捨て)
        main_class_multiplier = main_class_cor.get(stat_name, 1.0)
        main_after_class = int(base_val * main_class_multiplier)

        # 1-2. 種族補正適用 (切り捨て)
        race_multiplier = race_cor.get(stat_name, 1.0)
        main_final_value = int(main_after_class * race_multiplier)
        
        total_value = main_final_value

        # --- 2. サブクラス貢献度 & マグ (ATK/DEF/ACC/技量のみ) ---
        
        # HP/PPにはサブクラス、マグの寄与は無い
        if stat_name not in ['HP', 'PP']:
            
            # マグボーナス加算
            mag_bonus = mag_stats.get(stat_name, 0)
            total_value += mag_bonus
            
            sub_contribution = 0
            
            # サブクラスが設定されており、かつメインクラスが後継クラスではない場合
            # メインクラスが後継クラスの場合、sub_class_selectは強制的に'None'になるため、このチェックは不要だが、念のため。
            if sub_class_select != 'None':
                sub_cor = CLASS_CORRECTIONS.get(sub_class_select, {})
                sub_class_multiplier = sub_cor.get(stat_name, 1.0)

                # 2-1. サブクラス補正適用 (切り捨て)
                # 基礎値から計算を始める
                sub_after_class = int(base_val * sub_class_multiplier)

                # 2-2. 種族補正適用 (切り捨て)
                sub_after_race = int(sub_after_class * race_multiplier)
                
                # 2-3. サブクラス貢献度 20% 適用 (切り捨て)
                # 確定ロジック: 最終補正の0.2倍にも切り捨てを適用する
                sub_contribution = int(sub_after_race * 0.2)
                
                total_value += sub_contribution

        # --- 3. クラスブースト/その他固定値加算 ---
        
        # クラスブースト増加分 (全ステータス共通)
        total_value += CB_BONUS.get(stat_name, 0)
        
        calculated_stats[stat_name] = total_value
        
    return calculated_stats

# =================================================================
# Streamlit UI
# =================================================================

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
    if main_class in SUCCESSOR_MAIN_CLASSES:
        # メインクラスが後継クラス (Hr, Ph, Et, Lu) の場合、サブクラスは "None" 固定
        st.selectbox(
            "サブクラス",
            options=["None"],
            index=0,
            key="sub_class_select",
            disabled=True,
        )
        # 状態を強制的に"None"に設定
        if st.session_state.get('sub_class_select') != "None":
            st.session_state['sub_class_select'] = "None" 

        st.info(f"{main_class}は後継クラスのため、サブクラスはNone固定です。", icon="ℹ️")
    else:
        # メインクラスが旧クラスの場合
        # サブクラスの選択肢からメインクラス自身と【Hrのみ】を除外する
        sub_class_options_filtered = ["None"] + [
            c for c in ALL_CLASSES 
            if c != main_class and c not in UNAVAILABLE_SUBCLASSES # Hrは選択肢から除外
        ]

        st.selectbox(
            "サブクラス",
            options=sub_class_options_filtered,
            key="sub_class_select",
        )
        
        # 選択されたサブクラスがHrだった場合（過去のセッションステート等で残っていた場合）
        if st.session_state.get('sub_class_select') == "Hr":
            st.warning("Hrはサブクラスに設定できません。Noneに戻します。")
            st.session_state['sub_class_select'] = "None"
            st.rerun()


st.markdown("---")

# =================================================================
# 2. 種族設定
# =================================================================

# --- 種族セクション ---
st.subheader("種族設定")

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

st.markdown("---")

# =================================================================
# 3. マグ設定
# =================================================================

st.subheader("マグ設定")

# 合計値の計算とチェック
current_total_mag = sum(st.session_state['mag_stats'].values())
MAG_MAX_TOTAL = 200

# --- マグの合計値を最初に表示 ---
st.markdown(f"**合計値:** **`{current_total_mag} / {MAG_MAX_TOTAL}`**")

if current_total_mag > MAG_MAX_TOTAL:
    st.error(f"マグの合計値が上限の {MAG_MAX_TOTAL} を超えています！")
elif current_total_mag == MAG_MAX_TOTAL:
    st.success("マグの合計値が上限に達しました。", icon="✅")

# マグの数値入力 (3列で配置)
mag_cols = st.columns(3) 

# 入力欄の生成 (打撃力, 射撃力, 法撃力)
for i, field in enumerate(["打撃力", "射撃力", "法撃力"]):
    with mag_cols[0]:
        st.number_input(
            field,
            min_value=0,
            max_value=MAG_MAX_TOTAL, 
            key=f"mag_input_{field}",
            value=st.session_state['mag_stats'].get(field, 0),
            step=1,
            label_visibility="visible",
            on_change=lambda f=field: st.session_state['mag_stats'].__setitem__(f, st.session_state[f"mag_input_{f}"])
        )

# 入力欄の生成 (打撃防御, 射撃防御, 法撃防御)
for i, field in enumerate(["打撃防御", "射撃防御", "法撃防御"]):
    with mag_cols[1]:
        st.number_input(
            field,
            min_value=0,
            max_value=MAG_MAX_TOTAL, 
            key=f"mag_input_{field}",
            value=st.session_state['mag_stats'].get(field, 0),
            step=1,
            label_visibility="visible",
            on_change=lambda f=field: st.session_state['mag_stats'].__setitem__(f, st.session_state[f"mag_input_{f}"])
        )

# 入力欄の生成 (技量)
with mag_cols[2]:
    field = "技量"
    st.number_input(
        field,
        min_value=0,
        max_value=MAG_MAX_TOTAL, 
        key=f"mag_input_{field}",
        value=st.session_state['mag_stats'].get(field, 0),
        step=1,
        label_visibility="visible",
        on_change=lambda f=field: st.session_state['mag_stats'].__setitem__(f, st.session_state[f"mag_input_{f}"])
    )

st.markdown("---")

# --- クラスブースト設定 ---
st.subheader("クラスブースト設定")

# クラスブーストチェックボックス
st.checkbox(
    "クラスブースト（全クラスLv75達成）",
    key="class_boost_enabled",
    value=st.session_state['class_boost_enabled'],
    help="チェックを入れると、HP+60, PP+10, 攻撃力+120, 技量+60, 防御力+90が加算されます。"
)

st.markdown("---")

# =================================================================
# 4. 合計基本ステータス表示 (計算結果表示)
# =================================================================

# 補正込みの合計値を計算
total_stats = get_calculated_stats()

st.subheader("合計基本ステータス (計算式適用後)")

st.markdown(f"##### (Lv100基礎値 ({NEW_BASE_STATS['打撃力']}など) + 種族/クラス補正 + クラスブースト + マグ)")
st.caption(f"※ 計算は**全ステップで厳密に切り捨て ($\text{{INT}}$) を適用**しています。")

# ステータス表示を整頓
stat_pairs = [
    ("打撃力", "打撃防御"),
    ("射撃力", "射撃防御"),
    ("法撃力", "法撃防御"),
    ("技量", None),
    ("HP", "PP")
]

for stat1_name, stat2_name in stat_pairs:
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label=f"{stat1_name} (Total)", value=f"{total_stats[stat1_name]}")
    
    if stat2_name:
        with col2:
            st.metric(label=f"{stat2_name} (Total)", value=f"{total_stats[stat2_name]}")

st.markdown("---")

# =================================================================
# 5. エクスポート/インポート機能 (in / out)
# =================================================================

st.subheader("mysetno (エクスポート/インポート)")

export_data = {
    "main_class": st.session_state['main_class_select'],
    "sub_class": st.session_state['sub_class_select'],
    "skills": st.session_state['skills_data'], 
    "race": st.session_state['race_select'],
    "mag_stats": st.session_state['mag_stats'], 
    "class_boost_enabled": st.session_state['class_boost_enabled'],
    "version": "pso2_dmg_calc_v15_hr_sub_fix" # バージョン名を更新
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
                         
            if "class_boost_enabled" in data:
                st.session_state['class_boost_enabled'] = data["class_boost_enabled"]

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
# 6. スキルツリー詳細設定
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
            st.info("ここにスキル名とレベル入力（スライダーまたは数値入力）のUIが入り、そのスキル効果が上記の基本ステータスやダメージ計算に反映されます。（未実装）")
else:
