import React from 'react';
import { Link } from 'react-router-dom';
import { EIPS_STATUSES } from '../const';

class EIPStatusButton extends React.Component {
  render () {
    const { text: statusName, extraClass } = EIPS_STATUSES[this.props.status];
    const toURL = this.props.url ? this.props.url : `/status/${this.props.status.toLowerCase()}`;
    return (
      <Link to={toURL} className={`button status-button${extraClass ? ' extraClass' : ''}`}>
        {statusName} <span className="count">{this.props.count}</span>
      </Link>
    );
  }
}

export default EIPStatusButton;
