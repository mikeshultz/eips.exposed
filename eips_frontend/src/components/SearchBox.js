import React from 'react';

/**
 * SearchBox is an input intended for live search
 *
 * Props
 * -----
 * onUpdate - function called when the search terms have been updated
 * searchTerm - The search term(s)
 * placeholder - The HTML input placeholder
 * disabled - if the HTML input should be set disabled
 */
class SearchBox extends React.Component {
  constructor(props) {
    super(props);

    if (typeof this.props.onUpdate === 'undefined') {
      throw new Error('onUpdate must be provided for SearchBox')
    }

    this.state = {
      searchTerm: this.props.searchTerm || ''
    }

    this.timeout = null;
    this.onChange = this.onChange.bind(this);
  }

  onChange(ev) {
    const term = ev.target.value;

    this.setState({
      searchTerm: term,
    });

    clearTimeout(this.timeout);
    const that = this;
    console.debug('setTimeout')
    this.timeout = setTimeout(() => {
      console.log('timeout!')
      that.props.onUpdate(that.state.searchTerm)
    }, 500);
  }

  render () {
    return (
      <div className="container search-box">
        <input
          className="search-input"
          value={this.state.searchTerm}
          placeholder={this.props.placeholder || 'Search'}
          disabled={this.props.disabled || false}
          onChange={this.onChange}
          />
      </div>
    )
  }
}

export default SearchBox;
