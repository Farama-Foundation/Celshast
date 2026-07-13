const { resolve } = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");

module.exports = {
  devtool: "source-map",
  entry: {
    celshast: [
      "./src/celshast/assets/scripts/celshast.js",
      "./src/celshast/assets/styles/celshast.sass",
    ],
    "celshast-extensions": ["./src/celshast/assets/styles/celshast-extensions.sass"],
  },
  output: {
    filename: "scripts/[name].js",
    path: resolve(__dirname, "src/celshast/theme/celshast/static"),
  },
  plugins: [new MiniCssExtractPlugin({ filename: "styles/[name].css" })],
  optimization: { minimizer: [`...`, new CssMinimizerPlugin()] },
  module: {
    rules: [
      {
        test: /\.s[ac]ss$/i,
        use: [
          MiniCssExtractPlugin.loader,
          { loader: "css-loader", options: { sourceMap: true } },
          { loader: "postcss-loader", options: { sourceMap: true } },
          { loader: "sass-loader", options: { sourceMap: true } },
        ],
      },
    ],
  },
};
