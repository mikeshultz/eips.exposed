import React from 'react';
import EIP from './EIP';

class EIPs extends React.Component {
  render () {
    let eipCounter = 0;
    const colOne = []
    const colTwo = []
    const colThree = []

    this.props.eips.forEach(eip => {
      eipCounter += 1;
      const eipEl = (
        <EIP key={eip.eipId} eip={eip} />
      );

      if (eipCounter % 3 === 0) {
        colThree.push(eipEl)
      } else if (eipCounter % 2 === 0) {
        colTwo.push(eipEl)
      } else {
        colOne.push(eipEl)
      }
    });

    return (
      <section id="eips" className="section is-clearfix">
        <div className="columns">
          <div className="column">
            {colOne}
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
