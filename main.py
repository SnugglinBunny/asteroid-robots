import argparse
import json
import sys
from app import robots

def format_robot_final_pos(robots_final_pos):
    """Format the final positions of robots for JSON output."""
    return [
        {
            "type": "robot",
            "position": {"x": robot.x, "y": robot.y},
            "bearing": robot.bearing,
        }
        for robot in robots_final_pos
    ]

def parse_arguments():
    """Parse command-line arguments using argparse."""
    parser = argparse.ArgumentParser(description="Simulate robot movements on an asteroid.")
    parser.add_argument(
        "file_name", nargs="?", default="instructions.txt", 
            help="Name of the input file with robot commands."
    )
    return parser.parse_args()

def main():
    try:
        args = parse_arguments()
        robot_commands = robots.load_commands(args.file_name)
        for r in format_robot_final_pos(robot_commands):
            print(json.dumps(r))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
    