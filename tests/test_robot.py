import json
import pytest
from robots import robot_commands, robots

TEST_FILE_LOC = "tests/"

def test_update_robot_turn_left():
    initial_robot = robots.Robot("north", 0, 0)
    updated_robot = robot_commands.update_robot(initial_robot, "turn-left", {"x": 10, "y": 10})
    assert updated_robot.bearing == "west"

def test_update_robot_turn_right():
    initial_robot = robots.Robot("north", 0, 0)
    updated_robot = robot_commands.update_robot(initial_robot, "turn-right", {"x": 10, "y": 10})
    assert updated_robot.bearing == "east"

def test_update_robot_move_forward():
    initial_robot = robots.Robot("north", 0, 0)
    updated_robot = robot_commands.update_robot(initial_robot, "move-forward", {"x": 10, "y": 10})
    assert updated_robot.x == 0
    assert updated_robot.y == 1

def test_load_commands():
    commands = [
        '{"type": "asteroid", "size": {"x": 10, "y": 10}}\n',
        '{"type": "new-robot", "bearing": "north", "position": {"x": 0, "y": 0}}\n',
        '{"type": "move", "movement": "move-forward"}\n',
    ]
    with open(f"{TEST_FILE_LOC}/test_instructions.txt", mode="w", encoding="utf-8") as test_file:
        test_file.writelines(commands)

    test_robots = list(robot_commands.load_commands(f"{TEST_FILE_LOC}/test_instructions.txt"))
    assert len(test_robots) == 1
    assert test_robots[0].bearing == "north"
    assert test_robots[0].x == 0
    assert test_robots[0].y == 1

def test_update_robot_move_forward_bounds():
    initial_robot = robots.Robot("north", 10, 10)  # Near the edge of a 10x10 asteroid.
    updated_robot = robot_commands.update_robot(initial_robot, "move-forward", {"x": 10, "y": 10})
    assert updated_robot.x == 10  # Should not exceed the asteroid's bounds.
    assert updated_robot.y == 10

def test_update_robot_missing_asteroid_data():
    initial_robot = robots.Robot("north", 0, 0)
    with pytest.raises(KeyError):
        robot_commands.update_robot(initial_robot, "move-forward", {})

def test_load_commands_invalid_json():
    commands = [
        '{"type": "asteroid", "size": {"x": 5, "y": 5}}\n',
        '{"type": "new-robot", "bearing": "south", "position": {"x": 1, "y": 1}}\n',
        '{"type": "invalid-json, "bearing": "east", "position": {"x": 2, "y": 2}\n',  # Invalid JSON
    ]
    with open("tests/test_instructions_invalid.txt", mode="w", encoding="utf-8") as test_file:
        test_file.writelines(commands)
    with pytest.raises(json.decoder.JSONDecodeError):
        list(robot_commands.load_commands(f"{TEST_FILE_LOC}/test_instructions_invalid.txt"))

def test_load_commands_multiple_robots():
    commands = [
        '{"type": "asteroid", "size": {"x": 5, "y": 5}}\n',
        '{"type": "new-robot", "bearing": "north", "position": {"x": 0, "y": 0}}\n',
        '{"type": "move", "movement": "move-forward"}\n',
        '{"type": "new-robot", "bearing": "east", "position": {"x": 1, "y": 1}}\n',
        '{"type": "move", "movement": "move-forward"}\n',
    ]
    with open("tests/test_instructions_multiple.txt", mode="w", encoding="utf-8") as test_file:
        test_file.writelines(commands)
    test_robots = list(robot_commands.load_commands(f"{TEST_FILE_LOC}/test_instructions_multiple.txt"))
    assert len(test_robots) == 2  # Two robots in the input file.

if __name__ == "__main__":
    pytest.main()
    