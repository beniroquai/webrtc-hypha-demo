import asyncio
from imjoy_rpc.hypha import connect_to_server

async def start_service(client_id, service_id, workspace=None, token=None):
    print(f"Starting service...")
    api = await connect_to_server(
        {
            "client_id": client_id,
            "server_url": "https://ai.imjoy.io/",
            "workspace": workspace,
            "token": token,
        }
    )
    # print("Workspace: ", workspace, "Token:", await api.generate_token({"expires_in": 3600*24*100}))
    await api.register_service(
        {
            "id": service_id,
            "config": {
                "visibility": "public",
            },
            "hello": lambda name: f"Hello, {name}!",
        }
    )
    
    print(
        f"Service (client_id={client_id}) started successfully, available at https://ai.imjoy.io/{api.config.workspace}/services"
    )
    
    print(f"Execute the service via HTTP proxy, example: https://ai.imjoy.io/{api.config.workspace}/services/hello-service/hello?name=John")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    workspace = None
    token = None
    loop.create_task(
        start_service(
            "hello-client",
            "hello-service",
            workspace=workspace,
            token=token,
        )
    )
    loop.run_forever()