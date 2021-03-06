import React from 'react';
import { Query } from 'react-apollo';

import { Tags, EIPsCompact, SearchBox, EIPCategoryNav, EIPStatusNav } from '../components';
import { getEIPs, getTags } from '../queries';

class EIPListCompact extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      searchTerm: '',
      hideTags: false,
    }

    this.search = this.search.bind(this);
  }

  search(terms) {
    this.setState({
      searchTerm: terms,
      hideTags: terms ? true : false,
    });
    console.debug(`Searching for "${terms}"`)
  }

  render () {
    const { tagName, category, status } = this.props.match.params
    const variables = { tag: tagName, category, status, search: this.state.searchTerm };
    return (
      <>

        <SearchBox onUpdate={this.search} searchTerm={this.state.searchTerm} />

        <div className="level category-status">
          <div className="level-left">
            <div className="level-item">
              <EIPCategoryNav />
            </div>
          </div>
          <div className="level-right">
            <div className="level-item">
              <EIPStatusNav />
            </div>
          </div>
        </div>

        {/*<Query query={getTags}>
          {({ loading, error, data }) => {
            if (loading) return (
              <div className="notification is-info">
                Loading...
              </div>
            );
            if (error) return (
              <div className="notification is-danger">
                Error: ${error.message}
              </div>
            );

            if (this.state.hideTags) return null
        
            return (
              <div id="tag-container" className="container">
                <Tags tags={data.tags} />
              </div>
            )
          }}
        </Query>*/}

        <Query query={getEIPs} variables={variables}>
          {({ loading, error, data }) => {
            if (error) return `Error! ${error.message}`;
          
            return (
              <EIPsCompact
                loading={loading}
                eips={data && data.eips ? data.eips : []}
                />
            )
          }}
        </Query>
      </>
    )
  }
}

export default EIPListCompact;

