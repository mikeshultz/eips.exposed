import React from 'react';
import { Query } from 'react-apollo';
import EIPStatusButton from './EIPStatusButton';
import { getStatuses } from '../queries';

class EIPStatusNav extends React.Component {
  render () {
    return (
      <Query query={getStatuses}>
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

          const statusButtons = data.statuses.reduce((acc, {status, eipCount}) => {
            if (status == null) return acc
            acc.push((
              <EIPStatusButton key={status} status={status} count={eipCount} />
            ));
            return acc
          }, []);

          return (
            <div className="status-nav">
              {statusButtons}
            </div>
          );
        }}
      </Query>
    )
  }
}

export default EIPStatusNav;
