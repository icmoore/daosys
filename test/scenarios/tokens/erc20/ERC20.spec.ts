import {
  ethers,
  tracer
} from 'hardhat';
import { expect } from "chai";
import { SignerWithAddress } from '@nomiclabs/hardhat-ethers/signers';
import {
  ERC20,
  ERC20__factory
} from '../../../../typechain';

describe("ERC20 Test Suite", function () {

  // Test Wallets
  let deployer: SignerWithAddress;

  // ERC20Basic test variables
  let token: ERC20;
  const tokenName = "TestToken";

  /* -------------------------------------------------------------------------- */
  /*                        SECTION Before All Test Hook                        */
  /* -------------------------------------------------------------------------- */

  before(async function () {
    // Tagging address(0) as "System" in logs.
    tracer.nameTags[ethers.constants.AddressZero] = "System";
  })

  /* -------------------------------------------------------------------------- */
  /*                       !SECTION Before All Test Hook                        */
  /* -------------------------------------------------------------------------- */

  /* -------------------------------------------------------------------------- */
  /*                        SECTION Before Each Test Hook                       */
  /* -------------------------------------------------------------------------- */
  beforeEach(async function () {

    [
      deployer
    ] = await ethers.getSigners();
    tracer.nameTags[deployer.address] = "Deployer";

    token = await new ERC20__factory(deployer).deploy();
    tracer.nameTags[token.address] = "ERC20";

    await token.initERC20(
      tokenName
    );

  });

  /* -------------------------------------------------------------------------- */
  /*                         SECTION Testing ERC20Basic                         */
  /* -------------------------------------------------------------------------- */

  describe("ERC20", function () {
    describe("#name()", function () {
      it("Can read name", async function () {
        expect(await token.name()).to.equal(tokenName);
      });
    });
  });

  /* -------------------------------------------------------------------------- */
  /*                         !SECTION Testing ERC20Basic                        */
  /* -------------------------------------------------------------------------- */

});