(function() {
  var canvas = new fabric.Canvas('canvas');
  canvas.preserveObjectStacking = true // 禁止选中图层时自定置于顶部

  canvas.setWidth(1200)
  canvas.setHeight(380)

  fabric.Image.fromURL('../static/res/sea.jpg', (img) => {
    img.set({
        // 通过scale来设置图片大小，这里设置和画布一样大
        scaleX: canvas.width / img.width,
        scaleY: canvas.height / img.height,
    });
    // 设置背景
    canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas));
    canvas.renderAll();
  });

  fabric.Image.fromURL('../static/res/ship/ship.png', function(img) {

    // var ang = Math.asin(185/875);

    canvas.add(img.set({ left: 15, top: 200, angle: -30 }).scale(0.15));
    function animate() {
        img.animate('left', img.left === 15 ? 875 : 15, {
                duration: 5000,
                // easing: fabric.util.ease.easeInElastic
        });
        img.animate('top', img.get('top') === 200 ? 25 : 200, {
            duration: 5000,
            // onChange: canvas.renderAll.bind(canvas),
            // onComplete: animate
        });
    }
    animate();
  });

})();