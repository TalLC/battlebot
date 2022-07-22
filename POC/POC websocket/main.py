import random
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>My first three.js app</title>
		<style>
			body { margin: 0; }
		</style>
	</head>
	<body>
	<script async src="https://unpkg.com/es-module-shims@1.3.6/dist/es-module-shims.js"></script>
    <script type="importmap">
    {
    "imports":  {
                    "three": "https://unpkg.com/three@0.142.0/build/three.module.js"
                }
    }
    </script>
    <script type="module">
            import * as THREE from 'three';
            var ws = new WebSocket("ws://localhost:8000/ws");
            
            
  		    console.log("Script lancer")
			const scene = new THREE.Scene();
			const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

			const renderer = new THREE.WebGLRenderer();
			renderer.setSize( window.innerWidth, window.innerHeight );
			document.body.appendChild( renderer.domElement );

			const geometry = new THREE.BoxGeometry( 1, 1, 1 );
			const material = new THREE.MeshBasicMaterial( { color: 0x0000ff } );
			const cube = new THREE.Mesh( geometry, material );
			scene.add( cube );

			camera.position.z = 5;

			function animate(dep) {
				requestAnimationFrame( animate );
				var cha = dep.split(":");
                var val = parseFloat(cha[1]);
                if (cha[0] == 'x'){
				    cube.rotation.x += val;
				}
				else if (cha[0] == 'y'){
				    cube.rotation.y += val;
				}
				else{
				    cube.rotation.z += val;
                }
				renderer.render( scene, camera );
			};
			
			ws.onmessage = function(event) {
                var dep = event.data;
                animate(dep);
            };

	</script>
	</body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        rand = random.randint(1, 5)
        if rand == 1:
            await websocket.send_text("x:0.5")
        elif rand == 2:
            await websocket.send_text("y:1")
        elif rand == 3:
            await websocket.send_text("z:2.5")
        elif rand == 4:
            await websocket.send_text("x:2.5")
        elif rand == 5:
            await websocket.send_text("y:1.5")