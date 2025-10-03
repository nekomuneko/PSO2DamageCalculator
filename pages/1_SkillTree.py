# pages/1_SkillTree.py

import streamlit as st
import json
import math 

st.set_page_config(layout="wide")

# =================================================================
# 1. 補正データ定義 (拡張性のため、ここに静的データを集約)
# =================================================================

# --- プレイヤー基礎ステータス (固定値) ---
# 基礎ステータス入力UIを削除したため、これらの値を定数として使用します。
BASE_HP_CONST = 650
BASE_PP_CONST = 120
BASE_ATK_CONST = 540       # 打撃力、射撃力、法撃力の基礎値
BASE_DEF_CONST = 450       # 打撃防御、射撃防御、法撃防御の基礎値
BASE_ACCURACY_CONST = 415  # 技量の基礎値

# --- 種族補正データ (乗算補正: 1.05 = +5%, 0.95 = -5%) ---
# 最終的な計算は小数点以下を四捨五入(round)または切り捨て(int/floor)
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

# --- クラス補正データ (乗算補正: ユーザー提供データに基づき更新) ---
CLASS_CORRECTIONS = {
    "Hu": {"HP": 1.18, "PP": 1.00, "打撃力": 1.07, "射撃力": 1.00, "法撃力": 0.83, "技量": 1.00, "打撃防御": 1.29, "射撃防御": 1.00, "法撃防御": 1.00}, # ハンター
    "Fi": {"HP": 1.01, "PP": 1.00, "打撃力": 1.07, "射撃力": 0.83, "法撃力": 1.00, "技量": 1.00, "打撃防御": 1.29, "射撃防御": 1.00, "法撃防御": 1.00}, # ファイター
    "Ra": {"HP": 0.99, "PP": 1.00, "打撃力": 1.00, "射撃力": 1.07, "法撃力": 0.83, "技量": 1.00, "打撃防御": 1.00, "射撃防御": 1.29, "法撃防御": 1.00}, # レンジャー
    "Gu": {"HP": 1.00, "PP": 1.00, "打撃力": 1.00, "射撃力": 1.07, "法撃力": 0.83, "技量": 1.00, "打撃防御": 1.00, "射撃防御": 1.29, "法撃防御": 1.00}, # ガンナー
    "Fo": {"HP": 0.82, "PP": 1.00, "打撃力": 0.83, "射撃力": 1.00, "法撃力": 1.07, "技量": 1.00, "打撃防御": 1.00, "射撃防御": 1.00, "法撃防御": 1.29}, # フォース
    "Te": {"HP": 0.82, "PP": 1.00, "打撃力": 1.00, "射撃力": 0.83, "法撃力": 1.07, "技量": 1.00, "打撃防御": 1.29, "射撃防御": 1.00, "法撃防御": 1.00}, # テクター
    "Br": {"HP": 1.01, "PP": 1.00, "打撃力": 1.01, "射撃力": 1.01, "法撃力": 0.90, "技量": 1.01, "打撃防御": 1.08, "射撃防御": 1.08, "法撃防御": 1.08}, # ブレイバー
    "Bo": {"HP": 1.01, "PP": 1.00, "打撃力": 1.01, "射撃力": 0.90, "法撃力": 1.01, "技量": 1.01, "打撃防御": 1.08, "射撃防御": 1.08, "法撃防御": 1.08}, # バウンサー
    "Su": {"HP": 0.99, "PP": 1.00, "打撃力": 1.01, "射撃力": 1.01, "法撃力": 1.01, "技量": 1.01, "打撃防御": 1.08, "射撃防御": 1.08, "法撃防御": 1.08}, # サモナー
    # 後継クラス
    "Hr": {"HP": 1.24, "PP": 1.00, "打撃力": 1.29, "射撃力": 1.29, "法撃力": 1.29, "技量": 1.32, "打撃防御": 1.55, "射撃防御": 1.55, "法撃防御": 1.55}, # ヒーロー
    "Ph": {"HP": 1.20, "PP": 1.00, "打撃力": 1.32, "射撃力": 1.32, "法撃力": 1.32, "技量": 1.36, "打撃防御": 1.46, "射撃防御": 1.46, "法撃防御": 1.46}, # ファントム
    "Et": {"HP": 1.26, "PP": 1.00, "打撃力": 1.25, "射撃力": 1.25, "法撃力": 1.25, "技量": 1.31, "打撃防御": 1.62, "射撃防御": 1.62, "法撃防御": 1.62}, # エトワール
    "Lu": {"HP": 1.22, "PP": 1.00, "打撃力": 1.27, "射撃力": 1.27, "法撃力": 1.27, "技量": 1.39, "打撃防御": 1.58, "射撃防御": 1.58, "法撃防御": 1.58}, # ラスター
}

