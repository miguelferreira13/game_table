from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

import argparse
from config import config
from random import choice
import os

from color_blind_html_generator import generate_html, landing_page
from notifier import Notifier
from util.color_blind_generator import generate_combinations, COLOR_TRANSLATIONS


notifier = Notifier()

origins = ["*"]

app = FastAPI(title='game_table',
              redoc_url='/game_table/docs',
              openapi_url='/game_table/openapi.json')


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/game_table", response_class=HTMLResponse)
async def main_page():

    return landing_page()


@app.get("/game_table/{winning_color}", response_class=HTMLResponse)
async def push_html(request: Request, winning_color: str):

    if winning_color == "loser":
        html = generate_html("LOSER!", "red", "white")
        await notifier.push(html)
        return
    if winning_color not in all_combinations.keys():
        raise HTTPException(status_code=404, detail=f"Supported colors: {list(all_combinations.keys())}")

    html = generate_html(*choice(all_combinations[winning_color]))
    await notifier.push(html)


@app.websocket(f"/{config.ws_type}")
async def websocket_endpoint(websocket: WebSocket):
    await notifier.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)
    except WebSocketDisconnect:
        notifier.remove(websocket)


@app.on_event("startup")
async def startup():
    # Prime the push notification generator
    await notifier.generator.asend(None)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Beer Table API')
    parser.add_argument('--language', '-c',
                        dest='language',
                        type=str, default='EN',
                        help='Language code (default: EN)',
                        choices=list(COLOR_TRANSLATIONS.keys())
                        )
    args = parser.parse_args()
    language_code = args.language

    try:
        all_combinations = generate_combinations(language_code)
    except KeyError:
        raise KeyError(f"Supported languages: {list(COLOR_TRANSLATIONS.keys())}")

    uvicorn.run(app, host="0.0.0.0", port=config.port,
                ssl_keyfile=os.getenv("SSL_KEYFILE"),
                ssl_certfile=os.getenv("SSL_CERTFILE"))
