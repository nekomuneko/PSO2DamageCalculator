import streamlit as st
import math

st.set_page_config(layout="wide")

# =================================================================
# 1. 補正データ定義
# =================================================================

# --- Lv100メインクラス補正済み基礎値 ---
WIKI_BASE_STATS = {
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

# --- 種族補正データ ---
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

# --- クラスブーストの固定値 ---
CLASS_BOOST_BONUS = {
    "HP": 60, "PP": 10, "打撃力": 120, "射撃力": 120, "法撃力": 120, "技量": 60, "打撃防御": 90, "射撃防御": 90, "法撃防御": 90
}

# =================================================================
# 2. スキルデータ定義 (統合)
# =================================================================

# クラス名 -> {スキル名: {"max_level": X, "description": "説明", "prereq": {"前提スキル名": 必須SP}}}
ALL_SKILL_DATA = {
    "Hu": {
        "フューリースタンス": {"max_level": 10, "description": "打撃力と射撃力を上昇。", "prereq": None},
        "フューリーSアップ": {"max_level": 10, "description": "フューリースタンス中の威力上昇効果をさらに強化。", "prereq": {"フューリースタンス": 1}},
        "オートメイトハーフ": {"max_level": 1, "description": "HPが半分以下になると自動でHP回復。", "prereq": None},
        "アイアンウィル": {"max_level": 1, "description": "戦闘不能になるダメージを受けてもHP1で耐える。", "prereq": None},
        "乙女の意地": {"max_level": 1, "description": "アイアンウィル発動時にPPを回復。", "prereq": {"アイアンウィル": 1}},
        "打撃力アップ": {"max_level": 10, "description": "打撃力を上昇させる。", "prereq": None},
        "PPアップ": {"max_level": 10, "description": "最大PPを上昇させる。", "prereq": None},
    },
    "Fi": {
        "リミットブレイク": {"max_level": 1, "description": "HPを犠牲に攻撃能力を大幅強化。", "prereq": None},
        "テックアーツJAボーナス": {"max_level": 10, "description": "異なるPA/テクニックを続けて使用すると威力上昇。", "prereq": None},
        "チェイスアドバンス": {"max_level": 10, "description": "状態異常のエネミーへのダメージ増加。", "prereq": None},
        "HPアップ": {"max_level": 10, "description": "最大HPを上昇させる。", "prereq": None},
        "PPスレイヤー": {"max_level": 10, "description": "PP量が少ないほど威力上昇。", "prereq": None},
    },
    "Ra": {
        "ウィークスタンス": {"max_level": 10, "description": "弱点部位へのダメージを増加。", "prereq": None},
        "ウィークSアップ": {"max_level": 10, "description": "ウィークスタンス中の効果をさらに強化。", "prereq": {"ウィークスタンス": 1}},
        "キリングボーナス": {"max_level": 5, "description": "エネミー撃破時にPPを回復。", "prereq": None},
        "射撃力アップ": {"max_level": 10, "description": "射撃力を上昇させる。", "prereq": None},
    },
    "Gu": {
        "SロールJAボーナス": {"max_level": 10, "description": "スタイリッシュロール後のJAで威力上昇。", "prereq": None},
        "パーフェクトキーパー": {"max_level": 10, "description": "HPが満タンに近いほど威力上昇。", "prereq": None},
        "PPハイアップ": {"max_level": 10, "description": "PP最大値を大幅に上昇。", "prereq": None},
    },
    "Fo": {
        "テックチャージアドバンス": {"max_level": 10, "description": "テクニックのチャージ時間を短縮。", "prereq": None},
        "法撃力アップ": {"max_level": 10, "description": "法撃力を上昇させる。", "prereq": None},
        "エレメントコンバージョン": {"max_level": 10, "description": "属性一致時のダメージを増加。", "prereq": None},
        "チャージPPリバイバル": {"max_level": 1, "description": "テクニックチャージ中にPP回復速度が上昇。", "prereq": None},
    },
    "Te": {
        "テリトリーバースト": {"max_level": 1, "description": "シフタ・デバンドの効果範囲拡大。", "prereq": None},
        "シフタ・デバンドアドバンス": {"max_level": 10, "description": "シフタ・デバンドの効果上昇。", "prereq": None},
        "エレメントウィークヒット": {"max_level": 10, "description": "弱点属性へのダメージを増加。", "prereq": None},
    },
    "Br": {
        "アベレージスタンス": {"max_level": 10, "description": "常に安定したダメージを与える。", "prereq": None},
        "カタナコンバット": {"max_level": 1, "description": "一定時間、攻撃速度と威力を強化。", "prereq": None},
    },
    "Bo": {
        "ブレイクスタンス": {"max_level": 10, "description": "部位破壊時や特定の部位へのダメージ増加。", "prereq": None},
        "フォトンブレードフィーバー": {"max_level": 1, "description": "一定時間、フォトンブレードを連続射出。", "prereq": None},
    },
    "Su": {
        "マッシブハンター": {"max_level": 1, "description": "スーパーアーマーとダメージ耐性を獲得。", "prereq": None},
        "パフェスタンス": {"max_level": 10, "description": "ペットの攻撃力上昇。", "prereq": None},
    },
    # 後継クラス
    "Hr": {
        "ヒーローウィル": {"max_level": 1, "description": "戦闘不能になるダメージを受けてもHP1で耐える。", "prereq": None},
        "ヒーローブースト": {"max_level": 10, "description": "連続して攻撃を当てると威力上昇。", "prereq": None},
        "ヒーロータイム": {"max_level": 1, "description": "一定時間、攻撃能力と機動力を大幅に強化。", "prereq": None},
    },
    "Ph": {
        "ファントムマーカー": {"max_level": 10, "description": "マーカーを付与し、爆発でダメージを与える。", "prereq": None},
        "ファントムタイム": {"max_level": 1, "description": "一定時間、攻撃能力を強化。", "prereq": None},
    },
    "Et": {
        "エトワールウィル": {"max_level": 1, "description": "戦闘不能になるダメージを受けてもHP1で耐える。", "prereq": None},
        "オールアタックボーナス": {"max_level": 10, "description": "全ての攻撃種別でダメージ上昇。", "prereq": None},
    },
    "Lu": {
        "ルミナスリフレクト": {"max_level": 1, "description": "自動でガードし、PPを回復。", "prereq": None},
        "ルミナスマスタリー": {"max_level": 10, "description": "全ての攻撃種別でダメージ上昇。", "prereq": None},
    },
}

# -------------------------------------------------------------------

# 定数
MAG_STATS_FIELDS = ["打撃力", "射撃力", "法撃力", "技量", "打撃防御", "射撃防御", "法撃防御"]
STATS_FIELDS = ["HP", "PP", "打撃力", "射撃力", "法撃力", "技量", "打撃防御", "射撃防御", "法撃防御"]
ALL_CLASSES = list(WIKI_BASE_STATS.keys())
UNAVAILABLE_SUBCLASSES = ["Hr", "Ph", "Et", "Lu"] # 後継クラスはサブクラスにできない
SUCCESSOR_MAIN_CLASSES = ["Hr", "Ph", "Et", "Lu"]

# --- 丸め関数定義 ---
def custom_floor(num):
    """攻撃力/技量, HP/PP最終結果, およびサブクラス貢献度 (攻撃力/技量) に使用する切り捨て (FLOOR)"""
    return math.floor(num)

def custom_round_half_up(num):
    """防御力に使用する四捨五入 (X.5で繰り上げ)"""
    return int(num + 0.5)

# --- セッションステートの初期化 (ステータス計算機 + スキルツリー) ---
if 'main_class_select' not in st.session_state: st.session_state['main_class_select'] = "Gu" 
if 'sub_class_select' not in st.session_state: st.session_state['sub_class_select'] = "Lu" 
if 'race_select' not in st.session_state: st.session_state['race_select'] = "キャスト女" 
if 'mag_stats' not in st.session_state: 
    st.session_state['mag_stats'] = {field: 200 if field == "射撃力" else 0 for field in MAG_STATS_FIELDS}
if 'class_boost_enabled' not in st.session_state: st.session_state['class_boost_enabled'] = True 

# --- スキルツリー関連のセッションステート ---
if 'all_sp_allocations' not in st.session_state:
    st.session_state['all_sp_allocations'] = {
        class_name: {skill: 0 for skill in skills.keys()}
        for class_name, skills in ALL_SKILL_DATA.items()
    }
# 利用可能SPは共通
if 'total_sp_available' not in st.session_state: st.session_state['total_sp_available'] = 70 

# =================================================================
# 3. 計算関数
# =================================================================

def get_calculated_stats():
    """
    HP: サブクラス貢献度(0.2倍)あり。
    PP: サブクラス貢献度なし。
    その他: 標準ロジック (サブクラス貢献度0.2倍、途中丸めあり)。
    """
    
    race = st.session_state['race_select']
    main_class = st.session_state['main_class_select']
    sub_class_select = st.session_state['sub_class_select']
    
    race_cor = RACE_CORRECTIONS.get(race, {})
    mag_stats = st.session_state['mag_stats']
    
    # クラスブーストボーナスを適用するかどうか
    CB_BONUS = CLASS_BOOST_BONUS if st.session_state['class_boost_enabled'] else {k: 0 for k in CLASS_BOOST_BONUS.keys()}
        
    calculated_stats = {}

    for stat_name in STATS_FIELDS:
        wiki_main_base_val = WIKI_BASE_STATS.get(main_class, {}).get(stat_name, 0)
        race_multiplier = race_cor.get(stat_name, 1.0)
        total_value = 0.0 # 浮動小数点計算用に初期化

        
        if stat_name == 'HP':
            # HP 計算ロジック
            main_contribution = wiki_main_base_val * race_multiplier
            total_value += main_contribution
            
            # サブクラス貢献度 (HPのみサブクラスもHPに貢献すると仮定し、0.2倍)
            if sub_class_select != 'None':
                wiki_sub_base_val = WIKI_BASE_STATS.get(sub_class_select, {}).get(stat_name, 0)
                sub_contribution = (wiki_sub_base_val * race_multiplier) * 0.2
                total_value += sub_contribution
            
            total_value += CB_BONUS.get(stat_name, 0)
            
            calculated_stats[stat_name] = custom_floor(total_value)
            
        elif stat_name == 'PP':
            # PP 計算ロジック (サブクラス不参照)
            main_contribution = wiki_main_base_val * race_multiplier
            total_value += main_contribution
            
            total_value += CB_BONUS.get(stat_name, 0)
            
            calculated_stats[stat_name] = custom_floor(total_value)
            
        else:
            # 攻撃力/防御力/技量 計算 (標準ロジック: 途中丸めあり)

            # 1. メインクラスによるステータス計算 (種族補正適用 + 途中丸め)
            if stat_name in ["打撃力", "射撃力", "法撃力", "技量"]:
                main_final_value = custom_floor(wiki_main_base_val * race_multiplier)
            elif stat_name in ["打撃防御", "射撃防御", "法撃防御"]:
                main_final_value = custom_round_half_up(wiki_main_base_val * race_multiplier)
                
            total_value = float(main_final_value)

            # 2. マグボーナス加算
            if stat_name in MAG_STATS_FIELDS:
                total_value += mag_stats.get(stat_name, 0)
            
            # 3. サブクラス貢献度計算 (攻撃力/防御力/技量はサブ貢献 20% + 途中丸め)
            if sub_class_select != 'None' and main_class not in SUCCESSOR_MAIN_CLASSES:
                wiki_sub_base_val = WIKI_BASE_STATS.get(sub_class_select, {}).get(stat_name, 0)

                # 3-1. サブクラスの種族補正適用 (切り捨て)
                sub_after_race = custom_floor(wiki_sub_base_val * race_multiplier)
                
                # 3-2. サブクラス貢献度 20% 適用 (切り捨て)
                sub_contribution = custom_floor(sub_after_race * 0.2)
                
                total_value += sub_contribution

            # 4. クラスブースト増加分 (固定値)
            total_value += CB_BONUS.get(stat_name, 0)
            
            calculated_stats[stat_name] = int(total_value)
            
    return calculated_stats

# =================================================================
# Streamlit UI
# =================================================================

st.title("📚 PSO2 総合シミュレーター")
st.markdown("このシミュレーターは、ステータス計算とスキルツリー配分を同時に行うことができます。")
st.markdown("---")

# =================================================================
# 1. クラス構成 (クラス / サブクラス)
# =================================================================

st.markdown("### 1. クラス構成 (ステータス・スキルツリー共通)")
col_main_class, col_sub_class = st.columns(2)

with col_main_class:
    st.selectbox(
        "メインクラス",
        options=ALL_CLASSES,
        key="main_class_select",
    )
    main_class = st.session_state['main_class_select']

with col_sub_class:
    if main_class in SUCCESSOR_MAIN_CLASSES:
        # 後継クラスの場合、サブクラスは選択不可
        st.selectbox(
            "サブクラス",
            options=["None"],
            index=0,
            key="sub_class_select",
            disabled=True,
        )
        if st.session_state.get('sub_class_select') != "None": st.session_state['sub_class_select'] = "None" 
        st.info(f"ℹ️ {main_class}は後継クラスのため、サブクラスはNone固定です。")
    else:
        # メインクラスと後継クラスを除くリスト
        sub_class_options_filtered = ["None"] + [c for c in ALL_CLASSES if c != main_class and c not in UNAVAILABLE_SUBCLASSES]
        st.selectbox(
            "サブクラス",
            options=sub_class_options_filtered,
            key="sub_class_select",
        )
        # Hrが誤って選択された場合の処理（保険）
        if st.session_state.get('sub_class_select') == "Hr":
            st.warning("Hrはサブクラスに設定できません。Noneに戻します。")
            st.session_state['sub_class_select'] = "None"
            # st.rerun() # UIがフリーズしないよう、リランは避ける

current_sub_class = st.session_state.get('sub_class_select', 'None')


st.markdown("---")

# =================================================================
# 2. 種族設定 & 3. マグ/ボーナス設定 (既存ロジック)
# =================================================================

# --- 2. 種族設定 ---
st.markdown("### 2. 種族設定")

RACE_OPTIONS = list(RACE_CORRECTIONS.keys())
st.selectbox(
    "種族",
    options=RACE_OPTIONS,
    key="race_select",
)

st.markdown("---")

# --- 3. マグ設定と各種ボーナス ---
st.markdown("### 3. マグ/ボーナス設定")

# --- マグの入力 ---
st.markdown("##### マグのステータス (合計 **200** まで)")
current_total_mag = sum(st.session_state['mag_stats'].values())
MAG_MAX_TOTAL = 200
st.caption(f"**合計値:** **`{current_total_mag} / {MAG_MAX_TOTAL}`**") # captionで文字を小さく

if current_total_mag > MAG_MAX_TOTAL:
    st.error(f"マグの合計値が上限の {MAG_MAX_TOTAL} を超えています！")
elif current_total_mag == MAG_MAX_TOTAL:
    st.success("マグの合計値が上限に達しました。", icon="✅")

# 3列に分けたマグ入力フィールド
mag_cols = st.columns(3) 
mag_fields_groups = [["打撃力", "射撃力", "法撃力"], ["打撃防御", "射撃防御", "法撃防御"], ["技量"]]

def update_mag_stats(field):
    st.session_state['mag_stats'][field] = st.session_state[f"mag_input_{field}"]

for col_idx, fields in enumerate(mag_fields_groups):
    with mag_cols[col_idx]:
        for field in fields:
            st.markdown(f"**{field}**", help=f"{field}のマグレベル")
            st.number_input(
                field,
                min_value=0,
                max_value=MAG_MAX_TOTAL, 
                key=f"mag_input_{field}",
                value=st.session_state['mag_stats'].get(field, 0),
                step=1,
                label_visibility="collapsed", # ラベルを非表示
                on_change=update_mag_stats,
                args=(field,)
            )

# --- クラスブースト設定 ---
st.markdown("##### 固定ボーナス")
st.checkbox(
    "クラスブースト（全クラスLv75達成）",
    key="class_boost_enabled",
    value=st.session_state['class_boost_enabled'],
    help="HP+60, PP+10, 攻撃力+120, 技量+60, 防御力+90が加算されます。"
)


st.markdown("---")

# =================================================================
# 4. 合計基本ステータス表示 (計算結果表示)
# =================================================================

# 補正込みの合計値を計算
total_stats = get_calculated_stats()

st.markdown("### 4. 合計基本ステータス")
st.markdown(f"現在の構成: **{main_class} / {current_sub_class}**")

# 計算ロジックのタイトルをさらに小さく
st.markdown("###### 適用されている基本ステータス計算ロジック")
st.markdown(r"**HP:** $\text{floor}((\text{メイン基礎値} \times \text{種族補正}) + (\text{サブ基礎値} \times \text{種族補正} \times \text{0.2}) + \text{クラスブースト})$")
st.markdown(r"**PP:** $\text{floor}((\text{メイン基礎値} \times \text{種族補正}) + \text{クラスブースト})$ **(サブクラス不参照)**")


# ステータス表示を整頓
stat_pairs = [
    ("HP", "PP"),      
    ("打撃力", "打撃防御"),
    ("射撃力", "射撃防御"),
    ("法撃力", "法撃防御"),
    ("技量", None)
]

for stat1_name, stat2_name in stat_pairs:
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label=f"**{stat1_name}**", value=f"{total_stats[stat1_name]}")
    
    if stat2_name:
        with col2:
            st.metric(label=f"**{stat2_name}**", value=f"{total_stats[stat2_name]}")

