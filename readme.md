# MED9.1 Multimap Tool

## Overview

The MED9.1 Multimap Tool is a powerful utility designed for tuning and managing multimap configurations in Bosch MED9.1 engine control units. This tool simplifies the process of adjusting and optimizing the engine's performance by allowing users to easily modify and flash multimap settings.

## Features

- **Multimap Configuration:** Modify and manage multiple maps for various engine parameters.
  
- **Flash Tool Integration:** Seamlessly flash the updated multimap configurations to the Bosch MED9.1 ECU.

- **User-Friendly Interface:** Intuitive and easy-to-use interface for both novice and experienced tuners.

- **Version Control:** Keep track of changes with built-in version control for multimap configurations.

## Installation

1. **Download:** Clone or download the repository from [GitHub](https://github.com/EliasKotlyar/MED9.1-Multimap-Tool).

2. **Run:** Execute the tool by running the main application file.

## Usage

1. **Run the application** to launch the MED9.1 Multimap Tool.

## How does the multimap gonna work in my car?

1. This tool patches "vkKraQu" variable in
2. It will try to find a corresponding ECU Definition file under "variants"
3. When found, it will add all necessary addresses into the payload.
4. Then the payload will be attached to the binary and the address will be patched

## How does the patching tool work?

1. It will identify the binary using the EPK Number
2. It will try to find a corresponding ECU Definition file under "variants"
3. When found, it will add all necessary addresses into the payload
4. Then the payload will be attached to the binary and the binary will be patched to execute it

## How to adapt it to my MED9.1 Version?

see [Adaptation](adaptation.md).


## Contributing PRs

If you would like to contribute to the development of the MED9.1 Multimap Tool, please make a PR

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or support, please contact elias.kotlyar@gmail.com.

