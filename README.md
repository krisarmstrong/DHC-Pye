# DHC-Pye

## Description

This program is a Python implementation of a DHCP Server that can listen for DHCP messages on a specific network interface and respond with basic DHCP options like IP address, subnet mask, and gateway. It uses asyncio for multithreading and adheres to PEP8 conventions for naming variables and functions, and includes appropriate docstrings and comments to explain the purpose and functionality of each component of the program.

## Author

Kris Armstrong

## License

This program is licensed under the Apache 2.0 License.

## Usage

To use the DHCP Server program, simply run it in a Python 3.11 environment on the command line. The program will listen for DHCP messages on the specified network interface and respond with basic DHCP options like IP address, subnet mask, and gateway.

To add support for additional DHCP options like NTP time servers, DNS servers, TFTP, and network boot server options, refer to the DHCP protocol specification (RFC 2131) and other relevant documentation for guidance.

## Contributing

If you would like to contribute to this program, please feel free to submit a pull request with any bug fixes or feature enhancements. Before submitting a pull request, please ensure that your changes are in compliance with the PEP 8 coding style guide and the existing codebase.

## Issues

If you encounter any issues or bugs with this program, please submit an issue on the GitHub repository.

## Acknowledgments

This program was inspired by the DHCP protocol specification and the benefits of using asyncio for improved performance.

## Future Development

- Support for additional DHCP options
- Integration with other Python libraries
- GUI for easy-to-use interface

## Release History

- 0.1.0
  - Initial release

