import streamlit as st
import json
from typing import List, Dict

from info import PLAYERS, HEROES, TEAMS

# Настройка страницы
st.set_page_config(page_title="Dota 2 Match Stats", layout="wide")

# Заголовок
st.title("📊 Заполнение статистики матча Dota 2")

# Списки для автозаполнения
TEAMS_LIST = TEAMS

PLAYERS_LIST = PLAYERS

HEROES_LIST = HEROES

# Инициализация session state
if 'match_data' not in st.session_state:
    st.session_state.match_data = None

# Форма для ввода данных
with st.form("match_form"):
    st.header("Информация о матче")
    
    # Две колонки для команд
    col1, col2 = st.columns(2)
    
    # Dire team
    with col1:
        st.subheader("🔴 Dire")
        dire_team_name = st.selectbox(
            "Название команды Dire",
            options=[""] + TEAMS_LIST,
            index=0,
            key="dire_team",
            help="Начните вводить для поиска команды"
        )
        
        st.write("---")
        
        dire_players = []
        for i in range(5):
            st.write(f"**Игрок {i+1} (pos {i+1})**")
            player_name = st.selectbox(
                f"Имя игрока",
                options=[""] + PLAYERS_LIST,
                key=f"dire_player_{i}",
                help="Начните вводить для поиска игрока"
            )
            hero = st.selectbox(
                f"Герой",
                options=[""] + HEROES_LIST,
                key=f"dire_hero_{i}",
                help="Начните вводить для поиска героя"
            )
            dire_players.append({
                "name": player_name,
                "hero": hero,
                "pos": str(i+1)
            })
            if i < 4:  # Не добавлять разделитель после последнего игрока
                st.divider()
    
    # Radiant team
    with col2:
        st.subheader("🟢 Radiant")
        radiant_team_name = st.selectbox(
            "Название команды Radiant",
            options=[""] + TEAMS_LIST,
            index=0,
            key="radiant_team",
            help="Начните вводить для поиска команды"
        )
        
        st.write("---")
        
        radiant_players = []
        for i in range(5):
            st.write(f"**Игрок {i+1} (pos {i+1})**")
            player_name = st.selectbox(
                f"Имя игрока",
                options=[""] + PLAYERS_LIST,
                key=f"radiant_player_{i}",
                help="Начните вводить для поиска игрока"
            )
            hero = st.selectbox(
                f"Герой",
                options=[""] + HEROES_LIST,
                key=f"radiant_hero_{i}",
                help="Начните вводить для поиска героя"
            )
            radiant_players.append({
                "name": player_name,
                "hero": hero,
                "pos": str(i+1)
            })
            if i < 4:  # Не добавлять разделитель после последнего игрока
                st.divider()
    
    # Winner selection
    st.subheader("🏆 Победитель")
    winner = st.selectbox(
        "Выберите победителя",
        options=["Dire", "Radiant"],
        index=0
    )
    
    # Submit button
    submitted = st.form_submit_button("💾 Сохранить данные матча", use_container_width=True)
    
    if submitted:
        # Создание структуры данных
        match_data = {
            "Dire": {
                "name": dire_team_name,
                "players": dire_players
            },
            "Radiant": {
                "name": radiant_team_name,
                "players": radiant_players
            },
            "Winner": winner
        }
        
        st.session_state.match_data = match_data
        st.success("✅ Данные матча успешно сохранены!")

# Отображение и экспорт данных
if st.session_state.match_data:
    st.header("📄 Результат")
    
    # Показать JSON
    st.json(st.session_state.match_data)
    
    # Кнопка для скачивания JSON
    json_string = json.dumps(st.session_state.match_data, indent=4, ensure_ascii=False)
    st.download_button(
        label="⬇️ Скачать JSON",
        data=json_string,
        file_name="match_stats.json",
        mime="application/json"
    )
    
    # Кнопка для очистки данных
    if st.button("🗑️ Очистить данные"):
        st.session_state.match_data = None
        st.rerun()


