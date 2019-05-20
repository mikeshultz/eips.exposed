import React from 'react';
import MarkdownIt from 'markdown-it';

class Markdown extends React.Component {
  constructor(props) {
    super(props);

    this.md = new MarkdownIt({
      breaks: true,
      linkify: true
    });
  }
  render () {
    const noContent = '<p className="no-content">No content found</p>';
    return (
      <div className="container markdown" dangerouslySetInnerHTML={{
        __html: this.props.content ? this.md.render(this.props.content) : noContent
      }} />
    )
  }
}

export default Markdown;
