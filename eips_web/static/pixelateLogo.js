(function () {
  document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('logo')
    const { width, height } = container.getBoundingClientRect();
    const stage = new Konva.Stage({ container, width, height });
    const layer = new Konva.Layer();
    stage.add(layer);

    const image = new Image();
    image.onload = function () {
      const logo = new Konva.Image({
        x: 0,
        y: 0,
        image,
        width,
        height,
      });

      // add the shape to the layer
      layer.add(logo);
      logo.cache();
      logo.filters([Konva.Filters.Pixelate]);
      logo.pixelSize(1)

      function onClick() {
        window.location = '/';
      }

      logo.on('click', onClick)
      logo.on('tap', onClick)
      logo.on('mouseover', function () {
        logo.pixelSize(20);
      })
      logo.on('mouseout', function () {
        logo.pixelSize(1);
      })
    };
    image.src = '/static/logo.svg';
  });
})()
