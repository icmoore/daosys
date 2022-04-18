// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.8.0;

/**
 * @title Factory for arbitrary code deployment using the "CREATE" and "CREATE2" opcodes
 */
library FactoryUtils {
  /**
   * @notice deploy contract code using "CREATE" opcode
   * @param initCode contract initialization code
   * @return deployment address of deployed contract
   */
  function _deploy(bytes memory initCode) internal returns (address deployment) {
    assembly {
      let encoded_data := add(0x20, initCode)
      let encoded_size := mload(initCode)
      deployment := create(0, encoded_data, encoded_size)
    }

    require(deployment != address(0), 'Factory: failed deployment');
  }

  /**
   * @notice deploy contract code using "CREATE2" opcode
   * @dev reverts if deployment is not successful (likely because salt has already been used)
   * @param initCode contract initialization code
   * @param salt input for deterministic address calculation
   * @return deployment address of deployed contract
   */
  function _deployWithSalt(bytes memory initCode, bytes32 salt) internal returns (address deployment) {
    assembly {
      let encoded_data := add(0x20, initCode)
      let encoded_size := mload(initCode)
      deployment := create2(0, encoded_data, encoded_size, salt)
    }

    require(deployment != address(0), 'Factory: failed deployment');
  }

  function _calculateInitCodeHash(
    bytes memory creationCode
  ) pure internal returns (bytes32 initCodeHash) {
    initCodeHash = keccak256(creationCode);
  }

  /**
   * @notice calculate the _deployMetamorphicContract deployment address for a given salt
   * @param initCodeHash hash of contract initialization code
   * @param salt input for deterministic address calculation
   * @return deployment address
   */
  function _calculateDeploymentAddress(bytes32 initCodeHash, bytes32 salt) view internal returns (address) {
    return address(
      uint160(
        uint256(
          keccak256(
            abi.encodePacked(
              hex'ff',
              address(this),
              salt,
              initCodeHash
            )
          )
        )
      )
    );
  }

  function _calculateDeploymentAddressFromAddress(
      address deployer,
      bytes32 initCodeHash,
      bytes32 salt
    ) pure internal returns (address deploymenAddress) {
    deploymenAddress = address(
      uint160(
        uint256(
          keccak256(
            abi.encodePacked(
              hex'ff',
              deployer,
              salt,
              initCodeHash
            )
          )
        )
      )
    );
  }
}
