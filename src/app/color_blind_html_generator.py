def generate_html(text, text_color, background_color):
    return f"""
            <html>
            <style>
                body {{
                    background-color: #d8d6d6;
                    opacity: 0.8;
                }}
                @keyframes tilt-shaking {{
                        0% {{ transform: rotate(0deg); }}
                        25% {{ transform: rotate(5deg); }}
                        50% {{ transform: rotate(0eg); }}
                        75% {{ transform: rotate(-5deg); }}
                        100% {{ transform: rotate(0deg); }}
                        }}
                div {{
                    display: table-cell;
                    animation: tilt-shaking 0.3s infinite;
                    position: absolute;
                    # top:0;
                    # bottom: 0;
                    # left: 0;
                    # right: 0;
                    padding: 10px;
                    margin: auto;
                    border-radius: 25px;
                    border: 2px solid #5A5A5A;
                    width: 90%;
                    height: 90%;
                    background-color: {background_color};
                    }}
                p {{
                    # line-height: normal;
                    # display: inline-block;
                    # vertical-align: middle;
                    text-shadow: -1px 0 black, 0 1px black, 1px 0 black, 0 -1px black;
                    text-align: center;
                    font-weight: 1000;
                    font-size: 20vw;
                    color: {text_color};
                }}

            </style>
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
        <head>
            <title>Sobriety Test</title>
        </head>
        <body>
            <div id="mydiv">
                <p>{text}</p>
            </div>
        </body>

        <script>$('#mydiv').delay(5000).hide(0);</script>

        </html>"""


def landing_page(ws):
    return f"""
    <html>
    <head>
        <title>Sobriety Test</title>
    </head>
    <body>
        <div>
            <h1>You will now play color blind</h1>
        </div>
        <script>
            ws = new WebSocket("{ws}");
            ws.onmessage = function (event) {{
                document.open();
                document.write(event.data);
            }}
        </script>
    </body>
    </html>"""