st.markdown("---")

# =================================================================
# 5. スキルツリーシミュレーター (新規統合)
# =================================================================

st.markdown("### 5. スキルツリーシミュレーター")
st.markdown("上記で設定したメイン/サブクラスのスキルツリーに、利用可能 $\text{SP}$ を割り振ります。")


# --- SP計算とサマリー ---

main_allocations = st.session_state['all_sp_allocations'].get(main_class, {})
sub_class_name_key = current_sub_class
sub_allocations = st.session_state['all_sp_allocations'].get(sub_class_name_key, {})


total_sp_spent = sum(main_allocations.values())
if sub_class_name_key != 'None':
    total_sp_spent += sum(sub_allocations.values()) # サブクラスのSPを加算

total_sp_available = st.session_state['total_sp_available']
remaining_sp = total_sp_available - total_sp_spent

col_sp_input, col_sp_summary, col_sp_remaining = st.columns(3)

with col_sp_input:
    st.number_input(
        "利用可能な合計SP",
        min_value=1,
        max_value=150, 
        value=total_sp_available,
        step=1,
        key='total_sp_available',
        label_visibility="visible"
    )

with col_sp_summary:
    st.metric(
        label="使用済み SP (合計)",
        value=f"{total_sp_spent} ポイント",
        delta_color="off" 
    )

