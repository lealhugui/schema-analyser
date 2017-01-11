 // Launch GraphQL
  // const graphql = express();
  // graphql.use('/', graphQLHTTP({
  //   graphiql: true,
  //   pretty: true,
  //   schema
  // }));
  // graphql.listen(config.graphql.port, () => console.log(chalk.green(`GraphQL is listening on port ${config.graphql.port}`)));

  // But keep the proxy through to 8000 (which will now be served by django)
  // Launch Relay by using webpack.config.js
  const relayServer = new WebpackDevServer(webpack(webpackConfig), {
    contentBase: '/build/',
    proxy: {
      '/graphql': `http://localhost:${config.graphql.port}`
    },
    stats: {
      colors: true
    },
    hot: true,
    historyApiFallback: true
  });