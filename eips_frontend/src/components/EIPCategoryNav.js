import React from 'react';
import { Query } from 'react-apollo';
import EIPCategoryButton from './EIPCategoryButton';
import { getCategories } from '../queries';

class EIPCategoryNav extends React.Component {
  render () {
    return (
      <Query query={getCategories}>
        {({ loading, error, data }) => {
          if (loading) return (
            <div className="notification is-info">
              Loading...
            </div>
          );
          if (error) return (
            <div className="notification is-danger">
              Error: ${error.message}
            </div>
          );

          const categoryButtons = data.categories.reduce((acc, {category, eipCount}) => {
            if (category == null) return acc
            acc.push((
              <EIPCategoryButton category={category} count={eipCount} />
            ));
            return acc
          }, []);

          return (
            <div className="category-nav">
              {categoryButtons}
            </div>
          );
        }}
      </Query>
    )
  }
}

export default EIPCategoryNav;
