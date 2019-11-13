'''
경기 기록이 있는 데이터에 선수 id를 매칭하기 위한 함수들 
'''

import pandas as pd

player_id_list = pd.read_csv("data/KBO_player_info_full.csv")

rename_player = pd.read_csv("data/renamed_player_list.csv")

def get_id(name):
    '''
    선수 이름을 인자로 받아 선수 id를 얻는 함수 

    Args:
        name(str): 선수 이름
    Returns:
        output(list): 입력된 선수 이름의 모든 선수 id (동명이인 포함)
    '''
    return list(player_id_list.ID[player_id_list['선수명']==name])

def find_id(name,year,team):
    '''
    이름 연도 팀 정보를 받아 동명이인 선수의 id를 구분하는 함수  
    단 같은 연도에 같은 팀에서 경기를 한 동명이인 선수의 경우 구분 불가능 
    추후 그런 선수들의 경우 직접 구분해야함 

    Args:
        name(str): 선수 이름
        year(numeric): 선수가 출장한 경기 연도
        team(str): 선수의 소속팀 

    Returns:
        output(list): 입력된 선수 이름과 연도 팀으로 찾은 선수 id 
    '''
    temp = player_id_list[player_id_list['선수명']==name]
    return [temp.ID[temp["season_"+year]==i].values for i in list(temp["season_"+year]) if team in i]

error = []
def match_id(data,name,year,team):
    '''
    입력받은 데이터에 선수 이름과 연도 팀 정보를 토대로 해당 선수의 id를 매칭해주는 함수 
    이 때 같은 연도에 같은 팀에서 경기를 한 동명이인 선수의 경우는 id 매치가 되지 않는다.

    Args:
        data(pandas DF): 타자 데이터 혹은 투수 데이터 
        name(str): 선수 이름
        year(numeric): 선수가 출장한 경기 연도
        team(str): 선수의 소속팀 

    Returns:
        data(pandas DF): id가 입력된 타자 또는 투수 데이터
    '''
    year = str(year)
    id_list = get_id(name)
    if len(id_list)==1:
        data.id[data["선수명"]==name] = int(id_list[0])
    elif len(id_list)==0:
        if check_rename(name) != "not_rename_player":
            newname = check_rename(name)
            id_list = get_id(newname)
            data.id[data["선수명"]==name] = int(id_list[0])
        else:
            error.append([name,year,team])
    else:
        print(name,year,team)
        id_list = list(find_id(name,year,team)[0])
        if len(id_list)>=2:
            print("check_record")
            data.id[(data["선수명"]==name) & (data.팀.isin([team])) & (data.year.isin([year]))] = 0
        else:
            data.id[(data["선수명"]==name) & (data.팀.isin([team])) & (data.year.isin([year]))] = int(id_list[0])
    return data

def check_rename(name):
    '''
    어떤 선수의 이름이 개명한 선수인지 아닌지를 검사하는 함수

    Args:
        name(str): 선수 이름

    Returns:
        output(str): 만약 개명한 선수라면 선수의 개명한 이름이 나오고 아니라면 "not_rename_player" 문구가 리턴
    '''
    rename_tmp=rename_player.where(name == rename_player.before_name).dropna()
    if len(rename_tmp) !=0:
        return rename_tmp["rename"].values[0]
    else:
        return "not_rename_player" 
