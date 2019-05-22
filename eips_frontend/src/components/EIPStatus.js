import React from 'react';

import { EIPS_STATUSES } from '../const';

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
