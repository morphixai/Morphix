require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();  // ✅ ใช้ dotenv

module.exports = {
  solidity: "0.8.28",
  networks: {
    baseTestnet: {
      url: process.env.ALCHEMY_API_URL,  // ✅ ซ่อน API URL
      accounts: [process.env.PRIVATE_KEY]  // ✅ ซ่อน Private Key
    }
  }
};
