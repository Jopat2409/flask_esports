from esports_api.utils.scraping import XpathParser, get_url_segment, epoch_from_timestamp
from esports_api.utils.game_router import GameRouter

from esports_api.app.models import Player, SourceId, Match
from esports_api.app.models.team import Role, Team
from esports_api.app.valorant import constants


class ValorantRoutes(GameRouter):

    PAGE_SIZE = 20
    VLR_PAGE_SIZE = 12

    def _parse_player_fullname(name: str) -> tuple[str, str]:
        """Parses a player's full name into a forename and surname

        Args:
            name (str): The full name scraped from the website

        Returns:
            tuple[str, str]: forename, surname
        """

        # retards passing nothing into this method get nothing in return :D
        if not name:
            return None, None

        # Split into individual names and return the first / last name in the list
        given_names = name.split(" ")
        return given_names[0].strip(), (given_names[-1].strip() if len(given_names) > 1 else None)

    def _parse_stat(stat_td, type_, percentage=False):
        """Parses a single stat pulled from a vlr match page

        Args:
            stat_td (_type_): the table d thing of the stat
            type_ (_type_): the type to cast the stat to (usually float, int etc.)
            percentage (bool, optional): is the stat a percentage. Defaults to False.

        Returns:
            _type_: _description_
        """
        txt = stat_td.text.strip()

        # \xa0 is sometimes used to represent a blank space in vlr. Don't know why :(
        if not txt or txt == '\xa0':
            return None

        # Parse percentage or just return the stat
        return type_(txt.replace("%", '').strip() if percentage else txt)

    def _parse_player_stats(data: list) -> dict:
        """Given the data pulled directly from the match vlr page, parses each important stat line for the specific
        player

        Args:
            data (list): The data pulled from the vlr match page

        Returns:
            dict: a dictionary containing all of the present stats
        """
        return {
            "rating": ValorantRoutes._parse_stat(data[0], float),
            "ACS": ValorantRoutes._parse_stat(data[1], int),
            "kills": ValorantRoutes._parse_stat(data[2], int),
            "deaths": ValorantRoutes._parse_stat(data[3], int),
            "assists": ValorantRoutes._parse_stat(data[4], int),
            "KAST": ValorantRoutes._parse_stat(data[6], int, percentage=True),
            "ADR": ValorantRoutes._parse_stat(data[7], int),
            "HS": ValorantRoutes._parse_stat(data[8], int, percentage=True),
            "FK": ValorantRoutes._parse_stat(data[9], int),
            "FD": ValorantRoutes._parse_stat(data[10], int)
        }

    def _parse_player_card(card) -> dict:
        role = card.xpath(".//div[contains(@class, 'team-roster-item-name-role')]")
        return {
            "id": get_url_segment(card.get("href", ""), 2),
            "name": get_url_segment(card.get("href", ""), 3),
            "role": role[0].text.strip() if role else "player"

        }

    def get_player(player_id) -> Player | None:

        # Create scraper and return None if the page is not found
        parser = XpathParser(f"https://www.vlr.gg/player/{player_id}/?timespan=30d")
        if parser.content is None:
            return None

        # Get the full name text
        full_name = parser.get_text(constants.XPATH_VLR_PLAYER_FULLNAME)
        forename, surname = ValorantRoutes._parse_player_fullname(full_name)

        # Parse other metadata
        avatar = parser.get_img(constants.XPATH_VLR_PLAYER_AVATAR)
        alias = parser.get_text(constants.XPATH_VLR_PLAYER_ALIAS)
        current_team = parser.get_href(constants.XPATH_VLR_PLAYER_CURRENT_TEAM)
        current_team_id = get_url_segment(current_team, 2, int) if current_team else None

        # Construct player and return
        return Player(
            SourceId("valorant", player_id),
            alias,
            forename,
            surname,
            avatar,
            current_team_id
        )

    def get_player_matches(player_id: int, page: int) -> list[Match]:

        MATCHES_PER_VLR = 50
        to_scrape = []

        start_match = (page-1) * 12
        vlr_page = start_match // MATCHES_PER_VLR
        while len(to_scrape[(start_match-1):]) < 12 and vlr_page != -1:
            vlr_page += 1
            parser = XpathParser(f"https://www.vlr.gg/player/matches/{player_id}?page={vlr_page}")
            match_ids = list(map(lambda x: int(x.get("href").strip().split("/")[1]), parser.get_elements("//div[contains(@class, ' mod-dark')]//a")))
            to_scrape += match_ids
            if not match_ids:
                vlr_page = -1


        matches = [ValorantRoutes.get_match(match) for match in to_scrape[start_match:start_match+12]]
        return matches

    def get_player_teams(player_id: int) -> list:

        parser = XpathParser(f"https://www.vlr.gg/player/{player_id}/?timespan=30d")
        if parser.content is None:
            return None

        current_team = parser.get_href(constants.XPATH_VLR_PLAYER_CURRENT_TEAM)
        previous_teams = parser.get_elements(constants.XPATH_VLR_PLAYER_PREVIOUS_TEAMS, 'href')

        return [ValorantRoutes.get_team(get_url_segment(team, 2)) for team in [current_team, *previous_teams]]

    def get_match(match_id: int):

        parser = XpathParser(f"https://www.vlr.gg/{match_id}")
        if parser.content is None:
            return None

        # forgor why i do this
        match_name = ' '.join(parser.get_text(constants.XPATH_VLR_MATCH_NAME).split())
        match_epoch = epoch_from_timestamp(f"{parser.get_element(constants.XPATH_VLR_MATCH_TIMESTAMP).get('data-utc-ts', '')} -0400", "%Y-%m-%d %H:%M:%S %z")

        # Get the team IDs of the teams playing in the match
        teams = parser.get_elements(constants.XPATH_VLR_MATCH_TEAMS, attr='href')
        home_team, away_team = get_url_segment(teams[0], 2, int), get_url_segment(teams[1], 2, int)

        # Get the overall map score of each of the teams playing in the match
        scores = parser.get_elements(constants.XPATH_VLR_MATCH_SCORES)
        home_score, away_score = int(scores[0].text), int(scores[2].text)

        # Get the event ID of the match
        event_id = get_url_segment(parser.get_href(constants.XPATH_VLR_MATCH_EVENT_HREF), 2, int)

        # Get the player IDs and statistics for the match
        player_ids = [get_url_segment(player, 2, int) for player in parser.get_elements(constants.XPATH_VLR_MATCH_PLAYERS, attr="href")]
        player_stats_raw = parser.get_elements(constants.XPATH_VLR_MATCH_PLAYER_STATS)
        player_stats = {player_ids[int(i/12)]: ValorantRoutes._parse_player_stats(player_stats_raw[i:i+12]) for i in range(0, len(player_stats_raw), 12)}

        return Match(
            SourceId("valorant", match_id),
            event_id,
            match_name,
            home_team,
            away_team,
            home_score,
            away_score,
            match_epoch,
            player_stats
        )


    def get_team_matches(team_id: int, page: int):

        MATCHES_PER_VLR = 50
        to_scrape = []

        start_match = (page-1) * 12
        vlr_page = start_match // MATCHES_PER_VLR
        while len(to_scrape[(start_match-1):]) < 12 and vlr_page != -1:
            vlr_page += 1
            parser = XpathParser(f"https://www.vlr.gg/team/matches/{team_id}/?group=completed&page={vlr_page}")
            match_ids = list(map(lambda x: int(x.get("href").strip().split("/")[1]), parser.get_elements("//div[contains(@class, ' mod-dark')]//a")))
            to_scrape += match_ids
            if not match_ids:
                vlr_page = -1


        matches = [ValorantRoutes.get_match(match) for match in to_scrape[start_match:start_match+12]]
        return matches


    def get_team(team_id: int) -> None:

        parser = XpathParser(f"https://www.vlr.gg/team/{team_id}")

        if parser.content is None:
            return None

        team_name = parser.get_text(constants.XPATH_VLR_TEAM_NAME)
        team_tag = parser.get_text(constants.XPATH_VLR_TEAM_TAG)
        team_region = parser.get_element(constants.XPATH_VLR_TEAM_REGION).text_content().strip()
        team_logo = parser.get_img(constants.XPATH_VLR_TEAM_LOGO)

        player_divs = parser.get_elements(constants.XPATH_VLR_TEAM_PLAYERS)
        current_roster = [ValorantRoutes._parse_player_card(player) for player in player_divs]

        team = Team(SourceId("valorant", team_id), team_name, team_tag, team_logo, team_region)
        for player in current_roster:
            if player["role"].lower() in ["player", "sub", "inactive"]:
                team.add_player(player["id"], player["name"], player["role"].lower() == "sub", player["role"].lower() != "inactive")
            else:
                team.add_staff(player["id"], player["name"], Role[player["role"].upper().replace(" ", "_")])

        return team
