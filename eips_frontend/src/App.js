import React from 'react';
import { Query } from 'react-apollo';
import { BrowserRouter, Route } from 'react-router-dom'

import { EIPList, EIPListCompact, EIPDetailPage } from './pages';
import { Header, Footer } from './components';
import { getStats } from './queries';

import './App.css';

class App extends React.Component {
  render() {
    return (
      <BrowserRouter>
        <div className="App">
          <Query query={getStats}>
            {({ loading, error, data }) => {
              return (<Header loading={loading} stats={data ? data.stats : null} />)
            }}
          </Query>

          <Route path="/eip/:eipId" component={EIPDetailPage} />
          <Route path="/tagged/:tagName" exact component={EIPListCompact} />
          <Route path="/category/:category" exact component={EIPListCompact} />
          <Route path="/status/:status" exact component={EIPListCompact} />
          <Route path="/" exact component={EIPListCompact} />

          <Footer />
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
