import streamlit as st
import math

st.set_page_config(layout="wide")

# =================================================================
# 1. 補正データ定義（ステータス計算用）
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
    "キャスト男":  {"HP": 1.07, "PP": 1.00, "打撃力": 1.05, "射撃力": 1.04, "法撃力": 0.96, "技量": 1.07, "打撃防御": 1.05, "射撃防御": 1.00, "法撃防御": 0.95},
    "キャスト女":  {"HP": 1.06, "PP": 1.00, "打撃力": 1.04, "射撃力": 1.05, "法撃力": 0.96, "技量": 1.07, "打撃防御": 1.00, "射撃防御": 1.05, "法撃防御": 0.95},
    "デューマン男": {"HP": 0.96, "PP": 1.00, "打撃力": 1.07, "射撃力": 1.04, "法撃力": 1.05, "技量": 1.05, "打撃防御": 1.00, "射撃防御": 1.00, "法撃防御": 1.00},
    "デューマン女": {"HP": 0.95, "PP": 1.00, "打撃力": 1.06, "射撃力": 1.05, "法撃力": 1.05, "技量": 1.06, "打撃防御": 1.00, "射撃防御": 1.00, "法撃防御": 1.00},
}

# --- クラスブーストの固定値 ---
CLASS_BOOST_BONUS = {
    "HP": 60, "PP": 10, "打撃力": 120, "射撃力": 120, "法撃力": 120, "技量": 60, "打撃防御": 90, "射撃防御": 90, "法撃防御": 90
}
# -------------------------------------------------------------------

# =================================================================
# 2. スキルデータ定義（スキルツリー用）
# =================================================================

# --- HPアップ系スキルボーナス値の定義 ---
# レベルをキー、ボーナスHPを値とする
HP_UP_BONUSES = {
    "HPアップ 1": {1: 3, 2: 6, 3: 10, 4: 14, 5: 18, 6: 23, 7: 28, 8: 34, 9: 40, 10: 50},
    "HPアップ 2": {1: 4, 2: 9, 3: 14, 4: 19, 5: 25, 6: 31, 7: 39, 8: 50, 9: 62, 10: 75}, # Hu 限定
    "HPアップ 3": {1: 5, 2: 11, 3: 18, 4: 26, 5: 35, 6: 45, 7: 56, 8: 68, 9: 81, 10: 100}, # Hu 限定
    "HPアップ (Su)": {1: 20, 2: 25, 3: 30, 4: 35, 5: 50}, # Su 限定
    "HPハイアップ": {1: 20, 2: 25, 3: 30, 4: 35, 5: 50, 6: 60, 7: 70, 8: 80, 9: 90, 10: 100}, # Su 限定
    # 【NEW】後継クラス (Hr/Ph/Et/Lu) 共通のHPアップボーナス
    "HPアップ (後継)": {1: 5, 2: 10, 3: 15, 4: 20, 5: 25, 6: 30, 7: 35, 8: 40, 9: 45, 10: 50}, 
}

