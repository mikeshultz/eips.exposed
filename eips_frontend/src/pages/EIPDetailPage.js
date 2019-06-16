import React from 'react';
import { EIPDetail } from '../components';

class EIPDetailPage extends React.Component {
  render () {
    const eipId = this.props.eipId || this.props.match.params.eipId
    return (
      <section>
       <EIPDetail eipId={eipId} />
      </section>
    )
  }
}

export default EIPDetailPage;
