import sys
import argparse
from datetime import datetime

from setup.setup import setup_processes
from generate_outputs.output_generator import outputs_fn


def valid_date(s):
    """Validate and convert input string into a date."""
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Not a valid date: '{s}'. Expected format: YYYY-MM-DD.")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Process set names and a date.")
    parser.add_argument(
        '-s',
        '--set_name',
        metavar='set_name',
        type=str,
        required=True,
        help='The name of the set being computed (string)'
    )
    parser.add_argument(
        '-d',
        '--date',
        type=valid_date,
        required=True,
        help='Date in the format YYYY-MM-DD'
    )
    return parser.parse_args()


def main(
        output_set: list
):
    # Perform setup processes
    setup_processes()

    # Generate outputs
    ret = outputs_fn(output_set=output_set)

    return ret


if __name__ == "__main__":
    # Get arguments
    args = parse_arguments()

    # Print the date
    print(f"Output Set: {args.set_name}")
    print(f"Date: {args.date.strftime('%Y-%m-%d')}")

    # Run main
    ret = main(output_set=args.set_name)

    sys.exit(0 if ret else 1)

