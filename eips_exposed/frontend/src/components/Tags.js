import React from 'react';
import Tag from './Tag';

class Tags extends React.Component {
  render () {
    const tags = this.props.tags ?
      this.props.tags.map(tag => (<Tag key={tag} tag={tag} />)) : [];
    return (
      <div className="tags">
        {tags}
      </div>
    )
  }
}

export default Tags;