# クラス名 -> {スキル名: {"max_level": X, "description": "説明", "prereq": {"前提スキル名": 必須SP}}}
ALL_SKILL_DATA = {
    "Hu": {
        "フューリースタンス": {"max_level": 10, "description": "打撃力と射撃力を上昇。", "prereq": None},
        "フューリーSアップ": {"max_level": 10, "description": "フューリースタンス中の威力上昇効果をさらに強化。", "prereq": {"フューリースタンス": 1}},
        "オートメイトハーフ": {"max_level": 1, "description": "HPが半分以下になると自動でHP回復。", "prereq": None},
        "アイアンウィル": {"max_level": 1, "description": "戦闘不能になるダメージを受けてもHP1で耐える。", "prereq": None},
        "乙女の意地": {"max_level": 1, "description": "アイアンウィル発動時にPPを回復。", "prereq": {"アイアンウィル": 1}},
        "ウォーブレイカー": {"max_level": 5, "description": "敵のガードを崩しやすくする。", "prereq": None},
        "打撃力アップ": {"max_level": 10, "description": "打撃力を上昇させる。", "prereq": None},
        "PPアップ": {"max_level": 10, "description": "最大PPを上昇させる。", "prereq": None},
        "HPアップ 1": {"max_level": 10, "description": "最大HPを上昇させる (HPアップ 1のボーナス)。", "prereq": None},
        "HPアップ 2": {"max_level": 10, "description": "最大HPを上昇させる (Hu限定のHPアップ 2のボーナス)。", "prereq": None},
        "HPアップ 3": {"max_level": 10, "description": "最大HPを上昇させる (Hu限定のHPアップ 3のボーナス)。", "prereq": None}, 
    },
    "Fi": {
        "リミットブレイク": {"max_level": 1, "description": "HPを犠牲に攻撃能力を大幅強化。", "prereq": None},
        "テックアーツJAボーナス": {"max_level": 10, "description": "異なるPA/テクニックを続けて使用すると威力上昇。", "prereq": None},
        "チェイスアドバンス": {"max_level": 10, "description": "状態異常のエネミーへのダメージ増加。", "prereq": None},
        "HPアップ 1": {"max_level": 10, "description": "最大HPを上昇させる (HPアップ 1のボーナス)。", "prereq": None},
        "HPアップ 1（2）": {"max_level": 10, "description": "最大HPを上昇させる (HPアップ 1と同一の効果)。", "prereq": None}, 
        "PPスレイヤー": {"max_level": 10, "description": "PP量が少ないほど威力上昇。", "prereq": None},
    },
    "Ra": {
        "ウィークスタンス": {"max_level": 10, "description": "弱点部位へのダメージを増加。", "prereq": None},
        "ウィークSアップ": {"max_level": 10, "description": "ウィークスタンス中の効果をさらに強化。", "prereq": {"ウィークスタンス": 1}},
        "スタンディングSチャージ": {"max_level": 1, "description": "静止中にチャージ時間が短縮。", "prereq": None},
        "キリングボーナス": {"max_level": 5, "description": "エネミー撃破時にPPを回復。", "prereq": None},
        "射撃力アップ": {"max_level": 10, "description": "射撃力を上昇させる。", "prereq": None},
        "トラップサーチ": {"max_level": 1, "description": "トラップの場所をミニマップに表示。", "prereq": None},
    },
    "Gu": {
        "SロールJAボーナス": {"max_level": 10, "description": "スタイリッシュロール後のJAで威力上昇。", "prereq": None},
        "TマシンガンアーツSチャージ": {"max_level": 1, "description": "Tマシンガンのチャージ時間が短縮。", "prereq": None},
        "アタックPPリカバリー": {"max_level": 10, "description": "通常攻撃のPP回復量を上昇。", "prereq": None},
        "パーフェクトキーパー": {"max_level": 10, "description": "HPが満タンに近いほど威力上昇。", "prereq": None},
        "PPハイアップ": {"max_level": 10, "description": "PP最大値を大幅に上昇。", "prereq": None},
        "HPアップ 1": {"max_level": 10, "description": "最大HPを上昇させる (HPアップ 1のボーナス)。", "prereq": None},
    },
    "Fo": {
        "テックチャージアドバンス": {"max_level": 10, "description": "テクニックのチャージ時間を短縮。", "prereq": None},
        "ロッドシュート": {"max_level": 5, "description": "ロッドでの通常攻撃が長射程になる。", "prereq": None},
        "法撃力アップ": {"max_level": 10, "description": "法撃力を上昇させる。", "prereq": None},
        "エレメントコンバージョン": {"max_level": 10, "description": "属性一致時のダメージを増加。", "prereq": None},
        "チャージPPリバイバル": {"max_level": 1, "description": "テクニックチャージ中にPP回復速度が上昇。", "prereq": None},
        "HPアップ 1": {"max_level": 10, "description": "最大HPを上昇させる (HPアップ 1のボーナス)。", "prereq": None},
    },
    "Te": {
        "テリトリーバースト": {"max_level": 1, "description": "シフタ・デバンドの効果範囲拡大。", "prereq": None},
        "シフタ・デバンドアドバンス": {"max_level": 10, "description": "シフタ・デバンドの効果上昇。", "prereq": None},
        "エレメントウィークヒット": {"max_level": 10, "description": "弱点属性へのダメージを増加。", "prereq": None},
        "ライトマスタリー": {"max_level": 10, "description": "光属性テクニックの威力上昇。", "prereq": None},
        "ウィンドマスタリー": {"max_level": 10, "description": "風属性テクニックの威力上昇。", "prereq": None},
    },
    "Br": {
        "アベレージスタンス": {"max_level": 10, "description": "常に安定したダメージを与える。", "prereq": None},
        "カタナコンバット": {"max_level": 1, "description": "一定時間、攻撃速度と威力を強化。", "prereq": None},
        "バレットボウチャージボーナス": {"max_level": 1, "description": "バレットボウのチャージ攻撃の威力上昇。", "prereq": None},
    },
    "Bo": {
        "ブレードディスラプター": {"max_level": 10, "description": "ジェットブーツのPAが連続ヒットするように。", "prereq": None},
        "ブレイクスタンス": {"max_level": 10, "description": "部位破壊時や特定の部位へのダメージ増加。", "prereq": None},
        "フォトンブレードフィーバー": {"max_level": 1, "description": "一定時間、フォトンブレードを連続射出。", "prereq": None},
    },
    "Su": {
        "マッシブハンター": {"max_level": 1, "description": "スーパーアーマーとダメージ耐性を獲得。", "prereq": None},
        "シフタライド": {"max_level": 10, "description": "シフタライド後の威力上昇。", "prereq": None},
        "パフェスタンス": {"max_level": 10, "description": "ペットの攻撃力上昇。", "prereq": None},
        "HPアップ (Su)": {"max_level": 5, "description": "最大HPを上昇させる (Su専用のHPアップボーナス)。", "prereq": None}, 
        "HPハイアップ": {"max_level": 10, "description": "最大HPを大きく上昇させる。", "prereq": None}, # <- Lv10まで反映済み
    },
    # 後継クラス (サブクラス不可)
    "Hr": {
        "ヒーローウィル": {"max_level": 1, "description": "戦闘不能になるダメージを受けてもHP1で耐える。", "prereq": None},
        "ヒーローブースト": {"max_level": 10, "description": "連続して攻撃を当てると威力上昇。", "prereq": None},
        "ヒーロータイム": {"max_level": 1, "description": "一定時間、攻撃能力と機動力を大幅に強化。", "prereq": None},
        "HPアップ (後継)": {"max_level": 10, "description": "最大HPを上昇させる (後継クラス専用ボーナス)。", "prereq": None}, # <- NEW
    },
    "Ph": {
        "ファントムPPメイトリバイブ": {"max_level": 1, "description": "PPメイト使用時にHPも回復。", "prereq": None},
        "ファントムマーカー": {"max_level": 10, "description": "マーカーを付与し、爆発でダメージを与える。", "prereq": None},
        "ファントムタイム": {"max_level": 1, "description": "一定時間、攻撃能力を強化。", "prereq": None},
        "HPアップ (後継)": {"max_level": 10, "description": "最大HPを上昇させる (後継クラス専用ボーナス)。", "prereq": None}, # <- NEW
    },
    "Et": {
        "エトワールウィル": {"max_level": 1, "description": "戦闘不能になるダメージを受けてもHP1で耐える。", "prereq": None},
        "オールアタックボーナス": {"max_level": 10, "description": "全ての攻撃種別でダメージ上昇。", "prereq": None},
        "エトワールブースト": {"max_level": 1, "description": "状態異常を無効化し、被ダメージを軽減。", "prereq": None},
        "HPアップ (後継)": {"max_level": 10, "description": "最大HPを上昇させる (後継クラス専用ボーナス)。", "prereq": None}, # <- NEW
    },
    "Lu": {
        "ルミナスリフレクト": {"max_level": 1, "description": "自動でガードし、PPを回復。", "prereq": None},
        "ルミナスマスタリー": {"max_level": 10, "description": "全ての攻撃種別でダメージ上昇。", "prereq": None},
        "ライトニングスピア": {"max_level": 1, "description": "範囲内の敵にダメージを与え、PPを回復。", "prereq": None},
        "HPアップ (後継)": {"max_level": 10, "description": "最大HPを上昇させる (後継クラス専用ボーナス)。", "prereq": None}, # <- NEW
    },
}

