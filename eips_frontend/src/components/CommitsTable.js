import React from 'react';
import { Query } from 'react-apollo';
import { getCommits } from '../queries';
import { truncate } from '../utils';

class CommitsTable extends React.Component {
  render () {
    const { eipId } = this.props;
    return (
      <Query query={getCommits} variables={{ eipId }}>
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

            const commitRows = data.commits.map(commit => {
              return (
                <tr key={commit.commitHash}>
                  <td>
                    <a href={`https://github.com/ethereum/EIPs/commit/${commit.commitHash}`}>
                      {truncate(commit.commitHash, 7)}
                    </a>
                  </td>
                  <td>{commit.author}</td>
                  <td>{commit.committer}</td>
                  <td>{truncate(commit.message, 80)}</td>
                  <td>{commit.committedDate}</td>
                </tr>
              )
            });
          return (
            <table className="table commits">
              <thead>
                <tr>
                  <th>-</th>
                  <th>Author</th>
                  <th>Committer</th>
                  <th>Message</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {commitRows}
              </tbody>
            </table>
          );
        }}
      </Query>
    )
  }
}

export default CommitsTable;
