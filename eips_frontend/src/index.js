import React from 'react';
import ReactDOM from 'react-dom';
import './index.scss';
import App from './App';
import { ApolloProvider } from 'react-apollo';
import graphql from './lib/graphql'
import * as serviceWorker from './serviceWorker';

if (window.location.hostname !== 'localhost' && window.location.protocol !== 'https:') {
  window.location.href = 'https:' + window.location.href.substring(window.location.protocol.length);
}

ReactDOM.render(
  <ApolloProvider client={graphql}>
    <App />
  </ApolloProvider>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
