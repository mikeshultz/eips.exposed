import React from 'react';

class Footer extends React.Component {
  render () {
    return (
      <footer className="footer">
        <div className="content has-text-centered">
          <p className="is-size-7">
            <b>eips.exposed</b> is a project by <a href="https://mikeshultz.com">Mike Shultz</a>
          </p>
          <p className="is-size-7">
            It is intended to help developers of the Ethereum ecosystem navigate EIPs in a more
            coerent way.  All content copyrights have been waived and are availble in the
            <strong> public domain</strong> according to
            &nbsp;<a href="https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1.md">EIP-1</a>.
          </p>
        </div>
      </footer>
    )
  }
}

export default Footer;
