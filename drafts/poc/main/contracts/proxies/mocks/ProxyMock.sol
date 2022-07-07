// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import { Proxy } from '../Proxy.sol';

contract ProxyMock is Proxy {
    address private _impl;

    constructor(address implementation) {
        _impl = implementation;
    }

    function _getImplementation() internal view override returns (address) {
        return _impl;
    }
}
