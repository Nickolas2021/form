import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Настройка страницы
st.set_page_config(
    page_title="Статистика команд Dota 2",
    page_icon="🎮",
    layout="wide"
)

# Функция для инициализации session state
def init_session_state():
    if 'games_data' not in st.session_state:
        st.session_state.games_data = []

# Функция для создания формы команды
def create_team_form(team_name, key_prefix):
    st.subheader(f"📊 Команда {team_name}")
    
    # Данные команды
    with st.expander(f"Общая информация команды {team_name}", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            team_rank = st.number_input(f"Ранг команды {team_name}",  
                                            key=f"{key_prefix}_rank")
            
            team_prize = st.number_input(f"Призовые {team_name} ($)", 
                                            key=f"{key_prefix}_prize")
            
            first_places = st.number_input(f"Количество первых мест {team_name}", 
                                            key=f"{key_prefix}_first")
        
        with col2:
            win_rate = st.number_input(f"Процент побед команды {team_name} (%)",  
                                            key=f"{key_prefix}_winrate")
            
            total_games = st.number_input(f"Всего игр {team_name}",  
                                            key=f"{key_prefix}_games")
            
            team_region = st.selectbox(f"Регион {team_name}", 
                                            ["Europe", "North America","South America", "Asia", "China", "SEA", "CIS", "Africa"], 
                                            key=f"{key_prefix}_region")
    
    # Данные игроков
    players_data = []
    
    for pos in range(1, 6):
        with st.expander(f"👤 Игрок позиции {pos}", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                player_hero = st.text_input(f"Герой с аспектом",  
                                          key=f"{key_prefix}_p{pos}_hero")
                
                player_age = st.number_input(f"Возраст",  
                                           key=f"{key_prefix}_p{pos}_age")
            
            with col2:
                player_winrate = st.number_input(f"Процент побед (%)", 
                                            key=f"{key_prefix}_p{pos}_winrate")
                
                player_prize = st.number_input(f"Призовые ($)",  
                                             key=f"{key_prefix}_p{pos}_prize")
            
            with col3:
                player_kda = st.number_input(f"KDA",  
                                            key=f"{key_prefix}_p{pos}_kda")
                
                player_rank = st.number_input(f"Ранг", 
                                                   key=f"{key_prefix}_p{pos}_rank")
                
            with col4:
                player_gold_in_min = st.number_input(f"Золота в минуту",
                                                     key=f"{key_prefix}_p{pos}_gold")
                player_exp_in_min = st.number_input(f"Опыта в минуту",
                                                     key=f"{key_prefix}_p{pos}_exp")
                

        
        # Сохраняем данные игрока
        player_data = {
            'position': pos,
            'hero': player_hero,
            'age': player_age,
            'winrate': player_winrate,
            'prize': player_prize,
            'kda': player_kda,
            'rank': player_rank,
            'gold': player_gold_in_min,
            'exp': player_exp_in_min
        }
        players_data.append(player_data)
    
    # Возвращаем все данные команды
    team_data = {
        'team_name': team_name,
        'rank': team_rank,
        'prize': team_prize,
        'first_places': first_places,
        'win_rate': win_rate,
        'total_games': total_games,
        'region': team_region,
        'players': players_data
    }
    
    return team_data

# Функция для конвертации данных в CSV формат
@st.cache_data
def convert_to_csv(games_data):
    rows = []
    
    for game in games_data:
        # Базовая информация об игре
        row = {
            'match_date': game['match_date'],
            'match_time': game['match_time']
        }
        
        # Данные команды Radiant
        radiant = game['radiant']
        row.update({
            'radiant_name': radiant['team_name'],
            'radiant_rank': radiant['rank'],
            'radiant_prize': radiant['prize'],
            'radiant_first_places': radiant['first_places'],
            'radiant_win_rate': radiant['win_rate'],
            'radiant_total_games': radiant['total_games'],
            'radiant_region': radiant['region']
        })
        
        # Данные игроков Radiant
        for i, player in enumerate(radiant['players'], 1):
            row.update({
                f'radiant_p{i}_hero': player['hero'],
                f'radiant_p{i}_age': player['age'],
                f'radiant_p{i}_winrate': player['winrate'],
                f'radiant_p{i}_prize': player['prize'],
                f'radiant_p{i}_rank': player['rank'],
                f'radiant_p{i}_kda': player['kda'],
                f'radiant_p{i}_gold': player['gold'],
                f'radiant_p{i}_exp': player['exp']
            })
        
        # Данные команды Dire
        dire = game['dire']
        row.update({
            'dire_name': dire['team_name'],
            'dire_rank': dire['rank'],
            'dire_prize': dire['prize'],
            'dire_first_places': dire['first_places'],
            'dire_win_rate': dire['win_rate'],
            'dire_total_games': dire['total_games'],
            'dire_region': dire['region']
        })
        
        # Данные игроков Dire
        for i, player in enumerate(dire['players'], 1):
            row.update({
                f'dire_p{i}_hero': player['hero'],
                f'dire_p{i}_age': player['age'],
                f'dire_p{i}_winrate': player['winrate'],
                f'dire_p{i}_prize': player['prize'],
                f'dire_p{i}_rank': player['rank'],
                f'dire_p{i}_kda': player['kda'],
                f'dire_p{i}_gold': player['gold'],
                f'dire_p{i}_exp': player['exp']
            })
        
        rows.append(row)
    
    df = pd.DataFrame(rows)
    return df.to_csv(index=False).encode('utf-8')

# Основное приложение
def main():
    init_session_state()
    
    # Заголовок приложения
    st.title("🎮 Сбор статистики команд Dota 2")
    st.markdown("---")
    
    # Основная форма
    with st.form("match_stats_form"):
        st.subheader("⚔️ Информация о матче")
        
        # Общие данные матча
        col1, col2 = st.columns(2)
        with col1:
            match_date = st.date_input("Дата матча", value=datetime.now().date())
        with col2:
            match_time = st.time_input("Время матча", value=datetime.now().time())
        
        st.markdown("---")
        
        # Создаем формы для обеих команд
        col1, col2 = st.columns(2)
        
        with col1:
            radiant_data = create_team_form("Radiant", "radiant")
        
        with col2:
            dire_data = create_team_form("Dire", "dire")
        
        # Кнопка отправки формы
        submitted = st.form_submit_button("💾 Сохранить данные матча", type="primary")
        
        if submitted:
            # Сохраняем данные матча
            match_data = {
                'match_date': match_date.strftime('%Y-%m-%d'),
                'match_time': match_time.strftime('%H:%M:%S'),
                'radiant': radiant_data,
                'dire': dire_data
            }
            
            st.session_state.games_data.append(match_data)
            st.success(f"✅ Данные матча сохранены! Всего записей: {len(st.session_state.games_data)}")
            st.balloons()
    
    # Показываем сохраненные данные
    if st.session_state.games_data:
        st.markdown("---")
        st.subheader("📈 Сохраненные данные")
        
        # Показываем количество записей
        st.info(f"📊 Всего записано матчей: {len(st.session_state.games_data)}")
        
        # Показываем последние записи
        with st.expander("👁️ Просмотр последних записей", expanded=False):
            for i, game in enumerate(reversed(st.session_state.games_data[-5:]), 1):
                st.write(f"**Матч {len(st.session_state.games_data) - i + 1}:** {game['radiant']['team_name']} vs {game['dire']['team_name']} ({game['match_date']})")
        
        # Кнопки экспорта
        st.markdown("---")
        st.subheader("💾 Экспорт данных")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Кнопка скачивания CSV
            csv_data = convert_to_csv(st.session_state.games_data)
            st.download_button(
                label="📥 Скачать CSV",
                data=csv_data,
                file_name=f"dota2_team_stats_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                help="Скачать все данные в формате CSV для машинного обучения"
            )
        
        with col2:
            # Кнопка очистки данных
            if st.button("🗑️ Очистить все данные", help="Удалить все сохраненные записи"):
                st.session_state.games_data = []
                st.success("Все данные очищены!")
                st.rerun()
        
        with col3:
            # Показать превью CSV
            if st.button("👁️ Показать превью CSV"):
                if st.session_state.games_data:
                    df = pd.read_csv(pd.io.common.BytesIO(csv_data))
                    st.dataframe(df.head(), use_container_width=True)

if __name__ == "__main__":
    main()
