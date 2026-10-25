
const { app, BrowserWindow } = require("electron");
const express = require("express");
const http = require("node:http");
const path = require("node:path");

let server;

async function createWindow() {
  const simulatorDirectory = path.join(__dirname, "simulator");

  const webApp = express();
  webApp.use(express.static(simulatorDirectory));

  server = http.createServer(webApp);

  await new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", resolve);
  });

  const address = server.address();

  if (!address || typeof address === "string") {
    throw new Error("Could not start the local simulator server.");
  }

  const window = new BrowserWindow({
    width: 1440,
    height: 900,
    minWidth: 960,
    minHeight: 640,
    title: "Caelvyr Aeronautical Dynamics",
    backgroundColor: "#07111e",
    autoHideMenuBar: true,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true
    }
  });

  await window.loadURL(
    `http://127.0.0.1:${address.port}/index.html`
  );
}

app.whenReady()
  .then(createWindow)
  .catch((error) => {
    console.error("Caelvyr could not start:", error);
    app.quit();
  });

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("before-quit", () => {
  if (server) {
    server.close();
  }
});