# --- クラスブーストの固定値 (全クラスLv75達成時のボーナス) ---
CLASS_BOOST_BONUS = {
    "HP": 60, 
    "PP": 10, 
    "打撃力": 120, "射撃力": 120, "法撃力": 120, 
    "技量": 60, 
    "打撃防御": 90, "射撃防御": 90, "法撃防御": 90
}
# -------------------------------------------------------------------

# --- マグのステータス定義 ---
MAG_STATS_FIELDS = ["打撃力", "射撃力", "法撃力", "技量", "打撃防御", "射撃防御", "法撃防御"]

# --- セッションステートの初期化 ---
if 'main_class_select' not in st.session_state:
    st.session_state['main_class_select'] = "Br" 
if 'sub_class_select' not in st.session_state:
    st.session_state['sub_class_select'] = "None"
if 'skills_data' not in st.session_state:
    st.session_state['skills_data'] = {}
    
# 種族 (Race)
if 'race_select' not in st.session_state:
    st.session_state['race_select'] = "ヒューマン男"

# マグ (Mag Stats)
if 'mag_stats' not in st.session_state:
    st.session_state['mag_stats'] = {field: 0 for field in MAG_STATS_FIELDS}

# --- スキルツリー固定値ボーナス ---
# ※ 計算には反映しないが、入力UIには表示できるように維持
if 'st_fixed_bonus' not in st.session_state:
    st.session_state['st_fixed_bonus'] = {
        "HP": 50, 
        "PP": 10, 
        "打撃力": 50, "射撃力": 160, "法撃力": 50, 
        "技量": 50,
        "打撃防御": 50, "射撃防御": 50, "法撃防御": 50, 
    }

# --- クラスブーストON/OFF ---
if 'class_boost_enabled' not in st.session_state:
    st.session_state['class_boost_enabled'] = True 
# --------------------------------------------------

# -------------------------------------------------------------------
# クラス定義
# -------------------------------------------------------------------
ALL_CLASSES = ["Hu", "Fi", "Ra", "Gu", "Fo", "Te", "Br", "Bo", "Su", "Hr", "Ph", "Et", "Lu"]
SUB_CLASSES_CANDIDATES = [c for c in ALL_CLASSES if c != "Hr"]
# -------------------------------------------------------------------

# =================================================================
# 2. 計算関数
# =================================================================

