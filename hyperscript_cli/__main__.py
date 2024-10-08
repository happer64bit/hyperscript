import argparse
from hyperscript_cli.parser import parse_config, Parser
from colorama import Fore

def main():
    parser = argparse.ArgumentParser(description="Run tests based on YAML configuration")
    parser.add_argument('config_file', help="Path to the YAML configuration file", default="hypertest.yml")
    parser.add_argument('--skip-error', action='store_true', help="Skip error handling and continue", default=False)
    parser.add_argument('--verbose', action='store_true', help="Enable detailed logging", default=False)
    parser.add_argument('-c', '--concurrency', type=int, help="Number of concurrent threads (default is no concurrency)", default=None)
    args = parser.parse_args()

    try:
        config = parse_config(args.config_file)
        runner = Parser(config, args.skip_error, args.verbose, args.concurrency)
        runner.run_test()
        runner.show_summary()
    except Exception as e:
        print(f"{Fore.RED}ERROR: {e}{Fore.RESET}")
        exit(1)

if __name__ == "__main__":
    main()
