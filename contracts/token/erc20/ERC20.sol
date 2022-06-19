// SPDX-License-Identifier: AGPL-3.0-or-later
pragma solidity ^0.8.0;

import {IERC20} from "contracts/token/erc20/IERC20.sol";

contract ERC20 is IERC20 {

  string public name;

  function initERC20(
    string memory newName
  ) external returns (bool success) {
    name = newName;
    success = true;
  }

}