# =================================================================
# 3. 定数と初期化
# =================================================================

MAG_STATS_FIELDS = ["打撃力", "射撃力", "法撃力", "技量", "打撃防御", "射撃防御", "法撃防御"]
STATS_FIELDS = ["HP", "PP", "打撃力", "射撃力", "法撃力", "技量", "打撃防御", "射撃防御", "法撃防御"]
ALL_CLASSES = list(WIKI_BASE_STATS.keys())
UNAVAILABLE_SUBCLASSES = ["Hr", "Ph", "Et", "Lu"] # 後継クラスはサブクラス不可
SUCCESSOR_MAIN_CLASSES = ["Hr", "Ph", "Et", "Lu"]

# --- 丸め関数定義 ---
def custom_floor(num):
    """攻撃力/技量, HP/PP最終結果, およびサブクラス貢献度 (攻撃力/技量) に使用する切り捨て (FLOOR)"""
    return math.floor(num)

def custom_round_half_up(num):
    """防御力に使用する四捨五入 (X.5で繰り上げ)"""
    return int(num + 0.5)

# --- セッションステートの初期化 ---
if 'main_class_select' not in st.session_state: st.session_state['main_class_select'] = "Gu" 
if 'sub_class_select' not in st.session_state: st.session_state['sub_class_select'] = "Fi" 
if 'race_select' not in st.session_state: st.session_state['race_select'] = "キャスト女" 
if 'mag_stats' not in st.session_state: 
    st.session_state['mag_stats'] = {field: 200 if field == "射撃力" else 0 for field in MAG_STATS_FIELDS}
