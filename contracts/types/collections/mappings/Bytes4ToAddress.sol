// SPDX-License-Identifier: AGPL-3.0-or-later

pragma solidity ^0.8.0;

library Bytes4ToAddress {

  struct Layout {
    mapping(bytes4 => address) value;
  }

}

library Bytes4ToAddressUtils {

  bytes32 constant internal STRUCT_STORAGE_SLOT = keccak256(type(Bytes4ToAddress).creationCode);

  function _structSlot() pure internal returns (bytes32 structSlot) {
    structSlot = STRUCT_STORAGE_SLOT;
  }

  /**
   * @notice Could be optimized by having the exposing interface caclulate and store
   *  the storage slot as a constant.
   *  Storage slot is computed during runtime to facilitate development during
   *  standardization.
   */
  function _layout( bytes32 salt ) pure internal returns ( Bytes4ToAddress.Layout storage layout ) {
    bytes32 saltedSlot =
      salt
      ^ Bytes4ToAddressUtils._structSlot();
    assembly{ layout.slot := saltedSlot }
  }

}