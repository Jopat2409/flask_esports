
XPATH_VLR_PLAYER_FULLNAME = "/html/body/div[5]/div[1]/div/div[1]/div[1]/div[2]/div[1]/h2"
XPATH_VLR_PLAYER_ALIAS = "/html/body/div[5]/div[1]/div/div[1]/div[1]/div[2]/div[1]/h1"
XPATH_VLR_PLAYER_CURRENT_TEAM = "/html/body/div[5]/div[1]/div/div[2]/div[1]/div[4]/a"
XPATH_VLR_PLAYER_AVATAR = "/html/body/div[5]/div[1]/div/div[1]/div[1]/div[1]/div/img"
XPATH_VLR_PLAYER_PREVIOUS_TEAMS = "(//div[contains(@class, 'wf-card')])[4]//a"


XPATH_VLR_MATCH_PLAYER_STATS = """//div[contains(@class, 'vm-stats-game ') and contains(@data-game-id, "all")]//tr//span[contains(@class, "mod-both")]"""
XPATH_VLR_MATCH_PLAYERS = """//div[contains(@class, 'vm-stats-game ') and contains(@data-game-id, "all")]//td[contains(@class, "mod-player")]//a"""
XPATH_VLR_MATCH_SCORES = "/html/body/div[5]/div[1]/div[3]/div[1]/div[2]/div/div[2]/div[1]/span"
XPATH_VLR_MATCH_NAME = "/html/body/div[5]/div[1]/div[3]/div[1]/div[1]/div[1]/a/div/div[2]"
XPATH_VLR_MATCH_EVENT_HREF = "/html/body/div[5]/div[1]/div[3]/div[1]/div[1]/div[1]/a"
XPATH_VLR_MATCH_TEAMS = "/html/body/div[5]/div[1]/div[3]/div[1]/div[2]/a"
XPATH_VLR_MATCH_TIMESTAMP = "//div[contains(@class, 'moment-tz-convert')]"

XPATH_VLR_TEAM_NAME= "//div[contains(@class, 'team-header-name')]//h1[contains(@class, 'wf-title')]"
XPATH_VLR_TEAM_TAG= "//div[contains(@class, 'team-header-name')]//h2[contains(@class, 'wf-title')]"
XPATH_VLR_TEAM_PLAYERS = "//div[contains(@class, 'team-roster-item')]//a"
XPATH_VLR_TEAM_REGION = "//div[contains(@class, 'team-header-country')]"
XPATH_VLR_TEAM_LOGO = "//div[contains(@class, 'team-header-logo')]//img"
