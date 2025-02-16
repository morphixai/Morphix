const hre = require("hardhat");

async function main() {
  const MorphixDAO = await hre.ethers.getContractFactory("MorphixDAO");
  const dao = await MorphixDAO.deploy();

  await dao.waitForDeployment();  // ✅ ใช้ waitForDeployment() แทน
  console.log(`MorphixDAO deployed to: ${await dao.getAddress()}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
