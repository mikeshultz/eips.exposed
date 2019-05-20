import React from 'react';
import { Link } from 'react-router-dom';

import { EIPS_STATUSES } from '../const';
import Tags from './Tags';

class EIPStatus extends React.Component {
  render () {
    const { status } = this.props;
    const { extraClass, text } = EIPS_STATUSES[status];
    return (
      <div className={`eip-status ${extraClass}`}>
        {text ? text : status}
      </div>
    )
  }
}

export default EIPStatus;
