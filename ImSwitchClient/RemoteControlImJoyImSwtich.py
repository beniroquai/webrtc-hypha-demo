import numpy as np
import matplotlib.pyplot as plt
import base64
import skimage
import io

import io
import imageio


from imjoy_rpc.hypha import connect_to_server

server = await connect_to_server(
    {"name": "test client", "server_url": "https://ai.imjoy.io"}
)

public_services = await server.list_services("public")
svc_info = list(filter(lambda service: service["type"] == "test-display", public_services))[-1]
svc = await server.get_service(svc_info)

await svc.show_status('hello from python')


image = skimage.data.astronaut()
plt.imshow(image)
plt.show()



with io.BytesIO() as output:
    imageio.imwrite(output, np.random.randn(100,100), format='png')
    output.seek(0)
    data = output.read()
    result = base64.b64encode(data).decode('ascii')
    encoded_image = 'data:image/png;base64,' + result

await svc.display_image(encoded_image)



#!pip install Pyro5
#!pip install useq-schema
import Pyro5.api
from _serialize import register_serializers

register_serializers()
uri = 'PYRO:ImSwitchServer@0.0.0.0:54333'
imswitchServer = Pyro5.api.Proxy(uri)
imswitchServer.exec("ViewController", "liveview", [True])
#imswitchServer.exec("ViewController", "liveview", [False])


while(1):
    with io.BytesIO() as output:
        image = np.uint8(imswitchServer.get_image())
        imageio.imwrite(output, image, format='png')
        output.seek(0)
        data = output.read()
        result = base64.b64encode(data).decode('ascii')
        encoded_image = 'data:image/png;base64,' + result

    await svc.display_image(encoded_image)
    
    
'''
<docs lang="markdown">
[TODO: write documentation for this plugin.]
</docs>
​
<config lang="json">
{
  "name": "HyphaDemo",
  "type": "window",
  "tags": [],
  "ui": "",
  "version": "0.1.0",
  "cover": "",
  "description": "[TODO: describe this plugin with one sentence.]",
  "icon": "extension",
  "inputs": null,
  "outputs": null,
  "api_version": "0.1.8",
  "env": "",
  "permissions": [],
  "requirements": ["https://cdn.jsdelivr.net/npm/imjoy-rpc@0.5.6/dist/hypha-rpc-websocket.min.js"],
  "dependencies": [],
  "defaults": {"w": 20, "h": 10}
}
</config>
​
<script lang="javascript">
​
async function setupHypha(){
    const server = await hyphaWebsocketClient.connectToServer({"name": "js-client", "server_url": "https://ai.imjoy.io", "method_timeout": 10})
    const clients = [];
    await server.register_service(
        {
            "id": "display-image",
            "config":{
                "visibility": "public"
            },
            "type": "test-display",
            show_status( data ){
                console.log("this is your data: ", data)
                const statusElem = document.getElementById("status");
                statusElem.innerHTML = data;
            },
            display_image(img) {
                const imgElem = document.getElementById("img");
                imgElem.src = img;
            },
            add_button(name, svc_led){
                const buttonsElem = document.getElementById("buttons");
                const btn = document.createElement("button")
                btn.innerHTML = name;
                btn.onclick = async ()=>{
                    await svc_led.turn_on()
                }
                buttonsElem.appendChild(btn)
            }
        }
    )
}
​
class ImJoyPlugin {
  async setup() {
    await setupHypha()
  }
}
​
api.export(new ImJoyPlugin())
</script>
​
<window lang="html">
  <div>
    <h1 id="status">Ready<h1>
    <img id="img">
    <div id="buttons"></div>
  </div>
</window>
​
<style lang="css">
​
</style>


'''

