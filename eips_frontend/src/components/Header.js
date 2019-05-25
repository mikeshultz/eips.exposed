import React from 'react';
import { Link } from 'react-router-dom';
import PixelatedImage from './PixelatedImage';

class Header extends React.Component {
  render () {
    let logoWidth = 500; // orig: 723;
    let logoHeight = 102; // orig: 147;

    if (logoWidth > window.innerWidth) {
      const diff = logoWidth - window.innerWidth;
      const ratio = logoHeight / logoWidth;
      console.log(`orig - width: ${logoWidth} / height ${logoHeight}`);
      console.log(`diff: ${diff} -- ratio ${ratio}`);
      logoWidth = logoWidth - diff;
      logoHeight = logoWidth * ratio;
      console.log(`after - width: ${logoWidth} / height ${logoHeight}`);
    }

    return (
      <header className="App-header loading-overlay-parent">
        <div className={this.props.loading ? `loading-overlay` : `hide`}></div>
        <nav className="level">
          <div className="level-item has-text-centered">
            <div>
              <p className="heading">EIPs</p>
              <p className="title">{this.props.stats ? this.props.stats.eips : ''}</p>
            </div>
          </div>
          <div className="level-item has-text-centered">
            <div>
              <p className="heading">Commits</p>
              <p className="title">{this.props.stats ? this.props.stats.commits : ''}</p>
            </div>
          </div>
          <div className="level-item has-text-centered has-brand">
            <div className="brand">
              <Link to="/" className="">
                <PixelatedImage src="/eips.exposed-logo.png" maxPixelSize={15}>
                  <img id="exposed-logo" src="/eips.exposed-logo.png" alt="eips.exposed"
                    width={logoWidth} height={logoHeight} />
                </PixelatedImage>
                <p className="subtitl is-4">Ethereum improvement proposal explorer</p>
              </Link>
            </div>
          </div>
          <div className="level-item has-text-centered">
            <div>
              <p className="heading">Contributors</p>
              <p className="title">{this.props.stats ? this.props.stats.contributors : ''}</p>
            </div>
          </div>
          <div className="level-item has-text-centered">
            <div>
              <p className="heading">Issues</p>
              <p className="title">{this.props.stats ? this.props.stats.issues : ''}</p>
            </div>
          </div>
        </nav>
      </header>
    )
  }
}

export default Header;
