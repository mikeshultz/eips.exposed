import React from 'react';
import EIPBar from './EIPBar';

class EIPsCompact extends React.Component {
  render () {

    let children = [];

    if (this.props.eips.length > 0) {
      this.props.eips.forEach(eip => {
        children.push((
          <EIPBar key={eip.eipId} eip={eip} />
        ));
      });
    } else {
      children = [(<div key="-1" className="notification is-info no-results">No EIPs found</div>)];
    }

    return (
      <section id="eips-compact" className="loading-overlay-parent section is-clearfix">
        <div className={this.props.loading ? `loading-overlay` : `hide`}></div>
        <div className="eips-rows">
          {children}
        </div>
      </section>
    )
  }
}

export default EIPsCompact;
