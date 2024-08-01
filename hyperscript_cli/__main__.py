import argparse
from hyperscript.parser import parse_config, TestRunner
from colorama import Fore

def main():
    parser = argparse.ArgumentParser(description="Run tests based on YAML configuration")
    parser.add_argument('config_file', help="Path to the YAML configuration file", default="hypertest.yml")
    parser.add_argument('--skip-error', action='store_true', help="Skip error handling and continue", default=False)
    parser.add_argument('--verbose', action='store_true', help="Enable detailed logging", default=False)
    args = parser.parse_args()

    try:
        config = parse_config(args.config_file)
        runner = TestRunner(config, args.skip_error, args.verbose)
        runner.run_test()
        runner.show_summary()
    except Exception as e:
        print(f"{Fore.RED}ERROR: {e}{Fore.RESET}")
        exit(1)

if __name__ == "__main__":
    main()
