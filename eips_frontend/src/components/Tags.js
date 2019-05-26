import React from 'react';
import Tag from './Tag';

const BASE_FONT_SIZE = 10;

class Tags extends React.Component {
  render () {
    const tags = this.props.tags ?
      this.props.tags.map(tag => (
        <Tag
          key={tag.tagName}
          tag={tag.tagName}
          fontSize={tag.eipsCount ? BASE_FONT_SIZE + tag.eipsCount : BASE_FONT_SIZE}
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
