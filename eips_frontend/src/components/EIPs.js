import React from 'react';
import EIP from './EIP';

class EIPs extends React.Component {
  render () {
    let eipCounter = 0;
    const colOne = []
    const colTwo = []
    const colThree = []

    const noResultsEl = (<div className="notification is-info no-results">No EIPs found</div>);

    this.props.eips.forEach(eip => {
      const eipEl = (
        <EIP key={eip.eipId} eip={eip} />
      );

      if (eipCounter === 2) {
        colThree.push(eipEl);
        eipCounter = 0;
      } else if (eipCounter === 1) {
        colTwo.push(eipEl);
        eipCounter += 1;
      } else {
        colOne.push(eipEl);
        eipCounter += 1;
      }
    });

    return (
      <section id="eips" className="loading-overlay-parent section is-clearfix">
        <div className={this.props.loading ? `loading-overlay` : `hide`}></div>
        <div className="columns">
          <div className="column">
            {colOne.length > 0 ? colOne : noResultsEl}
          </div>
          <div className="column">
            {colTwo}
          </div>
          <div className="column">
            {colThree}
          </div>
        </div>
      </section>
    )
  }
}

export default EIPs;