with col_sp_remaining:
    delta_value = None
    delta_color = "off"
    if remaining_sp > 0:
        delta_value = f"残り {remaining_sp}"
        delta_color = "inverse"
    elif remaining_sp < 0:
        delta_value = f"超過 {abs(remaining_sp)}"
        delta_color = "normal" 

    st.metric(
        label="SP ステータス",
        value=f"{remaining_sp} ポイント",
        delta=delta_value,
        delta_color=delta_color 
    )

if remaining_sp < 0:
    st.error(f"合計SP ({total_sp_available}) を {abs(remaining_sp)} ポイント超過しています！")
elif remaining_sp == 0:
    st.success("スキルポイントを使い切りました！")


st.markdown("---")

# --- スキル入力のロジック ---
def update_allocation(class_name, skill_name):
    # キーにクラス名とスキル名を含めることで、どのインプットが変更されたかを正確に特定
    input_key = f"level_input_{class_name}_{skill_name}"
    # 選択されたクラスの割り当てを更新
    if class_name in st.session_state['all_sp_allocations']:
        st.session_state['all_sp_allocations'][class_name][skill_name] = st.session_state[input_key]


# --- スキルツリー描画関数 ---
def render_skill_tree(class_name, allocations):
    current_skills = ALL_SKILL_DATA.get(class_name, {})
    if not current_skills:
        st.info("このクラスのスキルデータは現在準備されていません。")
        return

    # スキルを2列に分けて表示
    skill_cols = st.columns(2)
    skill_names = list(current_skills.keys())
    half_point = (len(skill_names) + 1) // 2

    for i, skill_name in enumerate(skill_names):
        skill_info = current_skills[skill_name]
        
        col = skill_cols[0] if i < half_point else skill_cols[1]
        
        with col:
            max_lvl = skill_info['max_level']
            current_lvl = allocations.get(skill_name, 0)
            
            # スキル名と説明をコンパクトに表示
            st.markdown(f"**{skill_name}** (Max Lvl: {max_lvl})")
            st.caption(f"*{skill_info['description']}*")

            # ナンバーインプットを使用。キーにクラス名とスキル名を追加
            st.number_input(
                "Lv",
                min_value=0,
                max_value=max_lvl,
                value=current_lvl,
                step=1,
                key=f"level_input_{class_name}_{skill_name}",
                label_visibility="collapsed", 
                on_change=update_allocation,
                args=(class_name, skill_name,)
            )
            st.markdown("---")


