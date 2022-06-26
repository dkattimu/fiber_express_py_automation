import express from "express";

import { readFile } from "fs/promises";
import {readFileSync} from "fs"


const app = express();
const configPath = "./../automation.config.json"
const dataPath = "./data.json";

app.set("view engine", "pug");

const getData = async (location) => {
  try {
      const jsonData = await readFile(location, 'utf8')
      const data = JSON.parse(jsonData);
      return data;
  } catch (e) {
    console.log(`Oops! ${e}`);
  }
};

const config = JSON.parse(readFileSync(configPath, 'utf8')) // need this to complete before we proceed
//
//console.log(`config: ${config.PORTS.VIEW_ENGINE}`)
const PORT = parseInt(config.PORTS.VIEW_ENGINE)||50003


app.use((req, res, next) => {
  console.log(`Received ${req.method} at: ${Date()}`);
  next();
});

app.get("/", async (req, res) => {
  const data = await getData(dataPath);
  const _time = Date().toString()
  res.render("index", {
    modelInfos: data.models,
    time: _time,
  });
});

app.listen(PORT, () => {
   console.log(`View Engine Server Started.... ${Date()} at localhost:${PORT}`)
})
