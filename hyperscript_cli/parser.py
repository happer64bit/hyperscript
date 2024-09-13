import threading
from typing import Dict, Any, Union, List
from colorama import Fore, init
import requests
import yaml
import os
import re

init(autoreset=True)

class Parser:
    def __init__(self, config: Dict[str, Any], skip_error: bool, verbose: bool = False, concurrency: int = None) -> None:
        self.config = self._process_env_vars(config)
        self.skip_error = skip_error
        self.verbose = verbose
        self.success_count = 0
        self.fail_count = 0
        self.concurrency = concurrency

    def run_test(self) -> None:
        # Provide default values for retries and timeout
        global_url = self.config['global']['url']
        global_request_retries = self.config['global'].get('retries', 0)  # Default to 0 retries
        global_request_timeout = self.config['global'].get('timeout', None)  # Default to None for no timeout
        global_headers = self.config['global'].get('headers', {})
        global_cookies = self.config['global'].get('cookies', {})

        print(f"\n{Fore.CYAN}Running tests...\n{Fore.RESET}")

        # Run tests concurrently if concurrency is specified
        if self.concurrency:
            threads = []
            for run in self.config['run']:
                t = threading.Thread(target=self._run_single_test, args=(run, global_url, global_headers, global_cookies, global_request_retries, global_request_timeout))
                threads.append(t)
                t.start()

            # Wait for all threads to complete
            for t in threads:
                t.join()
        else:
            for run in self.config['run']:
                self._run_single_test(run, global_url, global_headers, global_cookies, global_request_retries, global_request_timeout)

    def _run_single_test(self, run: Dict[str, Any], global_url: str, global_headers: Dict[str, Any], global_cookies: Dict[str, Any], retries: int, timeout: Union[None, int]) -> None:
        name = run['name']
        path = run['path']
        url = global_url + path
        method = run.get('method', 'GET').upper()
        headers = {**global_headers, **run.get('headers', {})}
        cookies = {**global_cookies, **run.get('cookies', {})}
        data = run.get('body', {})

        for attempt in range(retries + 1):
            try:
                response = requests.request(method, url, headers=headers, cookies=cookies, json=data, timeout=timeout)
                self._check_response(response, run['expect'], name)
                break  # If request is successful, break out of retry loop
            except requests.RequestException as e:
                if attempt < retries:
                    if self.verbose:
                        print(f"Attempt {attempt + 1} failed. Retrying...")
                    continue  # Retry on failure
                self._handle_error(f"{str(e)}", name)
            except Exception as e:
                self._handle_error(f"Unexpected error occurred: {str(e)}", name)
                break

    def _check_response(self, response: requests.Response, expect: Dict[str, Any], name: str) -> None:
        try:
            expected_status = expect.get('status')
            expected_content_type = expect.get('contentType')
            expected_body = expect.get('body')
            contains = expect.get('contains')
            less_than = expect.get('lessThan')
            greater_than = expect.get('greaterThan')
            equal_to = expect.get('equalTo')

            # Check response status code
            if isinstance(expected_status, list):
                if response.status_code not in [status['value'] for status in expected_status]:
                    self._handle_error(f"STATUS CODE {response.status_code} DOES NOT MATCH EXPECTED", name)
                    return
            elif response.status_code != expected_status:
                self._handle_error(f"STATUS CODE {response.status_code} DOES NOT MATCH EXPECTED: {expected_status}", name)
                return

            # Check content type
            if response.headers.get('Content-Type') != expected_content_type:
                self._handle_error(f"CONTENT TYPE {response.headers.get('Content-Type')} DOES NOT MATCH EXPECTED: {expected_content_type}", name)
                return

            response_json = response.json()

            # Check body if expected_body is specified
            if expected_body and not self._compare_nested(response_json, expected_body):
                self._handle_error("RESPONSE BODY DOES NOT MATCH EXPECTED", name)
                return

            # Check if response contains specified keys/values
            if contains and not self._compare_contains(response_json, contains):
                self._handle_error(f"RESPONSE DOES NOT CONTAIN EXPECTED VALUES", name)
                return

            # Check if response values are less than expected values
            if less_than and not self._compare_less_than(response_json, less_than):
                self._handle_error(f"RESPONSE VALUES ARE NOT LESS THAN EXPECTED", name)
                return

            # Check if response values are greater than expected values
            if greater_than and not self._compare_greater_than(response_json, greater_than):
                self._handle_error(f"RESPONSE VALUES ARE NOT GREATER THAN EXPECTED", name)
                return

            # Check if response values are equal to expected values
            if equal_to and not self._compare_equal_to(response_json, equal_to):
                self._handle_error(f"RESPONSE VALUES DO NOT MATCH EXPECTED", name)
                return

            self._log_success(name)
        except Exception as e:
            self._handle_error(f"ERROR DURING RESPONSE VALIDATION: {str(e)}", name)

    def _compare_nested(self, actual: Any, expected: Any) -> bool:
        if isinstance(expected, dict):
            for key, value in expected.items():
                if key not in actual or not self._compare_nested(actual[key], value):
                    return False
            return True
        return actual == expected

    def _compare_contains(self, actual: Any, contains: Dict[str, Any]) -> bool:
        for key, value in contains.items():
            if key not in actual or actual[key] != value:
                return False
        return True

    def _compare_less_than(self, actual: Any, less_than: Dict[str, Any]) -> bool:
        for key, value in less_than.items():
            if key not in actual or not actual[key] < value:
                return False
        return True

    def _compare_greater_than(self, actual: Any, greater_than: Dict[str, Any]) -> bool:
        for key, value in greater_than.items():
            if key not in actual or not actual[key] > value:
                return False
        return True

    def _compare_equal_to(self, actual: Any, equal_to: Dict[str, Any]) -> bool:
        for key, value in equal_to.items():
            if key not in actual or actual[key] != value:
                return False
        return True

    def _handle_error(self, message: str, name: str) -> None:
        simplified_message = message
        if 'Max retries exceeded' in message:
            simplified_message = "Unable to connect to the server. Please check if the server is running and reachable."
        elif 'Failed to establish a new connection' in message:
            simplified_message = "No connection could be made to the server. Ensure the server is active and accessible."

        error_message = f"{Fore.RED}✖ FAILED: {name}{Fore.RESET}"
        detailed_message = f"{Fore.RED}{simplified_message}{Fore.RESET}"
        
        print(error_message)
        if self.verbose:
            print(detailed_message)
        
        self.fail_count += 1
        if not self.skip_error:
            raise RuntimeError(simplified_message)

    def _log_success(self, name: str) -> None:
        success_message = f"{Fore.GREEN}✔ SUCCESS: {name}{Fore.RESET}"
        print(success_message)
        self.success_count += 1

    def show_summary(self) -> None:
        total_tests = self.success_count + self.fail_count
        print(f"\n{Fore.GREEN}SUCCESS: {self.success_count}{Fore.RESET}, "
              f"{Fore.RED}FAILURE: {self.fail_count}{Fore.RESET}, "
              f"{Fore.WHITE}TOTAL: {total_tests}{Fore.RESET}\n")

    def _process_env_vars(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Replace placeholders in the config with environment variable values."""
        def replace_env_vars(value: Any) -> Any:
            if isinstance(value, str):
                return re.sub(r'\{\{(\w+)\}\}', lambda match: os.getenv(match.group(1), match.group(0)), value)
            elif isinstance(value, dict):
                return {k: replace_env_vars(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [replace_env_vars(v) for v in value]
            return value

        return replace_env_vars(config)

def parse_config(config_file: str) -> Dict[str, Any]:
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except yaml.YAMLError as e:
        print(f"{Fore.RED}FAILED TO PARSE YAML FILE: {e}{Fore.RESET}")
        raise
    except Exception as e:
        print(f"{Fore.RED}UNEXPECTED ERROR: {e}{Fore.RESET}")
        raise
