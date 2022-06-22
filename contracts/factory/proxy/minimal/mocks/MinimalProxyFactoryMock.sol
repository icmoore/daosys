// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.8.0;

import {MinimalProxyFactory} from "contracts/factory/proxy/minimal/MinimalProxyFactory.sol";

contract MinimalProxyFactoryMock is MinimalProxyFactory {
  
  /**
   * @notice deploy an EIP1167 minimal proxy using "CREATE" opcode
   * @param target implementation contract to proxy
   * @return minimalProxy address of deployed proxy
   */
  function deployMinimalProxy(address target) external returns (address minimalProxy) {
    return _deployMinimalProxy(target);
  }

  /**
   * @notice deploy an EIP1167 minimal proxy using "CREATE2" opcode
   * @dev reverts if deployment is not successful (likely because salt has already been used)
   * @param target implementation contract to proxy
   * @param salt input for deterministic address calculation
   * @return minimalProxy address of deployed proxy
   */
  function deployMinimalProxyWithSalt(address target, bytes32 salt) external returns (address minimalProxy) {
    return _deployMinimalProxyWithSalt(target, salt);
  }

  /**
   * @notice calculate the deployment address for a given target and salt
   * @param target implementation contract to proxy
   * @param salt input for deterministic address calculation
   * @return deployment address
   */
  // function calculateMinimalProxyDeploymentAddress(address target, bytes32 salt) external view returns (address) {
  //   return _calculateMinimalProxyDeploymentAddress(target, salt);
  // }

  /**
   * @notice concatenate elements to form EIP1167 minimal proxy initialization code
   * @param target implementation contract to proxy
   * @return bytes memory initialization code
   */
  // function generateMinimalProxyInitCode(address target) external pure returns (bytes memory) {
  //   return _generateMinimalProxyInitCode(target);
  // }

}