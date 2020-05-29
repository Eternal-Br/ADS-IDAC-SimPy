//Aliases
let Application = PIXI.Application,
    Container = PIXI.Container,
    loader = PIXI.loader,
    resources = PIXI.loader.resources,
    TextureCache = PIXI.utils.TextureCache,
    Sprite = PIXI.Sprite;

//Create a Pixi Application
let app = new Application({
    width: 1200,
    height: 386,
    antialiasing: true,
    transparent: false,
    resolution: 1
  }
);

//参数
let id = 0,counter = 0,basicText,bg,isCollision = false;
let stage = app.stage,renderer = app.renderer;
//全局控制参数
let shipList = [];
let ships=[];
let moveList = [];
let waveList=[];

let ship1 = new Ship("../static/res/ship/freighter.png",100,20,0,0.5);
let ship2 = new Ship("../static/res/ship/ship1.png",100,40,0,0.5);
ships.push(ship1);
ships.push(ship2);


// let move1 = new MoveInfo(0,200,-0.3,400,80,1,-0.3)
// let move2 = new MoveInfo(10,10,0,1300,10,1,0)
// moveList.push(move1)
// moveList.push(move2)

//Add the canvas that Pixi automatically created for you to the HTML document
document.getElementById('map').appendChild(app.view);

loader
    .add(["../static/res/background/sea.jpg"
    ,"../static/res/ship/freighter.png"
    ,"../static/res/ship/ship1.png"
    ,"../static/res/wave/wave_header.png"
    ,"../static/res/wave/wave_body.png"
    ])
    .on("progress", loadProgressHandler)
    .load(loadingFinish);
