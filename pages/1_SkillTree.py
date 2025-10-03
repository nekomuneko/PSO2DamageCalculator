import streamlit as st
import math

st.set_page_config(layout="wide")

# =================================================================
# 1. 補正データ定義 & 定数
# =================================================================

# --- Lv100メインクラス補正済み基礎値 (データは変更なし) ---
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
# 2. スキルデータ定義 (省略なし)
# =================================================================

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

# 定数と初期化
MAG_STATS_FIELDS = ["打撃力", "射撃力", "法撃力", "技量", "打撃防御", "射撃防御", "法撃防御"]
STATS_FIELDS = ["HP", "PP", "打撃力", "射撃力", "法撃力", "技量", "打撃防御", "射撃防御", "法撃防御"]
ALL_CLASSES = list(WIKI_BASE_STATS.keys())
# Hrはサブクラスに設定できない (ゲーム仕様に基づき修正)
UNAVAILABLE_SUBCLASSES = ["Hr"] 
# 後継クラスがメインクラスの場合、サブクラスはNoneに固定される (ゲーム仕様)
SUCCESSOR_MAIN_CLASSES = ["Hr", "Ph", "Et", "Lu"] 

# ユーザー要望によりSPは114で固定
FIXED_SP_PER_CLASS = 114

# --- 丸め関数定義 (変更なし) ---
def custom_floor(num):
    """攻撃力/技量, HP/PP最終結果, およびサブクラス貢献度 (攻撃力/技量) に使用する切り捨て (FLOOR)"""
    return math.floor(num)

def custom_round_half_up(num):
    """防御力に使用する四捨五入 (X.5で繰り上げ)"""
    return int(num + 0.5)

# --- セッションステートの初期化 ---
if 'main_class_select' not in st.session_state: st.session_state['main_class_select'] = "Gu" 
if 'sub_class_select' not in st.session_state: st.session_state['sub_class_select'] = "Ph" # デフォルトをPhに変更
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

# =================================================================
# 3. 計算関数
# =================================================================

def update_mag_stats(field):
    """マグのステータス入力値をセッションステートに反映する関数"""
    # この関数はマグ設定のnumber_inputのon_changeに必要
    st.session_state['mag_stats'][field] = st.session_state[f"mag_input_{field}"]

def get_calculated_stats():
    """ステータス計算ロジック"""
    
    race = st.session_state['race_select']
    main_class = st.session_state['main_class_select']
    sub_class_select = st.session_state['sub_class_select']
    
    race_cor = RACE_CORRECTIONS.get(race, {})
    mag_stats = st.session_state['mag_stats']
    
    CB_BONUS = CLASS_BOOST_BONUS if st.session_state['class_boost_enabled'] else {k: 0 for k in CLASS_BOOST_BONUS.keys()}
        
    calculated_stats = {}

    for stat_name in STATS_FIELDS:
        wiki_main_base_val = WIKI_BASE_STATS.get(main_class, {}).get(stat_name, 0)
        race_multiplier = race_cor.get(stat_name, 1.0)
        total_value = 0.0

        
        if stat_name == 'HP':
            main_contribution = wiki_main_base_val * race_multiplier
            total_value += main_contribution
            
            # HPのサブクラス貢献度 (20%) はメインクラスの種別に関わらず適用される
            if sub_class_select != 'None':
                wiki_sub_base_val = WIKI_BASE_STATS.get(sub_class_select, {}).get(stat_name, 0)
                sub_contribution = (wiki_sub_base_val * race_multiplier) * 0.2
                total_value += sub_contribution
            
            total_value += CB_BONUS.get(stat_name, 0)
            calculated_stats[stat_name] = custom_floor(total_value)
            
        elif stat_name == 'PP':
            main_contribution = wiki_main_base_val * race_multiplier
            total_value += main_contribution
            
            # PPはサブクラスの影響を受けない
            total_value += CB_BONUS.get(stat_name, 0)
            calculated_stats[stat_name] = custom_floor(total_value)
            
        else:
            # 攻撃力・技量・防御力
            if stat_name in ["打撃力", "射撃力", "法撃力", "技量"]:
                main_final_value = custom_floor(wiki_main_base_val * race_multiplier)
            elif stat_name in ["打撃防御", "射撃防御", "法撃防御"]:
                main_final_value = custom_round_half_up(wiki_main_base_val * race_multiplier)
                
            total_value = float(main_final_value)

            if stat_name in MAG_STATS_FIELDS:
                total_value += mag_stats.get(stat_name, 0)
            
            # 攻撃力/防御力/技量のサブクラス貢献度 (20%) はメインクラスが後継クラスの場合は適用されない
            if sub_class_select != 'None' and main_class not in SUCCESSOR_MAIN_CLASSES:
                wiki_sub_base_val = WIKI_BASE_STATS.get(sub_class_select, {}).get(stat_name, 0)

                # サブクラスの基礎値を種族補正し、20%切り捨て
                if stat_name in ["打撃力", "射撃力", "法撃力", "技量"]:
                     sub_after_race = custom_floor(wiki_sub_base_val * race_multiplier)
                else: # 防御力
                     sub_after_race = custom_round_half_up(wiki_sub_base_val * race_multiplier)
                
                sub_contribution = custom_floor(sub_after_race * 0.2)
                
                total_value += sub_contribution

            total_value += CB_BONUS.get(stat_name, 0)
            
            calculated_stats[stat_name] = int(total_value)
            
    return calculated_stats

