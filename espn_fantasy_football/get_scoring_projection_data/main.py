import requests
import pandas as pd


def extract_position_data(row, side, position):
    try:
        position_data = list(filter(lambda item: item['lineupSlotId'] == position,
                                    row[side]['rosterForCurrentScoringPeriod']['entries']))
    except:
        print('big ol tiddies')

    return position_data


def split_positions(data, expected_num):
    if expected_num == 2:
        if len(data) == 2:
            name_1 = data[0]['playerPoolEntry']['player']['fullName']
            name_2 = data[1]['playerPoolEntry']['player']['fullName']
            proj_1 = \
            list(filter(lambda item: item['statSourceId'] == 1, data[0]['playerPoolEntry']['player']['stats']))[0][
                'appliedTotal']
            proj_2 = \
            list(filter(lambda item: item['statSourceId'] == 1, data[1]['playerPoolEntry']['player']['stats']))[0][
                'appliedTotal']
            try:
                act_1 = \
                list(filter(lambda item: item['statSourceId'] == 0, data[0]['playerPoolEntry']['player']['stats']))[0][
                    'appliedTotal']
            except:
                act_1 = 'inactive player started'
            try:
                act_2 = \
                list(filter(lambda item: item['statSourceId'] == 0, data[1]['playerPoolEntry']['player']['stats']))[0][
                    'appliedTotal']
            except:
                act_2 = 'inactive player started'
        elif len(data) == 1:
            name_1 = data[0]['playerPoolEntry']['player']['fullName']
            proj_1 = \
            list(filter(lambda item: item['statSourceId'] == 1, data[0]['playerPoolEntry']['player']['stats']))[0][
                'appliedTotal']
            try:
                act_1 = \
                list(filter(lambda item: item['statSourceId'] == 0, data[0]['playerPoolEntry']['player']['stats']))[0][
                    'appliedTotal']
            except:
                print('tits')
            name_2 = 'no player started'
            proj_2 = 'no player started'
            act_2 = 'no player started'
        elif len(data) == 0:
            name_1 = 'no player started'
            name_2 = 'no player started'
            proj_1 = 'no player started'
            proj_2 = 'no player started'
            act_1 = 'no player started'
            act_2 = 'no player started'

        return name_1, proj_1, act_1, name_2, proj_2, act_2

    if expected_num == 1:
        if len(data) == 1:
            name_1 = data[0]['playerPoolEntry']['player']['fullName']
            try:
                proj_1 = \
                    list(filter(lambda item: item['statSourceId'] == 1, data[0]['playerPoolEntry']['player']['stats']))[
                        0][
                        'appliedTotal']
                act_1 = \
                list(filter(lambda item: item['statSourceId'] == 0, data[0]['playerPoolEntry']['player']['stats']))[0][
                    'appliedTotal']
            except:
                proj_1 = 'inactive_player_started'
                act_1 = 'inactive player started'
        elif len(data) == 0:
            name_1 = 'no player started'
            proj_1 = 'no player started'
            act_1 = 'no player started'

        return name_1, proj_1, act_1


# Initialize Global Parameters
league_id = 493554
year = 2018
current_week = 17
swid = "{47C30300-F34E-4F8A-808F-02562DA3925D}"
espn_s2 = "AECKGX7idqLg0P67gnm3%2Bgv%2BdW5zfpqZp%2FcbkYuEfhC115feoA4IoW52DTDHinMYCC0Lpg4yfTwS6jsSVlmeKEYI3yem2EDQgPpL1vkGT8KnxEVg660MSiDoMo9pvHTt2CD3tmGRLqUw3wSncABoxdg8F2NKSWsJvy7gyyn66B5%2B8ILo8kv4G9d4%2BeL%2B1EWLV%2B1woGvkWv%2FJYESJrclvF2UWQZc%2FC5JJlPbVRlvoHiblx2hgZJdg8D38pnUNETyVJbn2rLC5Cxjy%2FLcS7YaAEacY"

response = requests.get(
    "https://fantasy.espn.com/apis/v3/games/ffl/seasons/" + str(year) + "/segments/0/leagues/" + str(league_id),
    cookies={"swid": swid, "espn_s2": espn_s2})
response_json = response.json()

team_info = {}

for index, team in enumerate(response_json["teams"]):
    team_info_temp = {}

    team_info_temp['id'] = team['id']
    team_info_temp['abbrev'] = team['abbrev']
    team_info_temp['location'] = team['location']
    team_info_temp['nickname'] = team['nickname']

    team_info[team['id']] = team_info_temp

