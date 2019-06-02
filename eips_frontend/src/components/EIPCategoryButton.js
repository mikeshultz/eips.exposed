import React from 'react';
import { Link } from 'react-router-dom';
import { EIPS_CATEGORIES } from '../const';

class EIPCategoryButton extends React.Component {
  render () {
    const categoryName = EIPS_CATEGORIES[this.props.category].text
    const toURL = this.props.url ? this.props.url : `/category/${this.props.category.toLowerCase()}`;
    return (
      <Link to={toURL} className="button category-button">
        {categoryName} <span className="count">{this.props.count}</span>
      </Link>
    );
  }
}

export default EIPCategoryButton;
