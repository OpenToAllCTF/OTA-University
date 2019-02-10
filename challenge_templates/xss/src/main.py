import os
import secrets
from urllib.parse import parse_qs

import asyncio
from pyppeteer import launch
from quart import render_template, Quart, request, session, send_file

import flag

app = Quart(__name__)

app.config.update({
    "SECRET_KEY": secrets.token_hex(32),
})

@app.route("/")
async def index():
    query = parse_qs(request.query_string)
    if b"xss" in query:
        session["xss"] = query[b"xss"][0].decode()
    return await render_template("index.html")

@app.route("/flag")
async def get_flag():
    return flag.FLAG

@app.route("/source")
async def source():
    return await send_file(__file__)

@app.route("/report", methods=["POST"])
async def report():
    form = await request.form
    if form["url"]:
        asyncio.ensure_future(check_url(form["url"]))
    return "OK"

async def check_url(url):
    task = asyncio.ensure_future(start_browser(url))
    await asyncio.sleep(20)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

async def start_browser(url):
    browser = await launch(**chromium_path(), args=["--no-sandbox"])
    try:
        page = await browser.newPage()
        await page.goto(url)
        await asyncio.sleep(10)
    finally:
        await browser.close()

def chromium_path():
    if os.path.isfile("/usr/bin/chromium"):
        return {"executablePath": "/usr/bin/chromium"}
    return {}

if __name__ == "__main__":
    app.run(port=5000)
