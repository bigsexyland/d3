#!/usr/bin/env python
# D3 Paragon Calculator
# Get total paragon by combining seasonal + non seasonal paragon
# or seasonal paragon needed to reach non seasonal goal
# It doesn't matter which is which, they are valued equally
# Or find half-way point to arbitrary paragon

import sys
import argparse
from paragon_calc import ParagonCalc


def main():
    parser = argparse.ArgumentParser(description='Calculate Paragons')
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument('--total', '-t', action='store_true',
                         help='Total Non Seasonal paragon (requires --seasonal <p> --non_seasonal <p>)')
    actions.add_argument('--goal', '-g', type=int,
                         help='Goal Non Seasonal paragon (requires --non_seasonal)')
    parser.add_argument('--seasonal', '-s', type=int,
                        help='Seasonal paragon (integer)')
    parser.add_argument('--non_seasonal', '-n', type=int,
                        help='Non Seasonal paragon (integer)')
    parser.add_argument('--halfway', '-a', type=int,
                        help='Paragon to find half-way point (integer)')
    parser.add_argument('--paragon_file', '-p', default='p10000.csv',
                        help='File with paragon definitions, csv')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Print verbose output')

    args = parser.parse_args()

    if args.total and not (args.seasonal and args.non_seasonal):
        parser.print_help()
        print('\nYou must specify: -s <p> -n <p> with -t\n')
        sys.exit(1)

    if args.goal and not args.non_seasonal:
        parser.print_help()
        print('\nYou must specify: -n <p> with -g\n')
        sys.exit(1)

    if not (args.total or args.goal or args.halfway):
        parser.print_help()
        print('\nYou must specify either: -t or -g or -a\n')
        sys.exit(1)

    paragons = ParagonCalc(
        paragon_seasonal=args.seasonal,
        paragon_non_seasonal=args.non_seasonal,
        paragon_goal=args.goal,
        paragon_halfway=args.halfway,
        paragon_file=args.paragon_file,
        verbose=args.verbose,
    )
    if args.total:
        output = paragons.get_paragon_total()
    elif args.goal:
        output = paragons.get_paragon_goal()
    elif args.halfway:
        output = paragons.get_paragon_halfway()
    print output
    sys.exit(0)


if __name__ == '__main__':
    sys.exit(main())
