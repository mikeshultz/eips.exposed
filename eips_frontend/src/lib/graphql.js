import ApolloClient from "apollo-boost";

export default new ApolloClient({
  uri: process.env.REACT_APP_GRAPHQL_URL ?
    process.env.REACT_APP_GRAPHQL_URL :
    `${window.location.protocol}//${window.location.host}/graphql`
})
