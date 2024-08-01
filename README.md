# Hyperscript

**Hyperscript** is a powerful and flexible script for handling complex configurations and requests. It supports various HTTP methods including GET, POST, PUT, and DELETE, and provides extensive options for validating responses against specified conditions.

## Features

- **Support for Multiple HTTP Methods**: Easily configure and test GET, POST, PUT, and DELETE requests.
- **Flexible Validation**: Validate responses based on status codes, content types, and specific body content.
- **Customizable Conditions**: Check if response bodies contain certain values, or if numeric fields are within specified ranges.
- **Detailed Reporting**: Get detailed success and failure messages, with optional verbose output.

## Installation

To install Hyperscript, use pip:

```bash
pip install hyperscript
```

## Usage

Create a YAML configuration file (`config.yaml`) to specify your tests. Here's an example configuration:

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

To run the tests, use the command line:

```bash
hyperscript path/to/config.yaml
```

### Command Line Options

- `--skip-error`: Skip error handling and continue with the next test.

### Example

Here’s how you can run the tests with verbose output:

```bash
hyperscript path/to/config.yaml --verbose
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

Hyperscript is released under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or feedback, please contact [happer64bit@gmail.com](mailto:happer64bit@gmail.com).