def get_calculated_stats():
    """
    ユーザー入力、種族補正、クラス補正、マグ補正、クラスブーストを合算した基本ステータスを計算します。
    【重要】お客様情報に基づき、ATK/DEF/ACC/技量の乗算補正には四捨五入（round）を適用します。
    
    計算式: 
    [ATK/DEF/ACC/技量]: ROUND(ROUND(基礎値 * 種族補正) * メイン補正) + INT(サブクラス値 * 0.2) + マグ + クラスブースト
    [HP/PP]: INT(INT(基礎値 * 種族補正) * メイン補正) + クラスブースト (HP/PPは切り捨てを維持)
    """
    
    # 選択されている設定の取得
    race = st.session_state['race_select']
    main_class = st.session_state['main_class_select']
    
    # 補正値/ボーナスを取得
    race_cor = RACE_CORRECTIONS.get(race, {})
    class_cor = CLASS_CORRECTIONS.get(main_class, {})
    mag_stats = st.session_state['mag_stats']
    sub_class_select = st.session_state['sub_class_select']

    # 計算に使う固定基礎値の定義
    BASE_ATK_VAL = BASE_ATK_CONST
    BASE_DEF_VAL = BASE_DEF_CONST
    BASE_ACCURACY_VAL = BASE_ACCURACY_CONST
    BASE_HP = BASE_HP_CONST
    BASE_PP = BASE_PP_CONST
        
    # クラスブーストボーナス
    CB_BONUS = CLASS_BOOST_BONUS if st.session_state['class_boost_enabled'] else {k: 0 for k in CLASS_BOOST_BONUS.keys()}
    
    calculated_stats = {}

    def calculate_stat(stat_name, base_stat_type):
        """
        特定のステータスを計算するヘルパー関数
        base_stat_type: 'atk', 'def', 'acc', 'hp', 'pp'
        """
        
        # 基礎値の取得
        if base_stat_type == 'atk': base_val = BASE_ATK_VAL
        elif base_stat_type == 'def': base_val = BASE_DEF_VAL
        elif base_stat_type == 'acc': base_val = BASE_ACCURACY_VAL
        elif base_stat_type == 'hp': base_val = BASE_HP
        elif base_stat_type == 'pp': base_val = BASE_PP
        else: return 0

        # --- 乗算補正の取得 ---
        race_multiplier = race_cor.get(stat_name, 1.0)
        main_class_multiplier = class_cor.get(stat_name, 1.0)
        
        # HP/PPの計算: 切り捨て(INT)を維持
        if base_stat_type in ['hp', 'pp']:
            # 1. 種族補正適用 (INT(基礎値 * 種族補正))
            base_after_race = int(base_val * race_multiplier)
            # 2. メインクラス貢献分: INT(↑ * メインクラス補正)
            main_contribution = int(base_after_race * main_class_multiplier)
            total_value = main_contribution
            
            # HP/PPにはサブクラス・マグボーナス無し
            
        else:
            # ATK/DEF/ACC/技量の計算: お客様情報に基づき、乗算補正には四捨五入(ROUND)を適用
            
            # 1. 種族補正適用 (ROUND(基礎値 * 種族補正))
            base_after_race = round(base_val * race_multiplier)

            # 2. メインクラス貢献分: ROUND(↑ * メインクラス補正)
            main_contribution = round(base_after_race * main_class_multiplier)
            total_value = main_contribution

            # 3. サブクラス貢献分 (Hr/Ph/Et/Luはサブクラス設定不可)
            if sub_class_select != 'None':
                sub_cor = CLASS_CORRECTIONS.get(sub_class_select, {})
                sub_class_multiplier = sub_cor.get(stat_name, 1.0)

                # サブクラス値: ROUND(ROUND(基礎値 * 種族補正) * サブクラス補正)
                # サブクラス値の計算にも四捨五入を適用
                sub_class_stat_value_before_mult = round(base_after_race * sub_class_multiplier)
                
                # サブクラス貢献分: INT(サブクラス値 * 0.2) (0.2倍のボーナスは切り捨ての可能性が高いためINTを維持)
                sub_contribution = int(sub_class_stat_value_before_mult * 0.2)
                total_value += sub_contribution
            
            # 4. マグ増加分
            if stat_name in mag_stats: 
                mag_bonus = mag_stats.get(stat_name, 0)
                total_value += mag_bonus

        # 5. クラスブースト増加分 (全ステータス共通)
        total_value += CB_BONUS.get(stat_name, 0)
        
        # 6. スキルツリー固定値ボーナス増加分 (計算には含めない)
        
        return total_value

    # --- 計算実行 ---
    # ステータス名と対応する基礎値タイプをマッピング
    stat_mapping = {
        "打撃力": 'atk', "射撃力": 'atk', "法撃力": 'atk',
        "打撃防御": 'def', "射撃防御": 'def', "法撃防御": 'def',
        "技量": 'acc',
        "HP": 'hp', "PP": 'pp' 
    }

    for stat, base_type in stat_mapping.items():
        calculated_stats[stat] = calculate_stat(stat, base_type)
        
    return calculated_stats

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
# 2. 種族 / マグ設定
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

# --- マグセクション ---
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

# マグの数値入力 (2列で配置: 攻撃/防御, 技量)
mag_cols = st.columns([1, 1, 1]) 

# 入力欄の生成
# 打撃力, 射撃力, 法撃力
for field in ["打撃力", "射撃力", "法撃力"]:
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

# 打撃防御, 射撃防御, 法撃防御
for field in ["打撃防御", "射撃防御", "法撃防御"]:
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

# 技量
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
# 3. 合計基本ステータス表示 (計算結果表示)
# =================================================================

# 補正込みの合計値を計算
total_stats = get_calculated_stats()

st.subheader("合計基本ステータス (計算式適用後)")

st.markdown("##### (基礎値 + 種族補正 + クラス補正 + クラスブースト + マグ)")
st.caption(f"※ 基礎値: HP:{BASE_HP_CONST}, PP:{BASE_PP_CONST}, 攻撃力:{BASE_ATK_CONST}, 防御力:{BASE_DEF_CONST}, 技量:{BASE_ACCURACY_CONST}")

col_atk, col_def = st.columns(2)

# 打撃力 / 打撃防御
with col_atk:
    st.metric(label="打撃力 (Total)", value=f"{total_stats['打撃力']}")
with col_def:
    st.metric(label="打撃防御 (Total)", value=f"{total_stats['打撃防御']}")

# 射撃力 / 射撃防御
col_atk, col_def = st.columns(2)
with col_atk:
    st.metric(label="射撃力 (Total)", value=f"{total_stats['射撃力']}")
with col_def:
    st.metric(label="射撃防御 (Total)", value=f"{total_stats['射撃防御']}")