# --- タブ表示 ---

# メインクラスのタブ名
main_tab_title = f"メイン: {main_class} ({sum(main_allocations.values())} SP)"

# サブクラスのタブ名と条件
sub_tab_enabled = sub_class_name_key != 'None'
sub_tab_title = f"サブ: {sub_class_name_key} ({sum(sub_allocations.values())} SP)" if sub_tab_enabled else "サブクラス (None)"


tab_main, tab_sub = st.tabs([main_tab_title, sub_tab_title])

# --- メインクラスのタブ内容 ---
with tab_main:
    st.markdown(f"#### {main_class} スキルポイント配分")
    render_skill_tree(main_class, main_allocations)

# --- サブクラスのタブ内容 ---
with tab_sub:
    if sub_tab_enabled:
        st.markdown(f"#### {sub_class_name_key} スキルポイント配分")
        render_skill_tree(sub_class_name_key, sub_allocations)
    else:
        st.info("サブクラスが設定されていないため、スキルツリーは表示されません。")


# --- リセットボタン ---
def reset_sp():
    main_class_name = st.session_state['main_class_select']
    sub_class_name = st.session_state.get('sub_class_select')

    # メインクラスのリセット
    if main_class_name in st.session_state['all_sp_allocations']:
        st.session_state['all_sp_allocations'][main_class_name] = {
            skill: 0 for skill in ALL_SKILL_DATA.get(main_class_name, {}).keys()
        }
    
    # サブクラスがNoneでない場合、サブクラスもリセット
    if sub_class_name and sub_class_name != 'None' and sub_class_name in st.session_state['all_sp_allocations']:
        st.session_state['all_sp_allocations'][sub_class_name] = {
            skill: 0 for skill in ALL_SKILL_DATA.get(sub_class_name, {}).keys()
        }
    
    # 利用可能SPはデフォルト値に戻す
    st.session_state['total_sp_available'] = 70 

st.button(f"🔄 現在の構成 ({main_class}/{current_sub_class}) のSPを全てリセット", on_click=reset_sp)
