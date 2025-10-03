# pages/1_SkillTree.py

import streamlit as st
import json
import math # math.floorやint()で小数点以下を切り捨てる

st.set_page_config(layout="wide")

# =================================================================
# 1. 補正データ定義 (拡張性のため、ここに静的データを集約)
# =================================================================

# --- 種族補正データ (乗算補正: 1.05 = +5%, 0.95 = -5%) ---
# 最終的な計算は小数点以下を切り捨て。
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
# -------------------------------------------------------------------

# --- マグのステータス定義 ---
MAG_STATS_FIELDS = ["打撃力", "射撃力", "法撃力", "技量", "打撃防御", "射撃防御", "法撃防御"]

# --- セッションステートの初期化 ---
if 'main_class_select' not in st.session_state:
    st.session_state['main_class_select'] = "Hu"
if 'sub_class_select' not in st.session_state:
    st.session_state['sub_class_select'] = "None"
if 'skills_data' not in st.session_state:
    st.session_state['skills_data'] = {}
    
# 装備・設定のダミー値（今回はユーザ入力として移動）
if 'gear_weapon_atk' not in st.session_state:
    st.session_state['gear_weapon_atk'] = 2000
if 'enemy_def' not in st.session_state:
    st.session_state['enemy_def'] = 1000

# プレイヤー基礎ステータス (初期値はユーザーの指定値)
if 'base_hp' not in st.session_state:
    st.session_state['base_hp'] = 650
if 'base_pp' not in st.session_state:
    st.session_state['base_pp'] = 120
if 'base_atk_val' not in st.session_state:
    st.session_state['base_atk_val'] = 540 
if 'base_def_val' not in st.session_state:
    st.session_state['base_def_val'] = 450 
if 'base_accuracy_val' not in st.session_state:
    st.session_state['base_accuracy_val'] = 415 

# 種族 (Race)
if 'race_select' not in st.session_state:
    st.session_state['race_select'] = "ヒューマン男"

# マグ (Mag Stats)
if 'mag_stats' not in st.session_state:
    st.session_state['mag_stats'] = {field: 0 for field in MAG_STATS_FIELDS}

# --- 新規追加: 加算ボーナス ---
# クラスブースト (+10) やS級特殊能力、クラススキルなどによる加算値
if 'additive_atk_acc_bonus' not in st.session_state:
    # デフォルトでクラスブースト分の +10 を想定
    st.session_state['additive_atk_acc_bonus'] = 10 
if 'additive_def_bonus' not in st.session_state:
    st.session_state['additive_def_bonus'] = 0 
# --------------------------------------------------

# -------------------------------------------------------------------
# クラス定義 (ご要望の並び順: Hu, FI, Ra, Gu, Fo, Te, Br, Bo, Su, Hr, Ph, Et, Lu)
# -------------------------------------------------------------------
ALL_CLASSES = ["Hu", "Fi", "Ra", "Gu", "Fo", "Te", "Br", "Bo", "Su", "Hr", "Ph", "Et", "Lu"]
SUB_CLASSES_CANDIDATES = [c for c in ALL_CLASSES if c != "Hr"]
# -------------------------------------------------------------------

# =================================================================
# 2. 計算関数
# =================================================================

