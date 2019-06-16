import React from 'react';
import { Link } from 'react-router-dom';

import { ADDRESS_PATTERN } from '../const';
import { truncateAddressInString } from '../utils';

import EIPStatus from './EIPStatus';
import EIPDetail from './EIPDetail';

class EIPBar extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      showDetails: false
    }

    this.toggleDetail = this.toggleDetail.bind(this)
  }

  toggleDetail(ev) {
    // Only fire for screens larger than mobile
    const mm = window.matchMedia('(max-width: 768px)')
    if (!mm.matches) {
      ev.preventDefault();
      this.setState({
        showDetails: !this.state.showDetails
      })
    }
  }

  render () {
    const { eipId, eipType, status, category, tags } = this.props.eip;
    let { title } = this.props.eip;

    if (title.search(ADDRESS_PATTERN) > -1) {
      title = truncateAddressInString(title);
    }

    const details = this.state.showDetails ? (<EIPDetail eipId={eipId} />) : '';

    return (
      <div className="eip-bar-combined">
        <Link to={`/eip/${eipId}`} onClick={this.toggleDetail}>
          <div className="level eip bar">
            <div className="level-left bar-title">
              <div className="level-item">
                <p className="is-pulled-left is-size-4">EIP-{eipId} - {title}</p>
              </div>
            </div>
            <div className="level-right bar-meta">
              <div className="level-item bar-status">
                <EIPStatus status={status} />
              </div>
              <div className="level-item bar-type">
                {eipType}
              </div>
              <div className="level-item bar-category">
                {category}
              </div>
              <div className="level-item bar-expand">
                <span className="expand">{this.state.showDetails ? `-` : `+`}</span>
              </div>
            </div>
          </div>
        </Link>
        <div id={`eip-content-${eipId}`} className={`bar-content${this.state.showDetails ? '' : ' hide'}`}>
          {details}
        </div>
      </div>
    )
  }
}

export default EIPBar;