//图片加载完成
function loadingFinish() {
    bg = new Sprite(resources["../static/res/background/sea.jpg"].texture);
    bg.scale.x = 1.5
    stage.addChild(bg);

    basicText = new PIXI.Text("play");
    basicText.x = 50;
    basicText.y = 100;
    stage.addChild(basicText);

    renderer.render(stage);

    // gameLoop();
}
//初始化船舶
function initShip(shipPositionList){
    
    for(let i = 0;i< shipPositionList.length;i++){
        let ship = new Sprite(resources[ships[i].path].texture);
        ship.width = ships[i].width;
        ship.height = ships[i].height;
        ship.x = shipPositionList[i].xPosition;
        ship.y = shipPositionList[i].yPosition;
        ship.rotation = shipPositionList[i].shipRotation;
        ship.anchor.x = ships[i].anchorX;
        ship.anchor.y = ships[i].anchorY;
        shipList.push(ship);
        stage.addChild(ship);
    }

    renderer.render(stage);
}
//
function updateMoveInfo(moveInfoList){
    moveList = [];
    for(let i = 0 ;i < moveInfoList.length;i++){
        moveList.push(moveInfoList[i]);
    }
    gameLoop();
}
//主循环
function gameLoop() {
    // 循环调用gameLoop
    counter += 1;
    id = requestAnimationFrame(gameLoop);

    //轨迹贴图
    let waves = [];
    for(let w = 0;w<moveList.length;w++){
      let wave = new Wave(counter,"../static/res/wave/wave_body.png",moveList[w].picRotation,10,5,moveList[w].locationX,moveList[w].locationY,1,0.5);
      waves.push(wave);
    }

    for(let i = 0;i<waves.length;i++){
        let wave_body = new Sprite(resources[waves[i].path].texture);
        wave_body.anchor.x = waves[i].anchorX;
        wave_body.anchor.y = waves[i].anchorY;
        wave_body.rotation = waves[i].waveRotation;
        wave_body.x = waves[i].waveX;
        wave_body.y = waves[i].waveY+5;
        wave_body.width = waves[i].width;
        wave_body.height = waves[i].height;
        if(counter<12000 && counter % 10 == 0){
            waveList.push(wave_body)
            stage.addChild(wave_body)
        }
    }

    //移动控制
    if (hitTestRectangle(shipList[0],shipList[1])) {
        //There's a collision
        isCollision = true ;
    }else{
        //There's no collision
        move(id,moveList);
    }
    // 渲染舞台
    renderer.render(stage);
}
//移动控制
function move(id,moveList) {
//       basicText.text = "<400"
       for(let i = 0; i< moveList.length;i++){
           if(((moveList[i].speedX >= 0 && shipList[0].x <= moveList[i].targetX)
            ||(moveList[i].speedX <= 0 && shipList[0].x >= moveList[i].targetX))
            &&((moveList[i].speedY >= 0 && shipList[0].y <= moveList[i].targetY)
            ||(moveList[i].speedY <= 0 && shipList[0].y >= moveList[i].targetY))
           ) {
               shipList[i].rotation = moveList[i].picRotation
               shipList[i].x += moveList[i].speedX
               shipList[i].y += moveList[i].speedY
               moveList[i].locationX += moveList[i].speedX
               moveList[i].locationY += moveList[i].speedY
           }else{
               continue;
           }
       }
       // cancelAnimationFrame(id);
}
//移动信息
function MoveInfo(locationX,locationY,picRotation,targetX,targetY,speedX,speedY){
    this.locationX = locationX;
    this.locationY = locationY;
    this.picRotation = picRotation;
    this.targetX = targetX;
    this.targetY = targetY;
    this.speedX = speedX;
    this.speedY = speedY;
}
//加载轨迹贴图
function Wave(counter,path,waveRotation,width,height,waveX,waveY,anchorX,anchorY){
    this.counter = counter;
    this.path = path;
    this.waveRotation = waveRotation;
    this.width = width;
    this.height = height;
    this.waveX = waveX;
    this.waveY = waveY;
    this.anchorX = anchorX;
    this.anchorY = anchorY;
}
//船舶数据类型,用于船舶图片加载
function Ship(path,width,height,anchorX,anchorY){
  this.stage = stage;
  this.path = path;
  this.anchorX = anchorX;
  this.anchorY = anchorY;
  this.width = width;
  this.height = height;
}
//船舶数据类型,用于船舶位置加载
function ShipPosition(xPosition,yPosition,shipRotation){
    this.shipRotation = shipRotation;
    this.xPosition = xPosition;
    this.yPosition = yPosition;
}
//图片加载进度
function loadProgressHandler(loader, resource) {
  console.log("loading: " + resource.url);
  console.log("progress: " + loader.progress + "%");
}
//碰撞检测函数
function hitTestRectangle(r1, r2) {

  //Define the variables we'll need to calculate
  let hit, combinedHalfWidths, combinedHalfHeights, vx, vy;

  //hit will determine whether there's a collision
  hit = false;

  //Find the center points of each sprite
  r1.centerX = r1.x + r1.width / 2;
  r1.centerY = r1.y + r1.height / 2;
  r2.centerX = r2.x + r2.width / 2;
  r2.centerY = r2.y + r2.height / 2;

  //Find the half-widths and half-heights of each sprite
  r1.halfWidth = r1.width / 2;
  r1.halfHeight = r1.height / 2;
  r2.halfWidth = r2.width / 2;
  r2.halfHeight = r2.height / 2;

  //Calculate the distance vector between the sprites
  vx = r1.centerX - r2.centerX;
  vy = r1.centerY - r2.centerY;

  //Figure out the combined half-widths and half-heights
  combinedHalfWidths = r1.halfWidth + r2.halfWidth;
  combinedHalfHeights = r1.halfHeight + r2.halfHeight;

  //Check for a collision on the x axis
  if (Math.abs(vx) < combinedHalfWidths) {

    //A collision might be occuring. Check for a collision on the y axis
    if (Math.abs(vy) < combinedHalfHeights) {

      //There's definitely a collision happening
      hit = true;
    } else {

      //There's no collision on the y axis
      hit = false;
    }
  } else {

    //There's no collision on the x axis
    hit = false;
  }

  //`hit` will be either `true` or `false`
  return hit;
}
//比例尺
function mapScale(width,height,canvasWidth,canvasHeight){
    let xScale = width /canvasWidth;
    let yScale = height /canvasHeight;
    let scale = xScale < yScale ? xScale : yScale;
    return scale;
}
//计算两个经纬度的距离(千米)
function getDistance(lat1, lng1, lat2, lng2){
    let radLat1 = lat1*Math.PI / 180.0;
    let radLat2 = lat2*Math.PI / 180.0;
    let a = radLat1 - radLat2;
    let b = lng1*Math.PI / 180.0 - lng2*Math.PI / 180.0;
    let s = 2 * Math.asin(Math.sqrt(Math.pow(Math.sin(a/2),2) +
    Math.cos(radLat1)*Math.cos(radLat2)*Math.pow(Math.sin(b/2),2)));
    s = s *6378.137 ;// EARTH_RADIUS;
    s = Math.round(s * 10000) / 10000;
    return s;
}