def get_calculated_stats():
    """
    ユーザー入力、種族補正、クラス補正、マグ補正、加算ボーナスを合算した基本ステータスを計算します。
    計算式: INT(基礎値 * 種族補正 * メイン補正) + INT(サブクラス値 * 0.2) + 加算ボーナス
    """
    
    # 選択されている設定の取得
    race = st.session_state['race_select']
    main_class = st.session_state['main_class_select']
    
    # 補正値/ボーナスを取得
    race_cor = RACE_CORRECTIONS.get(race, {})
    class_cor = CLASS_CORRECTIONS.get(main_class, {})
    mag_stats = st.session_state['mag_stats']
    sub_class_select = st.session_state['sub_class_select']

    # 計算に使う基礎値の定義
    BASE_ATK_VAL = st.session_state['base_atk_val']
    BASE_DEF_VAL = st.session_state['base_def_val'] 
    BASE_ACCURACY_VAL = st.session_state['base_accuracy_val']
    BASE_HP = st.session_state['base_hp']
    BASE_PP = st.session_state['base_pp']
    
    # 加算ボーナス
    ADDITIVE_ATK_ACC_BONUS = st.session_state['additive_atk_acc_bonus']
    ADDITIVE_DEF_BONUS = st.session_state['additive_def_bonus']
    
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
        
        # 1. メインクラス貢献分: INT(基礎値 * 種族補正 * メインクラス補正)
        main_contribution = int(base_val * race_multiplier * main_class_multiplier)
        total_value = main_contribution

        # 2. サブクラス貢献分 (ATK/DEF/ACCのみ)
        if base_stat_type in ['atk', 'def', 'acc'] and sub_class_select != 'None':
            sub_cor = CLASS_CORRECTIONS.get(sub_class_select, {})
            sub_class_multiplier = sub_cor.get(stat_name, 1.0)

            # サブクラス値: INT(基礎値 * 種族補正 * サブクラス補正)
            # 既にメインクラス補正として使われた基礎値ではなく、改めて計算する
            sub_class_stat_value = int(base_val * race_multiplier * sub_class_multiplier)
            
            # サブクラス貢献分: INT(サブクラス値 * 0.2)
            sub_contribution = int(sub_class_stat_value * 0.2)
            total_value += sub_contribution
            
        # 3. マグ増加分 (ATK/DEF/ACCのみ)
        if base_stat_type in ['atk', 'def', 'acc']:
            mag_bonus = mag_stats.get(stat_name, 0)
            total_value += mag_bonus

        # 4. クラスブースト/S級特殊能力増加分 (加算ボーナス)
        if base_stat_type in ['atk', 'acc']:
             total_value += ADDITIVE_ATK_ACC_BONUS
        elif base_stat_type == 'def':
             total_value += ADDITIVE_DEF_BONUS

        return total_value

    # --- 計算実行 ---
    # ステータス名と対応する基礎値タイプをマッピング
    stat_mapping = {
        "打撃力": 'atk', "射撃力": 'atk', "法撃力": 'atk',
        "打撃防御": 'def', "射撃防御": 'def', "法撃防御": 'def',
        "技量": 'acc',
        "HP": 'hp', "PP": 'pp' # HP/PPはサブクラス・マグ・加算ボーナスの影響を受けない（スキルツリー設定で後で考慮）
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
# 2. 基本ステータス設定 (基礎値 / 種族 / マグ)
# =================================================================

# --- 基礎値セクション ---
st.subheader("プレイヤー基礎ステータス (Lv・クラス補正前)")
col_hp, col_pp, col_base_atk = st.columns(3)

with col_hp:
    st.number_input(
        "HP",
        min_value=1,
        max_value=9999,
        key="base_hp",
        value=st.session_state['base_hp'],
        step=1,
        help="キャラクターの基礎HPを入力します。"
    )

with col_pp:
    st.number_input(
        "PP",
        min_value=1,
        max_value=999,
        key="base_pp",
        value=st.session_state['base_pp'],
        step=1,
        help="キャラクターの基礎PPを入力します。"
    )

with col_base_atk:
    st.number_input(
        "攻撃力基礎値 (打/射/法)",
        min_value=0,
        max_value=9999,
        key="base_atk_val",
        value=st.session_state['base_atk_val'],
        step=1,
        help="打撃力、射撃力、法撃力の基礎値。"
    )
    
col_base_def, col_base_acc, col_empty = st.columns(3) # 防御と技量の入力欄を追加

with col_base_def:
    st.number_input(
        "防御力基礎値 (打防/射防/法防)",
        min_value=0,
        max_value=9999,
        key="base_def_val",
        value=st.session_state['base_def_val'],
        step=1,
        help="打撃防御、射撃防御、法撃防御の基礎値。"
    )

with col_base_acc:
    st.number_input(
        "技量基礎値",
        min_value=0,
        max_value=9999,
        key="base_accuracy_val",
        value=st.session_state['base_accuracy_val'],
        step=1,
        help="技量の基礎値。"
    )


st.markdown("---")

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
# 技量を単独で配置するため、3列目を確保し、技量以外を2列で管理する
mag_cols = st.columns([1, 1, 1]) # 攻撃系、防御系、技量

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

# --- 加算ボーナスセクション ---
st.subheader("その他の加算ボーナス")
st.markdown("##### (クラスブースト、S級特殊能力、クラススキルによる加算値)")

col_add_atk, col_add_def = st.columns(2)

with col_add_atk:
    st.number_input(
        "攻撃・技量 (打/射/法/技量)",
        min_value=0,
        max_value=999,
        key="additive_atk_acc_bonus",
        value=st.session_state['additive_atk_acc_bonus'],
        step=1,
        help="クラスブーストやS級特殊能力、攻撃系クラススキルなどによる加算ボーナスを入力します。（例：クラスブースト+10）"
    )

with col_add_def:
    st.number_input(
        "防御力 (打防/射防/法防)",
        min_value=0,
        max_value=999,
        key="additive_def_bonus",
        value=st.session_state['additive_def_bonus'],
        step=1,
        help="防御系クラススキルなどによる加算ボーナスを入力します。"
    )

st.markdown("---")

# =================================================================
# 3. 合計基礎ステータス表示 (計算結果表示)
# =================================================================

# 補正込みの合計値を計算
total_stats = get_calculated_stats()

st.subheader("合計基本ステータス (計算式適用後)")

st.markdown("##### (メインクラス補正 + サブクラス補正(0.2倍) + マグ + 加算ボーナス)")

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
    st.metric(label="射撃防御 (Total)", value=f"{total_stats['打撃防御']}")

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
    # HP/PPはサブクラス・マグ・加算ボーナスの影響をここでは受けないシンプルな計算
    st.metric(label="合計HP (基礎 + 種族 + クラス)", value=f"{total_stats['HP']}")
with col_pp:
    st.metric(label="合計PP (基礎 + 種族 + クラス)", value=f"{total_stats['PP']}")


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
    "base_hp": st.session_state['base_hp'],
    "base_pp": st.session_state['base_pp'],
    "base_atk_val": st.session_state['base_atk_val'],
    "base_def_val": st.session_state['base_def_val'],
    "base_accuracy_val": st.session_state['base_accuracy_val'],

    "race": st.session_state['race_select'],
    "mag_stats": st.session_state['mag_stats'], 
    
    # 新しい加算ボーナス値
    "additive_atk_acc_bonus": st.session_state['additive_atk_acc_bonus'],
    "additive_def_bonus": st.session_state['additive_def_bonus'],
    
    "version": "pso2_dmg_calc_v2"
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
            
            # 基礎ステータスのインポート
            if "base_hp" in data:
                st.session_state['base_hp'] = data["base_hp"]
            if "base_pp" in data:
                st.session_state['base_pp'] = data["base_pp"]
            if "base_atk_val" in data:
                st.session_state['base_atk_val'] = data["base_atk_val"]
            if "base_def_val" in data: 
                st.session_state['base_def_val'] = data["base_def_val"]
            if "base_accuracy_val" in data: 
                st.session_state['base_accuracy_val'] = data["base_accuracy_val"]

            if "race" in data:
                st.session_state['race_select'] = data["race"]
            if "mag_stats" in data:
                st.session_state['mag_stats'] = data["mag_stats"]
                for field, value in data["mag_stats"].items():
                    # st.number_input の値を更新するためにセッションステートに再代入
                    if f"mag_input_{field}" in st.session_state:
                         st.session_state[f"mag_input_{field}"] = value
                         
            # 加算ボーナスのインポート
            if "additive_atk_acc_bonus" in data:
                st.session_state['additive_atk_acc_bonus'] = data["additive_atk_acc_bonus"]
            if "additive_def_bonus" in data:
                st.session_state['additive_def_bonus'] = data["additive_def_bonus"]
                
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
            st.info("ここにスキル名とレベル入力（スライダーまたは数値入力）のUIが入り、そのスキル効果が上記の基本ステータスやダメージ計算に反映されます。")
else:
    st.warning("クラスが選択されていません。")
