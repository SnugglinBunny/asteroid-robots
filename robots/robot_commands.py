import json
from .robots import Robot

# Define movements and outcomes as constants.
MOVEMENTS = {
    "turn-left": {"north": "west", "east": "north", "south": "east", "west":"south",},
    "turn-right": {"north": "east", "east": "south", "south": "west", "west":"north",},
    "move-forward": {"north": (0, 1), "east": (1, 0), "south": (0, -1), "west": (-1, 0)},
}

def update_robot(robot, movement, asteroid_data):
    """Update the robot's position or bearing based on the input movement intention.

    Args:
        robot (Robot): The robot's current state as a namedtuple.
        movement (str): The movement intention ("turn-left", "turn-right", or "move-forward").
        asteroid_data (dict): Size of the asteroid the robot needs to be contained within.

    Returns:
        Robot: A new Robot namedtuple with updated state.
    """
    if movement in ["turn-left", "turn-right"]:
        # Update the robot's bearing based on the chosen movement.
        new_bearing = MOVEMENTS[movement][robot.bearing]
        return Robot(new_bearing, robot.x, robot.y)
    elif movement == "move-forward":
        move_x, move_y = MOVEMENTS[movement][robot.bearing]
        current_x, current_y = robot.x, robot.y
        new_x = current_x + move_x
        new_y = current_y + move_y
        # Clamp robot's position to within the bounds of the asteroid.
        new_pos_x = max(0, min(new_x, asteroid_data["x"]))
        new_pos_y = max(0, min(new_y, asteroid_data["y"]))
        return Robot(robot.bearing, new_pos_x, new_pos_y)

def load_commands(file_name):
    """Load commands from a file and process them line by line.

        Args:
            file_name (str): The name of the file containing robot commands.

        Yields:
            Robot: A Robot namedtuple representing the final state of each robot.
        Raises:
            FileNotFoundError: If the specified file is not found.
            json.JSONDecodeError: If there is an error decoding JSON in the file.
    """
    asteroid_size = {}
    robot = None

    try:
        with open(file_name, mode="r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                try:
                    command = json.loads(line)
                except json.JSONDecodeError as e:
                    # Handle JSON decoding error with a more informative message.
                    raise json.JSONDecodeError(f"Error decoding JSON on line {line_number}: {e}", doc=line, pos=e.pos) from e

                cmd_type = command.get("type")

                if cmd_type == "asteroid":
                    # Store the size of the asteroid for reference.
                    asteroid_size = command.get("size", {})
                elif cmd_type == "new-robot":
                    # Create a new robot based on the command data.
                    if robot:
                        yield robot
                    robot = Robot(command["bearing"], command["position"]["x"], command["position"]["y"])
                elif cmd_type == "move":
                    # Update the robot's state based on the movement command.
                    if robot:
                        robot = update_robot(robot, command["movement"], asteroid_size)

        if robot:
            yield robot

    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_name}") from e