import random
from game_logic import move_snake, has_collision, spawn_food


def test_snake_moves_right():
    snake = [(5, 5), (4, 5), (3, 5)]
    assert move_snake(snake, (1, 0)) == [(6, 5), (5, 5), (4, 5)]


def test_eating_food_grows_snake():
    snake = [(5, 5), (4, 5), (3, 5)]
    assert len(move_snake(snake, (1, 0), grow=True)) == 4


def test_wall_collision():
    snake = [(10, 5), (9, 5), (8, 5)]
    assert has_collision(snake, 10, 10)


def test_self_collision():
    snake = [(2, 2), (2, 3), (1, 3), (1, 2)]
    result = move_snake(snake, (-1, 0), grow=True)
    assert has_collision(result, 10, 10)


def test_food_never_spawns_on_snake():
    snake = [(0, 0), (1, 0)]
    food = spawn_food(snake, 3, 3, rng=random.Random(42))
    assert food not in snake


def test_full_board_has_no_food_space():
    snake = [(x, y) for x in range(2) for y in range(2)]
    assert spawn_food(snake, 2, 2) is None
