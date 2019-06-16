import React from 'react';
import { Query } from 'react-apollo';
import { getEIP } from '../queries';
import { Markdown, Tags, EIPHeader, CommitsTable } from '../components';

class EIPDetail extends React.Component {
  render () {
    const eipId = this.props.eipId || this.props.match.params.eipId
    return (
      <div id="eip-detail" className="container">
        <Query query={getEIP} variables={{ eipId }}>
          {({ loading, error, data }) => {
            if (loading) return (
              <div className="notification loading">
                Loading...
              </div>
            );
            if (error) return (
              <div className="notification is-danger">
                Error: ${error.message}
              </div>
            );

            const { eipId, title, fullText } = data.eip
            const tags = data.eip.tags.map(tag => ({ tagName: tag }))
            return (
              <section className="section">
                <div className="container">
                  <div className="content">
                    <h2 className="is-title is-size-2">EIP-{eipId}: {title}</h2>

                    <EIPHeader eip={data.eip} />

                    <CommitsTable eipId={data.eip.eipId} />

                    <Tags tags={tags} />

                    <Markdown content={fullText} />
                  </div>
                </div>
              </section>
            )
          }}
        </Query>
      </div>
    )
  }
}

export default EIPDetail;
