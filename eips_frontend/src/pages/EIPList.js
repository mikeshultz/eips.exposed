import React from 'react';
import { Query } from 'react-apollo';

import { Tags, EIPs } from '../components';
import { getEIPs, getTags } from '../queries';

class EIPList extends React.Component {
  render () {
    const { tagName } = this.props.match.params
    const variables = { tag: tagName };
    return (
      <>
        <Query query={getTags}>
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
        
            return (
              <div id="tag-container" className="container">
                <Tags tags={data.tags} />
              </div>
            )
          }}
        </Query>

        <Query query={getEIPs} variables={variables}>
          {({ loading, error, data }) => {
            if (error) return `Error! ${error.message}`;
          
            return (
              <EIPs
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

export default EIPList;

