import streamlit as st
import numpy as np
st.title("home")
# --- 1. ダメージ計算ロジックの定義 (上記の関数を再掲) ---
def calculate_pso2_damage(attack_power, enemy_defense, total_multiplier):
    """
    PSO2のダメージ計算（簡略版）
    """
    min_rand = 0.9
    max_rand = 1.0
    
    base_damage = attack_power - enemy_defense
    
    # ダメージがマイナスにならないように処理
    if base_damage < 0:
        base_damage = 1 # 最小ダメージを1とする
        
    damage_before_rand = base_damage * total_multiplier
    
    min_damage = int(damage_before_rand * min_rand)
    max_damage = int(damage_before_rand * max_rand)
    expected_damage = int(damage_before_rand * (min_rand + max_rand) / 2)
    
    return min_damage, max_damage, expected_damage


# --- 2. Streamlit UIの構築 ---
st.set_page_config(
    page_title="PSO2 ダメージ計算ツール (Streamlit版)", 
    layout="centered"
)
st.title("🛡️ PSO2 ダメージ計算ツール (簡易版)")
st.caption("必要な入力値に基づいて、ダメージの最小値・最大値・期待値を計算します。")

st.markdown("---")

# プレイヤー側の入力
st.header("1. プレイヤー側のステータス")
player_attack = st.number_input(
    "最終攻撃力 (武器攻撃力 + ユニット攻撃力 + スキル補正など)", 
    min_value=1, 
    value=3000, 
    step=10,
    key='p_atk'
)

# 倍率の入力 (複数の倍率を掛け合わせるのが一般的ですが、ここでは単純化)
st.header("2. ダメージ倍率")
st.info("潜在能力、スキル、クラス補正、弱点属性などの全ての倍率を**掛け合わせた値**を入力してください。")
total_multiplier = st.slider(
    "総合ダメージ倍率 (例: 1.45)",
    min_value=1.0, 
    max_value=5.0, 
    value=1.50, 
    step=0.01,
    key='p_mult'
)

# エネミー側の入力
st.header("3. エネミー側のステータス")
enemy_defense = st.number_input(
    "エネミーの防御力 (エネミーデータに基づき入力)", 
    min_value=1, 
    value=1000, 
    step=10,
    key='e_def'
)

st.markdown("---")

# --- 3. ロジックの実行と結果の表示 ---
if st.button("ダメージを計算する 💥"):
    min_dmg, max_dmg, expected_dmg = calculate_pso2_damage(
        player_attack, 
        enemy_defense, 
        total_multiplier
    )

    st.header("🎉 計算結果")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="最小ダメージ (Min)", value=f"{min_dmg:,}")
    
    with col2:
        st.metric(label="期待値ダメージ (Exp)", value=f"{expected_dmg:,}")
        
    with col3:
        st.metric(label="最大ダメージ (Max)", value=f"{max_dmg:,}")

    st.success("計算が完了しました！")
    
