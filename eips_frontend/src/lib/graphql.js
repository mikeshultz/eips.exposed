import ApolloClient from 'apollo-boost';
import { GRAPHQL_URL } from '../const';

export default new ApolloClient({
  uri: GRAPHQL_URL
})
