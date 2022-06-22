import { expect } from 'chai';
import { ethers } from 'hardhat';
// import { describeBehaviorOfFactory } from '@solidstate/spec';
import {
  Create2MetadataAwareFactoryMock,
  Create2MetadataAwareFactoryMock__factory,
  ICreate2DeploymentMetadata
} from '../../../../typechain';

describe('Create2MetadataAwareFactory Test Suite', function () {
  
  let instance: Create2MetadataAwareFactoryMock;
  let newInstance: ICreate2DeploymentMetadata;

  beforeEach(async function () {
    const [deployer] = await ethers.getSigners();
    instance = await new Create2MetadataAwareFactoryMock__factory(deployer).deploy();
  });

  // describeBehaviorOfFactory({ deploy: async () => instance });

  describe('__internal', function () {
    describe('#_deployWithCreate2Metadata', function () {
      // describe('(bytes)', function () {
      //   it('deploys bytecode and returns deployment address', async function () {
      //     const initCode = instance.deployTransaction.data;

      //     const address = await instance.callStatic['deploy(bytes)'](initCode);
      //     expect(address).to.be.properAddress;

      //     await instance['deploy(bytes)'](initCode);

      //     expect(await ethers.provider.getCode(address)).to.equal(
      //       await ethers.provider.getCode(instance.address),
      //     );
      //   });

      //   describe('reverts if', function () {
      //     it('contract creation fails', async function () {
      //       const initCode = '0xfe';

      //       await expect(instance['deploy(bytes)'](initCode)).to.revertedWith(
      //         'CreateUtils: failed deployment',
      //       );
      //     });
      //   });
      // });

      describe('(bytes,bytes32)', function () {
        it('deploys bytecode and returns deployment address initialized with Create2Metadata', async function () {
          const initCode = await instance.deployTransaction.data;
          const initCodeHash = ethers.utils.keccak256(initCode);

          const address = await instance.callStatic['deployWithCreate2Metadata(bytes,bytes32)'](
            initCode,
            initCodeHash,
          );
          expect(address).to.equal(
            ethers.utils.getCreate2Address(instance.address, initCodeHash, initCodeHash)
          );
          expect(address).to.equal(
            await instance.callStatic.calculateDeploymentAddress(
              initCodeHash,
              initCodeHash,
            ),
          );

          await instance['deployWithCreate2Metadata(bytes,bytes32)'](initCode, initCodeHash);

          expect(await ethers.provider.getCode(address)).to.equal(
            await ethers.provider.getCode(instance.address),
          );

          newInstance = await ethers.getContractAt("ICreate2DeploymentMetadata", address) as ICreate2DeploymentMetadata;

          expect(await ethers.provider.getCode(newInstance.address)).to.equal(
            await ethers.provider.getCode(instance.address),
          );

          const metadata = await newInstance.getCreate2DeploymentMetadata();

          expect(metadata.deployerAddress).to.equal(instance.address);
          expect(metadata.deploymentSalt).to.equal(initCodeHash);
        });

        describe('reverts if', function () {
          it('contract creation fails', async function () {
            const initCode = '0xfe';
            const salt = ethers.utils.randomBytes(32);

            await expect(
              instance['deployWithCreate2Metadata(bytes,bytes32)'](initCode, salt),
            ).to.revertedWith('Create2Utils: failed deployment');
          });

          it('salt has already been used', async function () {
            const initCode = instance.deployTransaction.data;
            const salt = ethers.utils.randomBytes(32);

            await instance['deployWithCreate2Metadata(bytes,bytes32)'](initCode, salt);

            await expect(
              instance['deployWithCreate2Metadata(bytes,bytes32)'](initCode, salt),
            ).to.be.revertedWith('Create2Utils: failed deployment');
          });
        });
      });
    });

    describe('#_calculateDeploymentAddress', function () {
      it('returns address of not-yet-deployed contract', async function () {
        const initCode = instance.deployTransaction.data;
        const initCodeHash = ethers.utils.keccak256(initCode);
        const salt = ethers.utils.randomBytes(32);

        expect(
          await instance.callStatic.calculateDeploymentAddress(initCodeHash, salt),
        ).to.equal(
          ethers.utils.getCreate2Address(instance.address, salt, initCodeHash),
        );
      });
    });
  });
});