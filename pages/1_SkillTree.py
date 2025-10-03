import streamlit as st
import json
import math

st.set_page_config(layout="wide")

# =================================================================
# 1. 補正データ定義 (WIKI値と補正率)
# =================================================================

# --- WIKIから提供されたLv100メインクラス補正済み基礎値 ---
# この値は、クラス補正は適用済みだが、種族補正は未適用という前提で利用します。
WIKI_MAIN_STATS = {
    "Hu": {"HP": 764, "PP": 120, "打撃力": 580, "射撃力": 540, "法撃力": 451, "技量": 415, "打撃防御": 580, "射撃防御": 451, "法撃防御": 451},
    "Fi": {"HP": 655, "PP": 120, "打撃力": 580, "射撃力": 450, "法撃力": 540, "技量": 415, "打撃防御": 580, "射撃防御": 450, "法撃防御": 450},
    "Ra": {"HP": 645, "PP": 120, "打撃力": 540, "射撃力": 580, "法撃力": 450, "技量": 415, "打撃防御": 450, "射撃防御": 580, "法撃防御": 450},
    "Gu": {"HP": 650, "PP": 120, "打撃力": 540, "射撃力": 580, "法撃力": 450, "技量": 415, "打撃防御": 450, "射撃防御": 580, "法撃防御": 450},
    "Fo": {"HP": 536, "PP": 120, "打撃力": 450, "射撃力": 540, "法撃力": 580, "技量": 415, "打撃防御": 450, "射撃防御": 450, "法撃防御": 580},
    "Te": {"HP": 536, "PP": 120, "打撃力": 540, "射撃力": 450, "法撃力": 580, "技量": 415, "打撃防御": 580, "射撃防御": 450, "法撃防御": 450},
    "Br": {"HP": 655, "PP": 120, "打撃力": 545, "射撃力": 545, "法撃力": 486, "技量": 420, "打撃防御": 488, "射撃防御": 488, "法撃防御": 488},
    "Bo": {"HP": 655, "PP": 120, "打撃力": 545, "射撃力": 486, "法撃力": 545, "技量": 420, "打撃防御": 488, "射撃防御": 488, "法撃防御": 488},
    "Su": {"HP": 645, "PP": 120, "打撃力": 545, "射撃力": 545, "法撃力": 545, "技量": 420, "打撃防御": 488, "射撃防御": 488, "法撃防御": 488},
    "Hr": {"HP": 804, "PP": 120, "打撃力": 698, "射撃力": 698, "法撃力": 698, "技量": 549, "打撃防御": 697, "射撃防御": 697, "法撃防御": 697},
    "Ph": {"HP": 780, "PP": 120, "打撃力": 711, "射撃力": 711, "法撃力": 711, "技量": 564, "打撃防御": 659, "射撃防御": 659, "法撃防御": 659},
    "Et": {"HP": 819, "PP": 120, "打撃力": 677, "射撃力": 677, "法撃力": 677, "技量": 543, "打撃防御": 730, "射撃防御": 730, "法撃防御": 730},
    "Lu": {"HP": 795, "PP": 120, "打撃力": 684, "射撃力": 684, "法撃力": 684, "技量": 576, "打撃防御": 710, "射撃防御": 710, "法撃防御": 710},
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

# --- クラスブーストの固定値 (全クラスLv75達成時のボーナス) ---
CLASS_BOOST_BONUS = {
    "HP": 60, "PP": 10, "打撃力": 120, "射撃力": 120, "法撃力": 120, "技量": 60, "打撃防御": 90, "射撃防御": 90, "法撃防御": 90
}
# -------------------------------------------------------------------

# マグのステータス定義
MAG_STATS_FIELDS = ["打撃力", "射撃力", "法撃力", "技量", "打撃防御", "射撃防御", "法撃防御"]
STATS_FIELDS = ["HP", "PP", "打撃力", "射撃力", "法撃力", "技量", "打撃防御", "射撃防御", "法撃防御"]
ALL_CLASSES = list(WIKI_MAIN_STATS.keys())
UNAVAILABLE_SUBCLASSES = ["Hr"]
SUCCESSOR_MAIN_CLASSES = ["Hr", "Ph", "Et", "Lu"]

# --- 四捨五入関数 (X.5で繰り上げ) ---
def custom_round(num):
    """メインクラスの種族補正適用時に使用する、標準的な四捨五入（X.5で繰り上げ）"""
    return int(num + 0.5)

# --- セッションステートの初期化 ---
# 前回の設定値を保持
if 'main_class_select' not in st.session_state: st.session_state['main_class_select'] = "Gu" 
if 'sub_class_select' not in st.session_state: st.session_state['sub_class_select'] = "Lu" 
if 'race_select' not in st.session_state: st.session_state['race_select'] = "キャスト女" 
if 'mag_stats' not in st.session_state: 
    st.session_state['mag_stats'] = {field: 200 if field == "射撃力" else 0 for field in MAG_STATS_FIELDS}
if 'class_boost_enabled' not in st.session_state: st.session_state['class_boost_enabled'] = True 

# =================================================================
# 2. 計算関数 (WIKI値起点 + 全ステップ切り捨て適用)
# =================================================================

def get_calculated_stats():
    """
    WIKIのクラス補正済み基礎値に、種族補正、マグ、サブクラス貢献度、クラスブーストを合算した基本ステータスを計算します。
    
    ロジックの順序:
    1. メインクラス最終値 = ROUND(WIKI_MAIN_STATS[メインクラス] * 種族補正)
    2. サブクラス貢献度 = Floor(Floor(WIKI_MAIN_STATS[サブクラス] * 種族補正) * 0.2)
    3. 合計 = メインクラス最終値 + マグ + サブクラス貢献度 + クラスブースト
    """
    
    race = st.session_state['race_select']
    main_class = st.session_state['main_class_select']
    sub_class_select = st.session_state['sub_class_select']
    
    race_cor = RACE_CORRECTIONS.get(race, {})
    mag_stats = st.session_state['mag_stats']
    
    # クラスブーストボーナス
    CB_BONUS = CLASS_BOOST_BONUS if st.session_state['class_boost_enabled'] else {k: 0 for k in CLASS_BOOST_BONUS.keys()}
        
    calculated_stats = {}

    for stat_name in STATS_FIELDS:
        # WIKIからクラス補正済み基礎値を取得
        wiki_main_base_val = WIKI_MAIN_STATS.get(main_class, {}).get(stat_name, 0)
        
        # --- 1. メインクラスによるステータス計算 ---
        
        # 1-1. 種族補正適用 (四捨五入)
        # HPとPPは特別な計算ルールがあるため、HP/PPのみ切り捨てを維持し、他のATK/DEF/技量は四捨五入を適用
        race_multiplier = race_cor.get(stat_name, 1.0)
        
        if stat_name in ['HP', 'PP']:
             # HPとPPは常に切り捨てを適用
            main_final_value = int(wiki_main_base_val * race_multiplier)
        else:
            # ATK/DEF/技量は四捨五入を適用 (法防の1ポイントズレを解消)
            main_final_value = custom_round(wiki_main_base_val * race_multiplier)
        
        total_value = main_final_value

        # --- 2. サブクラス貢献度 & マグ (ATK/DEF/ACC/技量のみ) ---
        
        if stat_name not in ['HP', 'PP']:
            
            # マグボーナス加算
            mag_bonus = mag_stats.get(stat_name, 0)
            total_value += mag_bonus
            
            sub_contribution = 0
            
            # サブクラスが設定されており、かつメインクラスが後継クラスではない場合
            if sub_class_select != 'None' and main_class not in SUCCESSOR_MAIN_CLASSES:
                
                # サブクラスのWIKI値を取得
                wiki_sub_base_val = WIKI_MAIN_STATS.get(sub_class_select, {}).get(stat_name, 0)

                # 2-1. 種族補正適用 (切り捨て) - WIKI値から計算を始める
                sub_after_race = int(wiki_sub_base_val * race_multiplier)
                
                # 2-2. サブクラス貢献度 20% 適用 (切り捨て)
                sub_contribution = int(sub_after_race * 0.2)
                
                total_value += sub_contribution

        # --- 3. クラスブースト加算 ---
        
        # クラスブースト増加分 (全ステータス共通)
        total_value += CB_BONUS.get(stat_name, 0)
                
        calculated_stats[stat_name] = total_value
        
    return calculated_stats

# =================================================================
# Streamlit UI
# =================================================================

st.title("📚 1. ステータス計算機 (WIKI基礎値採用版)")
st.caption("※ 法防のズレ解消のため、ATK/DEF/技量のメインクラス補正に四捨五入を適用しました。HP/PPは切り捨てを維持しています。")

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
        if st.session_state.get('sub_class_select') != "None":
            st.session_state['sub_class_select'] = "None" 

        st.info(f"{main_class}は後継クラスのため、サブクラスはNone固定です。", icon="ℹ️")
    else:
        # メインクラスが旧クラスの場合
        sub_class_options_filtered = ["None"] + [
            c for c in ALL_CLASSES 
            if c != main_class and c not in UNAVAILABLE_SUBCLASSES 
        ]

        st.selectbox(
            "サブクラス",
            options=sub_class_options_filtered,
            key="sub_class_select",
        )
        if st.session_state.get('sub_class_select') == "Hr":
            st.warning("Hrはサブクラスに設定できません。Noneに戻します。")
            st.session_state['sub_class_select'] = "None"
            st.rerun()


st.markdown("---")

# =================================================================
# 2. 種族設定
# =================================================================

st.subheader("種族設定")

RACE_OPTIONS = list(RACE_CORRECTIONS.keys())
st.selectbox(
    "種族",
    options=RACE_OPTIONS,
    key="race_select",
)

st.markdown("---")

# =================================================================
# 3. マグ設定とクラスブースト
# =================================================================

st.subheader("マグ/クラスブースト設定")

# --- マグの入力 ---
st.markdown("##### マグのステータス")
# マグの合計値を最初に表示
current_total_mag = sum(st.session_state['mag_stats'].values())
MAG_MAX_TOTAL = 200
st.markdown(f"**合計値:** **`{current_total_mag} / {MAG_MAX_TOTAL}`**")

if current_total_mag > MAG_MAX_TOTAL:
    st.error(f"マグの合計値が上限の {MAG_MAX_TOTAL} を超えています！")
elif current_total_mag == MAG_MAX_TOTAL:
    st.success("マグの合計値が上限に達しました。", icon="✅")

# マグの数値入力 (3列で配置)
mag_cols = st.columns(3) 

mag_fields = [
    ["打撃力", "射撃力", "法撃力"],
    ["打撃防御", "射撃防御", "法撃防御"],
    ["技量"]
]

def update_mag_stats(field):
    st.session_state['mag_stats'][field] = st.session_state[f"mag_input_{field}"]

for col_idx, fields in enumerate(mag_fields):
    with mag_cols[col_idx]:
        for field in fields:
            st.number_input(
                field,
                min_value=0,
                max_value=MAG_MAX_TOTAL, 
                key=f"mag_input_{field}",
                value=st.session_state['mag_stats'].get(field, 0),
                step=1,
                label_visibility="visible",
                on_change=update_mag_stats,
                args=(field,)
            )

# --- クラスブースト設定 ---
st.markdown("##### クラスブースト")
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

st.subheader("合計基本ステータス (最終理論値)")

st.markdown(f"##### (WIKIクラス値 + 種族補正 + マグ + サブ貢献度 + クラスブースト)")
st.caption(f"※ ATK/DEF/技量はメインクラス補正時のみ**四捨五入**、その他は**切り捨て**を適用しています。")

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
