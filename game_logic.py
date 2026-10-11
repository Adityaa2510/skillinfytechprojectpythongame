import random


def move_snake(snake, direction, grow=False):
    dx, dy = direction
    head = (snake[0][0] + dx, snake[0][1] + dy)
    body = snake if grow else snake[:-1]
    return [head] + body


def has_collision(snake, width, height):
    x, y = snake[0]
    wall_collision = x < 0 or y < 0 or x >= width or y >= height
    self_collision = snake[0] in snake[1:]
    return wall_collision or self_collision


def spawn_food(snake, width, height, rng=None):
    rng = rng or random
    occupied = set(snake)
    available = [
        (x, y)
        for x in range(width)
        for y in range(height)
        if (x, y) not in occupied
    ]
    return rng.choice(available) if available else None