# --- スキル入力のロジック (変更なし) ---
def update_allocation(class_name, skill_name):
    """SP割り当てを更新する関数"""
    input_key = f"level_input_{class_name}_{skill_name}"
    if class_name in st.session_state['all_sp_allocations']:
        st.session_state['all_sp_allocations'][class_name][skill_name] = st.session_state[input_key]

# --- スキルツリー描画関数 (変更なし) ---
def render_skill_tree(class_name, allocations):
    """指定されたクラスのスキルツリーを描画する関数"""
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
            
            st.markdown(f"**{skill_name}** (Max Lvl: {max_lvl})")
            st.caption(f"*{skill_info['description']}*")

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

# --- リセット関数 (SP固定値114に対応) ---
def reset_sp():
    """メインクラスとサブクラスのSP割り当てをリセットする関数"""
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
    
# =================================================================
# Streamlit UI
# =================================================================

st.title("📚 PSO2 総合シミュレーター")
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
        # メインクラスが後継クラスの場合、サブクラスは選択不可 (ゲーム仕様)
        st.selectbox(
            "サブクラス",
            options=["None"],
            index=0,
            key="sub_class_select",
            disabled=True,
        )
        # 内部状態を確実に 'None' に設定
        if st.session_state.get('sub_class_select') != "None": st.session_state['sub_class_select'] = "None" 
        st.error(f"⚠️ {main_class}は後継クラスのため、サブクラスはNone固定です。")
    else:
        # メインクラスとHrを除くリスト
        sub_class_options_filtered = ["None"] + [c for c in ALL_CLASSES if c != main_class and c not in UNAVAILABLE_SUBCLASSES]
        st.selectbox(
            "サブクラス",
            options=sub_class_options_filtered,
            key="sub_class_select",
        )
        
current_sub_class = st.session_state.get('sub_class_select', 'None')
if current_sub_class != 'None' and current_sub_class in UNAVAILABLE_SUBCLASSES:
    # 選択肢から除外されるが、万が一のためにエラー表示 (今回はHrのみ)
    st.error(f"後継クラスの {current_sub_class} はサブクラスに設定できません。")


st.markdown("---")

# =================================================================
# 2. 種族設定 & 3. マグ/ボーナス設定
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
st.caption(f"**合計値:** **`{current_total_mag} / {MAG_MAX_TOTAL}`**")

if current_total_mag > MAG_MAX_TOTAL:
    st.error(f"マグの合計値が上限の {MAG_MAX_TOTAL} を超えています！")
elif current_total_mag == MAG_MAX_TOTAL:
    st.success("マグの合計値が上限に達しました。", icon="✅")

mag_cols = st.columns(3) 
mag_fields_groups = [["打撃力", "射撃力", "法撃力"], ["打撃防御", "射撃防御", "法撃防御"], ["技量"]]