if 'class_boost_enabled' not in st.session_state: st.session_state['class_boost_enabled'] = True 

# スキルツリー関連の初期化
if 'all_sp_allocations' not in st.session_state:
    st.session_state['all_sp_allocations'] = {
        class_name: {skill: 0 for skill in skills.keys()}
        for class_name, skills in ALL_SKILL_DATA.items()
    }
# 利用可能SPは共通
if 'total_sp_available' not in st.session_state:
    st.session_state['total_sp_available'] = 70 

# =================================================================
# 4. 計算関数（ステータス計算用）
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

    # スキルによるHPボーナスを計算する汎用ロジック
    total_skill_hp_bonus = 0

    def get_skill_hp_bonus(class_name, allocations):
        bonus = 0
        for skill_name, level in allocations.items():
            if level > 0:
                # HPボーナスを持つスキルのキー名を決定
                key_name = None
                if skill_name in ["HPアップ 2", "HPアップ 3", "HPアップ (Su)", "HPハイアップ", "HPアップ (後継)"]: # <-- 後継クラスのスキルを追加
                    key_name = skill_name
                elif skill_name in ["HPアップ 1", "HPアップ 1（2）"]:
                    key_name = "HPアップ 1"

                if key_name and key_name in HP_UP_BONUSES:
                    # レベルに対応するボーナス値を取得 (ボーナス値が未定義の場合は0を返す)
                    bonus_map = HP_UP_BONUSES.get(key_name, {})
                    bonus += bonus_map.get(level, 0)
        return bonus

    # メインクラスとサブクラスのHPスキルボーナスを加算
    main_allocations = st.session_state['all_sp_allocations'].get(main_class, {})
    total_skill_hp_bonus += get_skill_hp_bonus(main_class, main_allocations)

    sub_class_name_key = st.session_state.get('sub_class_select', 'None')
    if sub_class_name_key != 'None':
        sub_allocations = st.session_state['all_sp_allocations'].get(sub_class_name_key, {})
        # Note: 実際にはHPアップ系スキルはメインクラス限定が多いが、シミュレーターとしてはサブクラスのスキルも計算対象に含める
        total_skill_hp_bonus += get_skill_hp_bonus(sub_class_name_key, sub_allocations)
    
    
    for stat_name in STATS_FIELDS:
        wiki_main_base_val = WIKI_BASE_STATS.get(main_class, {}).get(stat_name, 0)
        race_multiplier = race_cor.get(stat_name, 1.0)
        total_value = 0.0 # 浮動小数点計算用に初期化

        
        if stat_name == 'HP':
            # -----------------------------------------------------
            # HP 計算ロジック: floor((Main * Race) + (Sub * Race * 0.2) + CB) + Skill_Bonus
            # -----------------------------------------------------

            # 1. メインクラス貢献度 (丸め処理なし)
            main_contribution = wiki_main_base_val * race_multiplier
            total_value += main_contribution
            
            # 2. サブクラス貢献度 (HPのみサブクラスもHPに貢献すると仮定し、0.2倍)
            if sub_class_select != 'None':
                wiki_sub_base_val = WIKI_BASE_STATS.get(sub_class_select, {}).get(stat_name, 0)
                sub_contribution = (wiki_sub_base_val * race_multiplier) * 0.2
                total_value += sub_contribution
            
            # 3. クラスブースト固定値
            total_value += CB_BONUS.get(stat_name, 0)
            
            # 4. スキルボーナス加算 (切り捨て前)
            total_value += total_skill_hp_bonus
            
            # 5. 最終結果を切り捨て (floor)
            calculated_stats[stat_name] = custom_floor(total_value)
            
        elif stat_name == 'PP':
            # -----------------------------------------------------
            # PP 計算ロジック: floor((Main * Race) + CB) (サブクラス不参照)
            # -----------------------------------------------------
            
            # 1. メインクラス貢献度 (丸め処理なし)
            main_contribution = wiki_main_base_val * race_multiplier
            total_value += main_contribution
            
            # 2. クラスブースト固定値
            total_value += CB_BONUS.get(stat_name, 0)
            
            # 3. 最終結果を切り捨て (floor)
            calculated_stats[stat_name] = custom_floor(total_value)
            
        else:
            # -----------------------------------------------------
            # 攻撃力/防御力/技量 計算 (標準ロジック: 途中丸めあり)
            # -----------------------------------------------------

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
# 5. Streamlit UI (統合)
# =================================================================

