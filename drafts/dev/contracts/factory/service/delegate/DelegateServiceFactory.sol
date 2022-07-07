// SPDX-License-Identifier: AGPL-3.0-or-later

/* -------------------------------------------------------------------------- */
/*                       SECTION DelegateServiceFactory                       */
/* -------------------------------------------------------------------------- */

pragma solidity ^0.8.0;

import {
  DelegateServiceFactoryLogic,
  DelegateServiceFactoryStorage,
  DelegateServiceFactoryStorageUtils
} from "contracts/factory/service/delegate/logic/DelegateServiceFactoryLogic.sol";
import {
  IDelegateServiceFactory
} from "contracts/factory/service/delegate/interfaces/IDelegateServiceFactory.sol";
import {
  DelegateService,
  IDelegateService,
  ICreate2DeploymentMetadata
} from "contracts/service/delegate/DelegateService.sol";
import {
  IDelegateServiceRegistry
} from "contracts/registries/service/delegate/interfaces/IDelegateServiceRegistry.sol";
// import {
//   IDelegateService
// } from "contracts/service/delegate/interfaces/IDelegateService.sol";

import "hardhat/console.sol";

contract DelegateServiceFactory
  is
    IDelegateServiceFactory,
    DelegateServiceFactoryLogic,
    DelegateService
{

  constructor() {

    bytes4[] memory functionSelectors = new bytes4[](3);
    functionSelectors[0] = IDelegateServiceFactory.calculateDeploymentAddress.selector;
    functionSelectors[1] = IDelegateServiceFactory.deployDelegateService.selector;
    functionSelectors[2] = IDelegateServiceFactory.getDelegateServiceRegistry.selector;

    _initServiceDef(
      type(IDelegateServiceFactory).interfaceId,
      functionSelectors
    );
    
  }

  function calculateDeploymentAddress(bytes32 initCodeHash, bytes32 salt) external view returns (address newAddress) {
    newAddress = _calculateDeploymentAddress(initCodeHash, salt);
  }

  // function calculateDeploymentAddressFromAddress(
  //     address deployer,
  //     bytes32 initCodeHash,
  //     bytes32 salt
  //   ) pure external returns (address deploymenAddress) {
  //   deploymenAddress = _calculateDeploymentAddressFromAddress(
  //     deployer,
  //     initCodeHash,
  //     salt
  //   );
  // }

  // TODO Restrict to Ownable
  // TODO Implement RBAC NFT
  function deployDelegateService(
    bytes4 delegateServiceInterfaceId,
    bytes memory delegateServiceCreationCode
  ) external returns (address delegateService) {
    // console.log("DelegateServiceFactory:deployDelegateService:: Deploying new DelegateService with salt of %s", address(bytes20(delegateServiceInterfaceId)));
    // console.log("DelegateServiceFactory:deployDelegateService:: Deploying new DelegateService from %s",address(this));

    delegateService = _deployDelegateService(delegateServiceCreationCode, delegateServiceInterfaceId);

    // console.log("DelegateServiceFactory:deployDelegateService:: New DelegateService address is %s", delegateService);

    IDelegateServiceRegistry(_getDelegateServiceRegistry()).registerDelegateService(
      delegateServiceInterfaceId,
      delegateService
    );
    // TODO move new delegate service registration logic into this DelegateServiceFactory.
    // require( IDelegateService(delegateService).registerDelegateService(delegateServiceInterfaceId), "DSFactory: DS registration failed." );
  }

  function _getDelegateServiceRegistry() view internal returns (address delegateServiceRegistry) {
    delegateServiceRegistry = _getDelegateServiceRegistry(type(IDelegateServiceFactory).interfaceId);
  }

  function getDelegateServiceRegistry() view external returns (address delegateServiceRegistry) {
    delegateServiceRegistry = _getDelegateServiceRegistry();
  }

}
/* -------------------------------------------------------------------------- */
/*                       !SECTION DelegateServiceFactory                      */
/* -------------------------------------------------------------------------- */