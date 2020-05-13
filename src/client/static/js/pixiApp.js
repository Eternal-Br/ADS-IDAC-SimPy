//Aliases
let Application = PIXI.Application,
    Container = PIXI.Container,
    loader = PIXI.loader,
    resources = PIXI.loader.resources,
    TextureCache = PIXI.utils.TextureCache,
    Sprite = PIXI.Sprite;

//Create a Pixi Application
let app = new Application({
    width: 1000,
    height: 380,
    antialiasing: true,
    transparent: false,
    resolution: 1
  }
);

//Add the canvas that Pixi automatically created for you to the HTML document
document.getElementById('map').appendChild(app.view);

 let appStage = new Container();


loader
    .add(["../static/res/sea.jpg"
    ,"../static/res/ship/ship.png"
    ,"../static/res/wave.png"
    ])
    .on("progress", loadProgressHandler)
    .load(loadingFinish);

//Define any variables that are used in more than one function
let ship,wave;
let shipWave = new Container();

function loadingFinish() {

   let bg = new Sprite(resources["../static/res/sea.jpg"].texture);
   bg.width = 1000;
   bg.height = 380;
  //Create the `cat` sprite
  ship = new Sprite(resources["../static/res/ship/ship.png"].texture);
  ship.anchor.set(0,0.5);
  ship.rotation = -0.3;
  ship.x = 0;
  ship.y = 380;
  ship.width = 200;
  ship.height = 50;

  wave = new Sprite(resources["../static/res/wave.png"].texture);
  wave.anchor.set(1,0.5);
  wave.rotation = -0.3;
  wave.x = 85;
  wave.y = 348;
  wave.width = 1000;
  wave.height = 50;

  shipWave.addChild(ship);
  shipWave.addChild(wave);

  app.stage.addChild(bg);
  app.stage.addChild(shipWave);

  app.ticker.add(delta => shipMove(delta));

}

function shipMove(delta){
    shipWave.x += 0.5;
    shipWave.y -= 0.15;
}

function loadProgressHandler(loader, resource) {
  console.log("loading: " + resource.url);
  console.log("progress: " + loader.progress + "%");
}