# -----------------------------------------------------------------
# 5-1. ステータス計算機 UI (ユーザー提供コードをベース)
# -----------------------------------------------------------------

st.title("📚 PSO2 統合シミュレーター")
st.markdown("---")
st.header("1. ステータス計算機")


# --- A. クラス構成 ---
st.markdown("### クラス構成")
col_main_class, col_sub_class = st.columns(2)

main_class_select_key = 'main_class_select'
sub_class_select_key = 'sub_class_select'

with col_main_class:
    st.selectbox(
        "メインクラス",
        options=ALL_CLASSES,
        key=main_class_select_key,
    )
    main_class = st.session_state[main_class_select_key]

with col_sub_class:
    if main_class in SUCCESSOR_MAIN_CLASSES:
        # 後継クラスの場合、サブクラスは選択不可
        st.selectbox(
            "サブクラス",
            options=["None"],
            index=0,
            key=sub_class_select_key,
            disabled=True,
        )
        if st.session_state.get(sub_class_select_key) != "None": st.session_state[sub_class_select_key] = "None" 
        st.info(f"{main_class}は後継クラスのため、サブクラスはNone固定です。", icon="ℹ️")
    else:
        sub_class_options_filtered = ["None"] + [c for c in ALL_CLASSES if c != main_class and c not in UNAVAILABLE_SUBCLASSES]
        st.selectbox(
            "サブクラス",
            options=sub_class_options_filtered,
            key=sub_class_select_key,
        )
        # Hrなどが誤って選択された場合の処理（保険）
        sub_class = st.session_state[sub_class_select_key]
        if sub_class in UNAVAILABLE_SUBCLASSES:
            st.warning(f"{sub_class}はサブクラスに設定できません。Noneに戻します。")
            st.session_state[sub_class_select_key] = "None"
            st.rerun()

sub_class_select = st.session_state[sub_class_select_key]

st.markdown("---")

# --- B. 種族設定 ---
st.markdown("### 種族設定")
RACE_OPTIONS = list(RACE_CORRECTIONS.keys())
st.selectbox(
    "種族",
    options=RACE_OPTIONS,
    key="race_select",
)
st.markdown("---")

# --- C. マグ設定と各種ボーナス ---
st.markdown("### マグ/ボーナス設定")

# マグの入力
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

# クラスブースト設定
st.markdown("##### 固定ボーナス")
st.checkbox(
    "クラスブースト（全クラスLv75達成）",
    key="class_boost_enabled",
    value=st.session_state['class_boost_enabled'],
    help="HP+60, PP+10, 攻撃力+120, 技量+60, 防御力+90が加算されます。"
)
st.markdown("---")

