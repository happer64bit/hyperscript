# Hyperscript

**Hyperscript** is a tool for testing HTTP requests with flexible configuration and validation.

<a href="https://www.producthunt.com/posts/hyperscript?embed=true&utm_source=badge-featured&utm_medium=badge&utm_souce=badge-hyperscript" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=476454&theme=light" alt="HyperScript - Powerful&#0032;HTTP&#0032;Request&#0032;Tester&#0032;⌚ | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>

## Features

- **HTTP Methods**: Test GET, POST, PUT, and DELETE requests.
- **Validation**: Check status codes, content types, and body content.
- **Conditions**: Validate if responses contain specific values, match exact values, or if numeric fields meet criteria (less than, greater than, equal to).
- **Concurrency**: Run tests in parallel to improve efficiency.
- **Reporting**: Detailed success and failure messages, with optional verbose output.

## Installation

Install with pip:

```bash
pip install hyperscript-cli
```

## Configuration

Create a YAML file (`config.yaml`) for your tests. Example:

```yaml
global:
  url: https://freetestapi.com

run:
  - name: Get All Cars
    path: /api/v1/cars
    expect:
      contentType: application/json
      status: 200

  - name: Get Single Car
    path: /api/v1/cars/1
    expect:
      contentType: application/json
      status:
        - value: 200
        - value: 201
      contains:
        id: 1
      equalTo:
        make: Toyota
        model: Corolla
      lessThan:
        price: 30000
      greaterThan:
        year: 2010
      body:
        make: Toyota
        model: Corolla
        color: Silver
```

### Environment Variables

You can use environment variables in your configuration. For example, use `{{VARIABLE_NAME}}` syntax to reference environment variables.

Set environment variables before running your tests:

```bash
export BASE_URL=https://freetestapi.com
export CAR_ID=1
```

Update `config.yaml` to use these variables:

```yaml
global:
  url: "{{BASE_URL}}"

run:
  - name: Get Single Car
    path: /api/v1/cars/{{CAR_ID}}
    expect:
      contentType: application/json
      status:
        - value: 200
        - value: 201
```

## Usage

Run tests with the `hyperscript` command:

```bash
hyperscript path/to/config.yaml
```

### Command-Line Arguments

- `config_file`: Path to the YAML configuration file. Default is `hypertest.yml`.

  Example:
  ```bash
  hyperscript path/to/config.yaml
  ```

- `--skip-error`: Continue with the next test on error.

  Example:
  ```bash
  hyperscript path/to/config.yaml --skip-error
  ```

- `--verbose`: Enable detailed logging for more comprehensive output.

  Example:
  ```bash
  hyperscript path/to/config.yaml --verbose
  ```

- `--concurrency`: Set the number of concurrent tests to run. If not specified, tests will run sequentially.

  Example:
  ```bash
  hyperscript path/to/config.yaml --concurrency 5
  ```

## Contributing

Fork the repository and submit a pull request with your changes.

## License

MIT License. See the [LICENSE](LICENSE) file.

## Contact

For questions, email [happer64bit@gmail.com](mailto:happer64bit@gmail.com).
