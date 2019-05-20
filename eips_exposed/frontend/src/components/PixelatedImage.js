import React from 'react';
import Konva from 'konva';
import { Stage, Layer, Image } from 'react-konva';

class PixelatedImage extends React.Component {
    constructor(props) {
      super(props)

      this.state = {
        image: null,
        pixelSize: 1
      };

      this.currentIntervalID = 0;
      this.maxPixelSize = this.props.maxPixelSize || 20;
      this.frames = 10;
      this.frameInterval = 50;

      this.mouseOver = this.mouseOver.bind(this);
      this.mouseOut = this.mouseOut.bind(this);
    }

    componentDidMount() {
      this.canvas = document.createElement('canvas');
      if (React.Children.count(this.props.children) > 1) {
        console.error('Component PixelatedImage should only have one child!');
        return
      }
      if (this.props.children.type !== 'img') {
        console.error('Child of PixelatedImage must be an img tag');
        return
      }
      const childImage = this.props.children;
      const imgURL = childImage.props.src;
      this.width = childImage.props.width;
      this.height = childImage.props.height;
      const image = new window.Image(this.width, this.height);
      image.src = imgURL;
      image.onload = () => {
        this.setState({
          image: image,
          pixelSize: 1
        }, () => {
          this.imageNode.cache();
          this.imageNode.getLayer().batchDraw();
        });
      }
    }

    mouseOver(ev) {
      const that = this;
      let frameCount = 0;

      // If there's an animation running, kill it
      if (this.currentIntervalID > 0) {
        clearInterval(this.currentIntervalID);
      }

      // Janky keyframes
      this.currentIntervalID = setInterval(() => {
        frameCount += 1
        that.setState({
          pixelSize: (that.maxPixelSize / that.frames) * frameCount
        })
        if (frameCount >= that.frames) {
          clearInterval(that.currentIntervalID);
        }
      }, this.frameInterval);
    }

    mouseOut(ev) {
      const that = this;
      let frameCount = this.frames;

      // If there's an animation running, kill it
      if (this.currentIntervalID > 0) {
        clearInterval(this.currentIntervalID);
      }

      // Janky keyframes
      this.currentIntervalID = setInterval(() => {
        frameCount -= 1
        that.setState({
          pixelSize: (that.maxPixelSize / that.frames) * frameCount
        })
        if (frameCount <= 1) {
          clearInterval(that.currentIntervalID);
        }
      }, this.frameInterval);
    }

    render() {
      return (
        <Stage width={this.width} height={this.height}>

          <Layer ref={node => {this.layer = node; }}>
            <Image
              x={this.props.x}
              y={this.props.y}
              image={this.state ? this.state.image : null}
              ref={node => {
                this.imageNode = node;
              }}
              filters={[Konva.Filters.Pixelate]}
              pixelSize={this.state.pixelSize}
              onMouseOver={this.mouseOver}
              onMouseOut={this.mouseOut}
            />
          </Layer>
        </Stage>
      )
    }
}

export default PixelatedImage;
