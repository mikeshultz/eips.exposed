import React from 'react';
import Tag from './Tag';

class Tags extends React.Component {
  render () {
    const tags = this.props.tags ?
      this.props.tags.map(tag => (
        <Tag
            key={tag.tagName}
            tag={tag.tagName}
            fontSize={tag.eipsCount ? 12 + tag.eipsCount : 12}
            />
    )) : [];
    return (
      <div className="tags">
        {tags}
      </div>
    )
  }
}

export default Tags;
