import React from 'react';
import { Query } from 'react-apollo';
import { BrowserRouter, Route } from 'react-router-dom'

import { EIPList, EIPDetail } from './pages';
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

          <Route path="/eip/:eipId" component={EIPDetail} />
          <Route path="/tagged/:tagName" exact component={EIPList} />
          <Route path="/category/:category" exact component={EIPList} />
          <Route path="/status/:status" exact component={EIPList} />
          <Route path="/" exact component={EIPList} />

          <Footer />
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
