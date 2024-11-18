from CustomPlayers.Player1.NaughtyAfterTwo import NaughtyAfterTwo
from ExamplePlayers.Alternating import Alternating
from ExamplePlayers.AlwaysNice import AlwaysNice
from ExamplePlayers.AlwaysNaughty import AlwaysNaughty
from ExamplePlayers.AlwaysRandom import AlwaysRandom
from ExamplePlayers.CopyCat import CopyCat
from base.GameManager import GameManager


player1Type = NaughtyAfterTwo
player2Type = Alternating


def main():
    print("Test run")
    manager = GameManager(player1Type, player2Type)
    manager.play_game()
    results = manager.accum_points()
    print(results)
    print(f"total: {sum(results.values())}")


if __name__ =="__main__":
    main()

