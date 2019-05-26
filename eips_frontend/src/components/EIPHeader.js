import React from 'react';
import { EIPS_STATUSES, EIPS_TYPES, EIPS_CATEGORIES } from '../const';

class EIPHeader extends React.Component {
  render () {
    const {
        eipId,
        eipType,
        status,
        author,
        updated,
        discussionsTo,
        reviewPeriodEnd,
        resolution,
        category
    } = this.props.eip;

    const originalLink = `https://github.com/ethereum/EIPs/blob/master/EIPS/eip-${eipId}.md`;
    const statusText = EIPS_STATUSES[status].text;
    const statusClass = EIPS_STATUSES[status].extraClass;
    const typeText = EIPS_TYPES[eipType].text;
    const categoryText = EIPS_CATEGORIES.hasOwnProperty(category) ? EIPS_CATEGORIES[category].text : null;

    return (
      <table className="eip-header table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
        <tr className={eipType ? '': 'hide'}>
            <td>Type</td><td>{typeText}</td>
        </tr>
        <tr className={status ? '': 'hide'}>
            <td>Status</td><td className={statusClass}>{statusText}</td>
        </tr>
        <tr className={author ? '': 'hide'}>
            <td>Author</td><td>{author}</td>
        </tr>
        <tr className={updated ? '': 'hide'}>
            <td>Updated</td><td>{updated}</td>
        </tr>
        <tr className={discussionsTo ? '': 'hide'}>
            <td>Discussion</td><td><a href={discussionsTo}>{discussionsTo}</a></td>
        </tr>
        <tr className={reviewPeriodEnd ? '': 'hide'}>
            <td>Review Period Ends</td><td>{reviewPeriodEnd}</td>
        </tr>
        <tr className={resolution ? '': 'hide'}>
            <td>Resolution</td><td>{resolution}</td>
        </tr>
        <tr className={category ? '': 'hide'}>
            <td>Category</td><td>{categoryText}</td>
        </tr>
        <tr>
            <td>Original</td><td><a href={originalLink}>{originalLink}</a></td>
        </tr>
      </table>
    )
  }
}

export default EIPHeader;