# --- D. 合計基本ステータス表示 (計算結果表示) ---
total_stats = get_calculated_stats()
st.markdown("### 合計基本ステータス")

st.markdown("###### 適用されている基本ステータス計算ロジック")
st.markdown(r"**HP:** $\text{floor}((\text{メイン基礎値} \times \text{種族補正}) + (\text{サブ基礎値} \times \text{種族補正} \times \text{0.2}) + \text{クラスブースト}) + \text{スキルボーナス}$")
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
st.markdown("---")

# -----------------------------------------------------------------
# 5-2. スキルツリーシミュレーター UI (統合部分)
# -----------------------------------------------------------------

st.header("2. スキルツリーシミュレーター")

# --- A. SP設定とサマリー ---

# 現在の合計SPの計算
main_allocations = st.session_state['all_sp_allocations'].get(main_class, {})
# サブクラスの名称を取得 (Noneの場合もそのままキーとして利用)
sub_class_name_key = st.session_state.get('sub_class_select', 'None')
sub_allocations = st.session_state['all_sp_allocations'].get(sub_class_name_key, {})


total_sp_spent = sum(main_allocations.values())
sub_tab_enabled = sub_class_name_key != 'None' and sub_class_name_key in ALL_SKILL_DATA # スキルデータがあるかもチェック

if sub_tab_enabled:
    total_sp_spent += sum(sub_allocations.values()) # サブクラスのSPを加算

total_sp_available = st.session_state['total_sp_available']
remaining_sp = total_sp_available - total_sp_spent

st.markdown("### 🛠️ SP設定とサマリー")
col_sp_input, col_sp_summary, col_sp_remaining = st.columns(3)

with col_sp_input:
    st.number_input(
        "利用可能な合計SP",
        min_value=1,
        max_value=150, 
        value=total_sp_available,
        step=1,
        key='total_sp_available',
        label_visibility="visible",
        help="メインクラスとサブクラスで合計して使用できるSPの最大値です。"
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

# --- B. スキル配分エリア (st.tabsを使用) ---

# スキル入力のロジック
def update_allocation(class_name, skill_name):
    # 選択されたクラスの割り当てを更新
    input_key = f"level_input_{class_name}_{skill_name}"
    st.session_state['all_sp_allocations'][class_name][skill_name] = st.session_state[input_key]


# メインクラスのタブ名
main_tab_title = f"メイン: {main_class} ({sum(main_allocations.values())} SP)"

# サブクラスのタブ名
sub_class_name_key = sub_class_name_key if sub_class_name_key != 'None' else "None"
sub_tab_title = f"サブ: {sub_class_name_key} ({sum(sub_allocations.values())} SP)" if sub_tab_enabled else f"サブ: {sub_class_name_key}"


tab_main, tab_sub = st.tabs([main_tab_title, sub_tab_title])

# スキルツリー描画関数
def render_skill_tree(class_name, allocations):
    current_skills = ALL_SKILL_DATA.get(class_name, {})
    if not current_skills:
        st.info("このクラスのスキルデータは現在準備されていません。")
        return

    st.markdown(f"#### {class_name} スキルポイント配分")
    
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

# メインクラスのタブ内容
with tab_main:
    render_skill_tree(main_class, main_allocations)

# サブクラスのタブ内容
with tab_sub:
    if sub_tab_enabled:
        render_skill_tree(sub_class_name_key, sub_allocations)
    else:
        st.info("サブクラスが選択されていないか、選択されたクラスがサブクラスとして使用できません。")


st.markdown("---")
st.markdown("### 📊 HP アップスキルボーナス一覧 (参考)")

hp_cols = st.columns(4)

def render_hp_bonus_table(key, title, col):
    with col:
        st.markdown(f"**{title}**")
        data = HP_UP_BONUSES.get(key, {})
        if data:
            st.table({"レベル": data.keys(), "ボーナスHP": data.values()})
        else:
             st.info("データなし")


render_hp_bonus_table("HPアップ 1", "HPアップ 1 (共通)", hp_cols[0])
render_hp_bonus_table("HPアップ (Su)", "HPアップ (Su)", hp_cols[1])
render_hp_bonus_table("HPハイアップ", "HPハイアップ (Su)", hp_cols[2])
render_hp_bonus_table("HPアップ (後継)", "HPアップ (後継)", hp_cols[3])