team_info_df = pd.DataFrame.from_dict(team_info, orient='index')
main_df = pd.DataFrame(columns=['team_id', 'team_abbrev', 'team_location', 'team_nickname', 'week', 'playoffs?!', 'opp',
                                'name_qb', 'proj_qb', 'act_qb', 'name_rb1', 'proj_rb1', 'act_rb1', 'name_rb2',
                                'proj_rb2', 'act_rb2', 'name_wr1', 'proj_wr1', 'act_wr1', 'name_wr2', 'proj_wr2',
                                'act_wr2', 'name_te', 'proj_te', 'act_te', 'name_flex', 'proj_flex', 'act_flex',
                                'name_dl1', 'proj_dl1', 'act_dl1', 'name_dl2', 'proj_dl2', 'act_dl2', 'name_lb1',
                                'proj_lb1',
                                'act_lb1', 'name_lb2', 'proj_lb2', 'act_lb2', 'name_db1', 'proj_db1', 'act_db1',
                                'name_db2',
                                'proj_db2', 'act_db2', 'name_dst', 'proj_dst', 'act_dst', 'name_k', 'proj_k', 'act_k'])

# Loop through weekly matchups to get box score data
week = 1
final_week = current_week
weekly_data_json = []

while week <= final_week:
    url = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/' + str(year) + '/segments/0/leagues/' + str(
        league_id) + '?view=mMatchup&view=mMatchupScore'
    weekly_response = requests.get(url, params={'scoringPeriodId': week}, cookies={"SWID": swid, "espn_s2": espn_s2})
    weekly_response_json = weekly_response.json()

    for row in weekly_response_json['schedule']:
        if row['matchupPeriodId'] == week and 'away' in row:
            team_id_a = row['away']['teamId']
            team_id_h = row['home']['teamId']
            team_abbrev_a = team_info_df[team_info_df['id'] == row['away']['teamId']]['abbrev'].values.item()
            team_abbrev_h = team_info_df[team_info_df['id'] == row['home']['teamId']]['abbrev'].values.item()
            team_location_a = team_info_df[team_info_df['id'] == row['away']['teamId']]['location'].values.item()
            team_location_h = team_info_df[team_info_df['id'] == row['home']['teamId']]['location'].values.item()
            team_nickname_a = team_info_df[team_info_df['id'] == row['away']['teamId']]['nickname'].values.item()
            team_nickname_h = team_info_df[team_info_df['id'] == row['home']['teamId']]['nickname'].values.item()
            name_qb_a, proj_qb_a, act_qb_a = split_positions(extract_position_data(row, 'away', 0), 1)
            name_qb_h, proj_qb_h, act_qb_h = split_positions(extract_position_data(row, 'home', 0), 1)
            name_rb1_a, proj_rb1_a, act_rb1_a, name_rb2_a, proj_rb2_a, act_rb2_a = split_positions(
                extract_position_data(row, 'away', 2), 2)
            name_rb1_h, proj_rb1_h, act_rb1_h, name_rb2_h, proj_rb2_h, act_rb2_h = split_positions(
                extract_position_data(row, 'home', 2), 2)
            name_wr1_a, proj_wr1_a, act_wr1_a, name_wr2_a, proj_wr2_a, act_wr2_a = split_positions(
                extract_position_data(row, 'away', 4), 2)
            name_wr1_h, proj_wr1_h, act_wr1_h, name_wr2_h, proj_wr2_h, act_wr2_h = split_positions(
                extract_position_data(row, 'home', 4), 2)
            name_te_a, proj_te_a, act_te_a = split_positions(extract_position_data(row, 'away', 6), 1)
            name_te_h, proj_te_h, act_te_h = split_positions(extract_position_data(row, 'home', 6), 1)
            name_flex_a, proj_flex_a, act_flex_a = split_positions(extract_position_data(row, 'away', 23), 1)
            name_flex_h, proj_flex_h, act_flex_h = split_positions(extract_position_data(row, 'home', 23), 1)
            name_lb1_a, proj_lb1_a, act_lb1_a, name_lb2_a, proj_lb2_a, act_lb2_a = split_positions(
                extract_position_data(row, 'away', 10), 2)
            name_lb1_h, proj_lb1_h, act_lb1_h, name_lb2_h, proj_lb2_h, act_lb2_h = split_positions(
                extract_position_data(row, 'home', 10), 2)
            name_dl1_a, proj_dl1_a, act_dl1_a, name_dl2_a, proj_dl2_a, act_dl2_a = split_positions(
                extract_position_data(row, 'away', 11), 2)
            name_dl1_h, proj_dl1_h, act_dl1_h, name_dl2_h, proj_dl2_h, act_dl2_h = split_positions(
                extract_position_data(row, 'home', 11), 2)
            name_db1_a, proj_db1_a, act_db1_a, name_db2_a, proj_db2_a, act_db2_a = split_positions(
                extract_position_data(row, 'away', 14), 2)
            name_db1_h, proj_db1_h, act_db1_h, name_db2_h, proj_db2_h, act_db2_h = split_positions(
                extract_position_data(row, 'home', 14), 2)
            name_dst_a, proj_dst_a, act_dst_a = split_positions(extract_position_data(row, 'away', 16), 1)
            name_dst_h, proj_dst_h, act_dst_h = split_positions(extract_position_data(row, 'home', 16), 1)
            name_k_a, proj_k_a, act_k_a = split_positions(extract_position_data(row, 'away', 17), 1)
            name_k_h, proj_k_h, act_k_h = split_positions(extract_position_data(row, 'home', 17), 1)

            main_df = main_df.append(
                {'team_id': team_id_a, 'team_abbrev': team_abbrev_a, 'team_location': team_location_a,
                 'team_nickname': team_nickname_a, 'week': week, 'playoffs?!': row['playoffTierType'],
                 'opp': team_abbrev_h,
                 'name_qb': name_qb_a, 'proj_qb': proj_qb_a, 'act_qb': act_qb_a, 'name_rb1': name_rb1_a,
                 'proj_rb1': proj_rb1_a, 'act_rb1': act_rb1_a, 'name_rb2': name_rb2_a,
                 'proj_rb2': proj_rb2_a, 'act_rb2': act_rb2_a, 'name_wr1': name_wr1_a, 'proj_wr1': proj_wr1_a,
                 'act_wr1': act_wr1_a, 'name_wr2': name_wr2_a, 'proj_wr2': proj_wr2_a,
                 'act_wr2': act_wr2_a, 'name_te': name_te_a, 'proj_te': proj_te_a, 'act_te': act_te_a,
                 'name_flex': name_flex_a, 'proj_flex': proj_flex_a, 'act_flex': act_flex_a,
                 'name_dl1': name_dl1_a, 'proj_dl1': proj_dl1_a, 'act_dl1': act_dl1_a, 'name_dl2': name_dl2_a,
                 'proj_dl2': proj_dl2_a, 'act_dl2': act_dl2_a, 'name_lb1': name_lb1_a, 'proj_lb1': proj_lb1_a,
                 'act_lb1': act_lb1_a, 'name_lb2': name_lb2_a, 'proj_lb2': proj_lb2_a, 'act_lb2': act_lb2_a,
                 'name_db1': name_db1_a, 'proj_db1': proj_db1_a, 'act_db1': act_db1_a, 'name_db2': name_db2_a,
                 'proj_db2': proj_db2_a, 'act_db2': act_db2_a, 'name_dst': name_dst_a, 'proj_dst': proj_dst_a,
                 'act_dst': act_dst_a, 'name_k': name_k_a, 'proj_k': proj_k_a, 'act_k': act_k_a}, ignore_index=True)
            main_df = main_df.append(
                {'team_id': team_id_h, 'team_abbrev': team_abbrev_h, 'team_location': team_location_h,
                 'team_nickname': team_nickname_h, 'week': week, 'playoffs?!': row['playoffTierType'],
                 'opp': team_abbrev_a,
                 'name_qb': name_qb_h, 'proj_qb': proj_qb_h, 'act_qb': act_qb_h, 'name_rb1': name_rb1_h,
                 'proj_rb1': proj_rb1_h, 'act_rb1': act_rb1_h, 'name_rb2': name_rb2_h,
                 'proj_rb2': proj_rb2_h, 'act_rb2': act_rb2_h, 'name_wr1': name_wr1_h, 'proj_wr1': proj_wr1_h,
                 'act_wr1': act_wr1_h, 'name_wr2': name_wr2_h, 'proj_wr2': proj_wr2_h,
                 'act_wr2': act_wr2_h, 'name_te': name_te_h, 'proj_te': proj_te_h, 'act_te': act_te_h,
                 'name_flex': name_flex_h, 'proj_flex': proj_flex_h, 'act_flex': act_flex_h,
                 'name_dl1': name_dl1_h, 'proj_dl1': proj_dl1_h, 'act_dl1': act_dl1_h, 'name_dl2': name_dl2_h,
                 'proj_dl2': proj_dl2_h, 'act_dl2': act_dl2_h, 'name_lb1': name_lb1_h, 'proj_lb1': proj_lb1_h,
                 'act_lb1': act_lb1_h, 'name_lb2': name_lb2_h, 'proj_lb2': proj_lb2_h, 'act_lb2': act_lb2_h,
                 'name_db1': name_db1_h, 'proj_db1': proj_db1_h, 'act_db1': act_db1_h, 'name_db2': name_db2_h,
                 'proj_db2': proj_db2_h, 'act_db2': act_db2_h, 'name_dst': name_dst_h, 'proj_dst': proj_dst_h,
                 'act_dst': act_dst_h, 'name_k': name_k_h, 'proj_k': proj_k_h, 'act_k': act_k_h}, ignore_index=True)

        if row['matchupPeriodId'] == week and not 'away' in row:
            team_id_h = row['home']['teamId']
            team_abbrev_h = team_info_df[team_info_df['id'] == row['home']['teamId']]['abbrev'].values.item()
            team_location_h = team_info_df[team_info_df['id'] == row['home']['teamId']]['location'].values.item()
            team_nickname_h = team_info_df[team_info_df['id'] == row['home']['teamId']]['nickname'].values.item()
            name_qb_h, proj_qb_h, act_qb_h = split_positions(extract_position_data(row, 'home', 0), 1)
            name_rb1_h, proj_rb1_h, act_rb1_h, name_rb2_h, proj_rb2_h, act_rb2_h = split_positions(
                extract_position_data(row, 'home', 2), 2)
            name_wr1_h, proj_wr1_h, act_wr1_h, name_wr2_h, proj_wr2_h, act_wr2_h = split_positions(
                extract_position_data(row, 'home', 4), 2)
            name_te_h, proj_te_h, act_te_h = split_positions(extract_position_data(row, 'home', 6), 1)
            name_flex_h, proj_flex_h, act_flex_h = split_positions(extract_position_data(row, 'home', 23), 1)
            name_lb1_h, proj_lb1_h, act_lb1_h, name_lb2_h, proj_lb2_h, act_lb2_h = split_positions(
                extract_position_data(row, 'home', 10), 2)
            name_dl1_h, proj_dl1_h, act_dl1_h, name_dl2_h, proj_dl2_h, act_dl2_h = split_positions(
                extract_position_data(row, 'home', 11), 2)
            name_db1_h, proj_db1_h, act_db1_h, name_db2_h, proj_db2_h, act_db2_h = split_positions(
                extract_position_data(row, 'home', 14), 2)
            name_dst_h, proj_dst_h, act_dst_h = split_positions(extract_position_data(row, 'home', 16), 1)
            name_k_h, proj_k_h, act_k_h = split_positions(extract_position_data(row, 'home', 17), 1)

            main_df = main_df.append(
                {'team_id': team_id_h, 'team_abbrev': team_abbrev_h, 'team_location': team_location_h,
                 'team_nickname': team_nickname_h, 'week': week, 'playoffs?!': row['playoffTierType'],
                 'opp': 'BYE',
                 'name_qb': name_qb_h, 'proj_qb': proj_qb_h, 'act_qb': act_qb_h, 'name_rb1': name_rb1_h,
                 'proj_rb1': proj_rb1_h, 'act_rb1': act_rb1_h, 'name_rb2': name_rb2_h,
                 'proj_rb2': proj_rb2_h, 'act_rb2': act_rb2_h, 'name_wr1': name_wr1_h, 'proj_wr1': proj_wr1_h,
                 'act_wr1': act_wr1_h, 'name_wr2': name_wr2_h, 'proj_wr2': proj_wr2_h,
                 'act_wr2': act_wr2_h, 'name_te': name_te_h, 'proj_te': proj_te_h, 'act_te': act_te_h,
                 'name_flex': name_flex_h, 'proj_flex': proj_flex_h, 'act_flex': act_flex_h,
                 'name_dl1': name_dl1_h, 'proj_dl1': proj_dl1_h, 'act_dl1': act_dl1_h, 'name_dl2': name_dl2_h,
                 'proj_dl2': proj_dl2_h, 'act_dl2': act_dl2_h, 'name_lb1': name_lb1_h, 'proj_lb1': proj_lb1_h,
                 'act_lb1': act_lb1_h, 'name_lb2': name_lb2_h, 'proj_lb2': proj_lb2_h, 'act_lb2': act_lb2_h,
                 'name_db1': name_db1_h, 'proj_db1': proj_db1_h, 'act_db1': act_db1_h, 'name_db2': name_db2_h,
                 'proj_db2': proj_db2_h, 'act_db2': act_db2_h, 'name_dst': name_dst_h, 'proj_dst': proj_dst_h,
                 'act_dst': act_dst_h, 'name_k': name_k_h, 'proj_k': proj_k_h, 'act_k': act_k_a},
                ignore_index=True)

    week = week + 1

with pd.ExcelWriter('output/' + str(year) + '_Data_Dump.xlsx') as writer:
    main_df.to_excel(writer, sheet_name='main')
