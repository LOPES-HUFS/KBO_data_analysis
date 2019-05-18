import ast
import json

from requests_html import HTMLSession
from bs4 import BeautifulSoup

import api.pasing_page

def get_game(date, home_team, away_team, double=0):
    ''' 개별 게임을 가져오는 함수
    쉽게 분석할 수 있도록 soup 으로 내보낸다.

    Args:
        date (int): 20190511 과 같이 숫자로 만든 경기 날짜
        home_team (str): 홈팀
    
    Returns:
        soup (soup): BeautifulSoup의 soup
    '''
    url = (f'https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx?gameDate={date}&gameId={date}{home_team}{away_team}{double}&section=REVIEW')
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    soup = BeautifulSoup(r.html.html, "lxml")
    return soup

def get_data(soup):
    tables = soup.find_all('table')
    record_etc = soup.findAll('div',{'class':'record-etc'})
    box_score = soup.findAll('div',{'class':'box-score-wrap'})
    teams = box_score[0].findAll('span',{'class':'logo'})
    temp_scoreboard = api.pasing_page.scoreboard(tables, teams)

    temp_all = {'scoreboard':ast.literal_eval(temp_scoreboard.to_json(orient='records'))}
    temp_all.update({"ETC_info":api.pasing_page.ETC_info(temp_page['tables'],temp_page['record_etc'])})
    temp_all.update({'away_batter':ast.literal_eval(away_batter(temp_page['tables'],temp_page['teams']).to_json(orient='records'))})
    temp_all.update({'home_batter':ast.literal_eval(home_batter(temp_page['tables'],temp_page['teams']).to_json(orient='records'))})
    temp_all.update({'away_pitcher':ast.literal_eval(away_pitcher(temp_page['tables'],temp_page['teams']).to_json(orient='records'))})
    temp_all.update({'home_pitcher':ast.literal_eval(home_pitcher(temp_page['tables'],temp_page['teams']).to_json(orient='records'))})

    temp_name = temp_page['date']+'_'+temp_page['id']
    return{'tables':tables, 'record_etc':record_etc, 'teams':teams, 'date':date, 'id':gameld}
    return soup