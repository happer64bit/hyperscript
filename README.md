# Hyperscript

**Hyperscript** is a tool for testing HTTP requests with flexible configuration and validation.

## Features

- **HTTP Methods**: Test GET, POST, PUT, and DELETE requests.
- **Validation**: Check status codes, content types, and body content.
- **Conditions**: Validate if responses contain specific values or if numeric fields meet criteria.
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

Run tests:

```bash
hyperscript path/to/config.yaml
```

### Options

- `--skip-error`: Continue with the next test on error.
- `--verbose`: Enable detailed logging.

## Contributing

Fork the repository and submit a pull request with your changes.

## License

MIT License. See the [LICENSE](LICENSE) file.

## Contact

For questions, email [happer64bit@gmail.com](mailto:happer64bit@gmail.com).

