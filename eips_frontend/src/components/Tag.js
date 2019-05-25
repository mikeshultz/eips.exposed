import React from 'react';
import { Link } from 'react-router-dom';

class Tag extends React.Component {
  render () {
    const fontSize = `${this.props.fontSize}px` || '12px'
    const className = `tag${this.props.extraClasses ? ' ' + this.props.extraClasses : ''}`;
    const toURL = this.props.url ? this.props.url : `/tagged/${this.props.tag}`;
    return (
      <Link to={toURL} className={className} style={{ fontSize }}>
        {this.props.tag}
      </Link>
    )
  }
}

export default Tag;
