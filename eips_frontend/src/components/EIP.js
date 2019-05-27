import React from 'react';
import { Link } from 'react-router-dom';

import { ADDRESS_PATTERN } from '../const';
import { truncateAddressInString } from '../utils';

import Tags from './Tags';
import EIPStatus from './EIPStatus';

class EIP extends React.Component {
  render () {
    const { eipId, eipType, status, category, tags } = this.props.eip;
    let { title } = this.props.eip;

    if (title.search(ADDRESS_PATTERN) > -1) {
      title = truncateAddressInString(title);
    }

    const tagObjs = tags.map(tag => ({ tagName: tag }))

    return (
      <div className="eip card">
        <Link to={`/eip/${eipId}`}>
          <header className="card-header">
            <div className="card-header-title">
              <h4 className="is-pulled-left is-size-4">{title}</h4>
            </div>
          </header>
          <div className="card-content">
            <div className="level is-mobile">
              <div className="level-left">
                <div className="level-item has-text-centered">
                  EIP-{eipId}
                </div>
                <div className="level-item has-text-centered">
                  <EIPStatus status={status} />
                </div>
              </div>
              <div className="level-right">
                <div className="level-item has-text-centered">
                  {eipType}
                </div>
                <div className="level-item has-text-centered">
                  {category}
                </div>
              </div>
            </div>
          </div>
        </Link>
        <footer className="card-footer">
          <Tags tags={tagObjs} />
        </footer>
      </div>
    )
  }
}

export default EIP;
