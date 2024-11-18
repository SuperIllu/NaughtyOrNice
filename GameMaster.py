import importlib
import itertools
import os
import yaml
from typing import List, Tuple, Optional
import logging

from base.GameManager import GameManager
from base.PlayerBase import PlayerBase


class PlayerEntry:
    def __init__(self, name: str, team_name: str, player: type):
        self.Name = name
        self.Team_name = team_name
        self.Player = player

    def __str__(self):
        return f"{self.Name}|{self.Team_name}"

    def __repr__(self):
        return self.__str__()


def find_yaml_files(folder_path: str, file_name: str) -> List[str]:
    """
    Finds all YAML files with a specific name in the first level of subfolders of a given folder path.

    Parameters:
        folder_path (str): The path to the main folder to search in.
        file_name (str): The name of the YAML file to search for (e.g., "config.yaml").

    Returns:
        List[str]: A list of file paths matching the specified name within the first hierarchy of subfolders.
    """
    yaml_files = []
    # Loop over each item in the first level of the given folder
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        # Check if the item is a directory
        if os.path.isdir(subfolder_path):
            target_file = os.path.join(subfolder_path, file_name)
            # Check if the target YAML file exists in the subfolder
            if os.path.isfile(target_file):
                yaml_files.append(target_file)

    return yaml_files


def find_dedicated_yamls():
    return find_yaml_files("CustomPlayers", "register.yaml")


def parse_yaml_file(yaml_file_path):
    try:
        logging.debug(f"Parsing {yaml_file_path}")
        with open(yaml_file_path, "r") as yaml_file:
            file_content = yaml.safe_load(yaml_file)

            entries_raw = file_content["entries"]
            entries = []

            for entry in entries_raw:
                class_name = entry["name"]
                file_name = entry["file"]

                entries.append((file_name, class_name))

        return entries
    except BaseException:
        logging.error(f"parsing {yaml_file_path} failed")


def parse_player_class(yaml_file_path, entry) -> Optional[PlayerEntry]:
    try:
        logging.debug(f"parsing {entry} in {yaml_file_path}")
        path_name = os.path.dirname(yaml_file_path)
        team_name = os.path.split(path_name)[-1]

        file_path = os.path.join(path_name, entry[0])
        module_name = os.path.splitext(file_path)[0].replace(os.path.sep, ".")
        logging.debug(f"module name: {module_name} for team {team_name}")
    except BaseException:
        logging.error(f"Could not parse {entry} @ {yaml_file_path}")
        return None

    try:
        imported_module = importlib.import_module(module_name)
        player_class_name = entry[1]
        if player_class_name not in dir(imported_module):
            logging.error(f"{player_class_name} not found in {module_name}")
            return None
        player_class = getattr(imported_module, player_class_name)
    except BaseException:
        logging.error(f"Could not load {module_name} in {yaml_file_path} for {entry}")
        return None

    logging.debug(f"found {player_class_name}|{team_name} -> {player_class}")
    return PlayerEntry(player_class_name, team_name, player_class)



def get_players():
    yaml_files = find_dedicated_yamls()
    logging.info(f"found registrations: {yaml_files}")
    valid_players = []
    for yaml_file in yaml_files:
        player_entries = parse_yaml_file(yaml_file)
        logging.debug(f"File content: {yaml_file} -> {player_entries}")

        for entry in player_entries:
            player_info = parse_player_class(yaml_file, entry)
            if player_info is not None:
                valid_players.append(player_info)
    logging.info(f"valid entries: {valid_players}")
    return valid_players


def get_player_combinations(valid_players):
    player_combinations = list(itertools.combinations(valid_players, 2))
    skip_internal_games = False
    if skip_internal_games:
        def entry_good(entry):
            return entry[0].Team_name != entry[1].Team_name
        valid_combinations = [entry for entry in player_combinations if entry_good(entry)]
        print(f"reduces to {valid_combinations}")
    logging.info(f"combinations: {player_combinations}")
    return player_combinations


def run_combinations(player_list, player_combinations):
    player_points = {key.Player: 0 for key in player_list}
    player_names = {key.Player: key.Name for key in player_list}

    rounds: int = 5

    for i in range(rounds):
        for combination in player_combinations:
            player1_type = combination[0].Player
            player2_type = combination[1].Player

            try:
                game = GameManager(player1_type, player2_type)
                game.play_game()
                points = game.accum_points()
                logging.info(f"game: {points}")
                for player, points in points.items():
                    player_points[player] += points
            except BaseException:
                logging.error(f"Game failed between {player1_type}|{player2_type}")

    try:
        shortened = {player_names[key]: value for key, value in player_points.items()}
        paired = [(key, value) for key, value in shortened.items()]
        paired.sort(key=lambda x: -x[1])
        logging.debug(f"total points: {paired}")

        logging.info("-"*50)
        for result in paired:
            logging.info(f"{result[0].ljust(25)}->\t{str(result[1]).rjust(10)}")
        logging.info("="*50)
    except BaseException as e:
        logging.error("Failed to parse game data")
        raise e


def main():
    if False:
        # just to see the messages
        logging.error("error")
        logging.warning("warning")
        logging.info("info")
        logging.debug("debug")

    valid_players = get_players()

    player_combinations = get_player_combinations(valid_players)

    run_combinations(valid_players, player_combinations)



if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    main()
