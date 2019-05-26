import React from 'react';
import { Query } from 'react-apollo';
import { getEIP } from '../queries';
import { Markdown, Tags, EIPHeader } from '../components';

class EIPDetail extends React.Component {
  render () {
    const { eipId } = this.props.match.params
    return (
      <section id="eip-detail">
        <div className="container">
          <Query query={getEIP} variables={{ eipId }}>
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

              const { eipId, title, fullText } = data.eip
              const tags = data.eip.tags.map(tag => ({ tagName: tag }))
              return (
                <section className="section">
                  <div className="container">
                    <div className="content">
                      <h2 className="is-title is-size-2">EIP-{eipId}: {title}</h2>

                      <EIPHeader eip={data.eip} />

                      <Tags tags={tags} />

                      <Markdown content={fullText} />
                    </div>
                  </div>
                </section>
              )
            }}
          </Query>
        </div>
      </section>
    )
  }
}

export default EIPDetail;