# 法撃力 / 法撃防御
col_atk, col_def = st.columns(2)
with col_atk:
    st.metric(label="法撃力 (Total)", value=f"{total_stats['法撃力']}")
with col_def:
    st.metric(label="法撃防御 (Total)", value=f"{total_stats['法撃防御']}")

# 技量
st.metric(label="技量 (Total)", value=f"{total_stats['技量']}")

# HP/PP
col_hp, col_pp = st.columns(2)
with col_hp:
    st.metric(label="合計HP", value=f"{total_stats['HP']}")
with col_pp:
    st.metric(label="合計PP", value=f"{total_stats['PP']}")


st.markdown("---")

# =================================================================
# 4. スキルツリー固定値ボーナス設定 (計算には未反映)
# =================================================================
st.subheader("スキルツリー固定値ボーナス (調整用)")
st.caption("※ **現在、このセクションで入力された数値は、合計基本ステータスには加算されていません。** ズレを確認するための一時的な入力欄です。")

st_bonus_cols = st.columns(4)

# 入力値の更新関数
def update_st_bonus(field):
    """スキルツリーボーナスの値をセッションステートに保存するコールバック"""
    st.session_state['st_fixed_bonus'][field] = st.session_state[f'st_bonus_input_{field}']

# HP / PP
with st_bonus_cols[0]:
    # HP
    st.number_input(
        "HP (STボーナス)",
        min_value=0,
        key='st_bonus_input_HP',
        value=st.session_state['st_fixed_bonus']['HP'],
        step=1,
        on_change=lambda f='HP': update_st_bonus(f)
    )
    # PP
    st.number_input(
        "PP (STボーナス)",
        min_value=0,
        key='st_bonus_input_PP',
        value=st.session_state['st_fixed_bonus']['PP'],
        step=1,
        on_change=lambda f='PP': update_st_bonus(f)
    )

# 攻撃力
for i, field in enumerate(["打撃力", "射撃力", "法撃力"]):
    with st_bonus_cols[1 + (i // 3)]: # 1列目 (攻撃力)
        st.number_input(
            f"{field} (STボーナス)",
            min_value=0,
            key=f'st_bonus_input_{field}',
            value=st.session_state['st_fixed_bonus'][field],
            step=1,
            on_change=lambda f=field: update_st_bonus(f)
        )
# 技量
with st_bonus_cols[2]:
    field = "技量"
    st.number_input(
        f"{field} (STボーナス)",
        min_value=0,
        key=f'st_bonus_input_{field}',
        value=st.session_state['st_fixed_bonus'][field],
        step=1,
        on_change=lambda f=field: update_st_bonus(f)
    )

# 防御力
for i, field in enumerate(["打撃防御", "射撃防御", "法撃防御"]):
    with st_bonus_cols[3]: # 4列目 (防御力)
        st.number_input(
            f"{field} (STボーナス)",
            min_value=0,
            key=f'st_bonus_input_{field}',
            value=st.session_state['st_fixed_bonus'][field],
            step=1,
            on_change=lambda f=field: update_st_bonus(f)
        )

st.markdown("---")

# =================================================================
# 5. エクスポート/インポート機能 (in / out)
# =================================================================

st.subheader("mysetno (エクスポート/インポート)")

export_data = {
    # 既存のデータ
    "main_class": st.session_state['main_class_select'],
    "sub_class": st.session_state['sub_class_select'],
    "skills": st.session_state['skills_data'], 
    
    "race": st.session_state['race_select'],
    "mag_stats": st.session_state['mag_stats'], 
    
    # クラスブースト設定値
    "class_boost_enabled": st.session_state['class_boost_enabled'],
    
    # スキルツリー固定値（入力値）をエクスポート
    "st_fixed_bonus": st.session_state['st_fixed_bonus'], 

    "version": "pso2_dmg_calc_v7_round_correction"
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
                         
            # クラスブーストのインポート
            if "class_boost_enabled" in data:
                st.session_state['class_boost_enabled'] = data["class_boost_enabled"]

            # スキルツリー固定値のインポート (新しい項目)
            if "st_fixed_bonus" in data:
                 st.session_state['st_fixed_bonus'] = data["st_fixed_bonus"]
                 # UIの更新
                 for field, value in data["st_fixed_bonus"].items():
                    if f"st_bonus_input_{field}" in st.session_state:
                        st.session_state[f"st_bonus_input_{field}"] = value
                         

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
            st.info("ここにスキル名とレベル入力（スライダーまたは数値入力）のUIが入り、そのスキル効果が上記の基本ステータスやダメージ計算に反映されます。")
else:
    st.warning("クラスが選択されていません。")