for col_idx, fields in enumerate(mag_fields_groups):
    with mag_cols[col_idx]:
        for field in fields:
            # マグのステータスは、対応するフィールドにしか振れないため、最大値を200に設定
            max_val = MAG_MAX_TOTAL if field in ["打撃力", "射撃力", "法撃力", "技量"] else 0 # 攻撃系ステータスにのみ振れる仕様を反映
            
            st.markdown(f"**{field}**", help=f"{field}のマグレベル")
            st.number_input(
                field,
                min_value=0,
                max_value=max_val, 
                key=f"mag_input_{field}",
                value=st.session_state['mag_stats'].get(field, 0),
                step=1,
                label_visibility="collapsed",
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

total_stats = get_calculated_stats()

st.markdown("### 4. 合計基本ステータス")
st.markdown(f"現在の構成: **{main_class} / {current_sub_class}**")

st.markdown("###### 適用されている基本ステータス計算ロジック")
st.markdown(r"**HP:** $\text{floor}((\text{メイン基礎値} \times \text{種族補正}) + (\text{サブ基礎値} \times \text{種族補正} \times \text{0.2}) + \text{クラスブースト})$")
st.markdown(r"**PP:** $\text{floor}((\text{メイン基礎値} \times \text{種族補正}) + \text{クラスブースト})$ **(サブクラス不参照)**")


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
# 5. スキルツリーシミュレーター (SP分離・固定化に伴い修正)
# =================================================================

st.markdown("### 5. スキルツリーシミュレーター")
st.markdown("各クラスのスキルポイントは**114ポイントで固定**されています。")

# --- SP計算とサマリー (メインとサブを分離) ---

main_allocations = st.session_state['all_sp_allocations'].get(main_class, {})
sub_class_name_key = current_sub_class
sub_allocations = st.session_state['all_sp_allocations'].get(sub_class_name_key, {})

# メインクラスSP
main_sp_spent = sum(main_allocations.values())
main_sp_remaining = FIXED_SP_PER_CLASS - main_sp_spent

# サブクラスSP
sub_sp_spent = sum(sub_allocations.values()) if sub_class_name_key != 'None' else 0
sub_sp_remaining = FIXED_SP_PER_CLASS - sub_sp_spent if sub_class_name_key != 'None' else 0

col_main_sp, col_sub_sp = st.columns(2)

with col_main_sp:
    st.markdown(f"#### メインクラス SP (合計: {FIXED_SP_PER_CLASS})")
    st.metric(
        label=f"**{main_class}** 使用済み / 残り SP",
        value=f"{main_sp_spent} / {main_sp_remaining}",
        delta=f"残り {main_sp_remaining}" if main_sp_remaining >= 0 else f"超過 {abs(main_sp_remaining)}",
        delta_color="inverse" if main_sp_remaining >= 0 else "normal"
    )
    if main_sp_remaining < 0:
        st.error(f"メインSPが {abs(main_sp_remaining)} ポイント超過しています！")


with col_sub_sp:
    if sub_class_name_key != 'None':
        st.markdown(f"#### サブクラス SP (合計: {FIXED_SP_PER_CLASS})")
        st.metric(
            label=f"**{sub_class_name_key}** 使用済み / 残り SP",
            value=f"{sub_sp_spent} / {sub_sp_remaining}",
            delta=f"残り {sub_sp_remaining}" if sub_sp_remaining >= 0 else f"超過 {abs(sub_sp_remaining)}",
            delta_color="inverse" if sub_sp_remaining >= 0 else "normal"
        )
        if sub_sp_remaining < 0:
            st.error(f"サブSPが {abs(sub_sp_remaining)} ポイント超過しています！")
    else:
        st.markdown("#### サブクラス SP")
        st.info("サブクラスが設定されていません。")

st.markdown("---")

# --- タブ表示 (タブ名に残SPを表示) ---

main_tab_title = f"メイン: {main_class} (残 {main_sp_remaining})"
sub_tab_title = f"サブ: {sub_class_name_key} (残 {sub_sp_remaining})" if current_sub_class != 'None' else "サブクラス (None)"


tab_main, tab_sub = st.tabs([main_tab_title, sub_tab_title])

# --- メインクラスのタブ内容 ---
with tab_main:
    st.markdown(f"#### {main_class} スキルポイント配分")
    render_skill_tree(main_class, main_allocations)

# --- サブクラスのタブ内容 ---
with tab_sub:
    if sub_class_name_key != 'None':
        st.markdown(f"#### {sub_class_name_key} スキルポイント配分")
        render_skill_tree(sub_class_name_key, sub_allocations)
    else:
        st.info("サブクラスがNoneのため、スキルツリーは表示されません。")


# --- リセットボタン ---
st.button(f"🔄 現在の構成 ({main_class}/{current_sub_class}) のSPを全てリセット", on_click=reset_sp)
