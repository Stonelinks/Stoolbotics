import CameraControls from "camera-controls"
import React from "react"
import ReactDOM from "react-dom"
import * as THREE from "three"
import App from "./App"
import "./index.css"

CameraControls.install({ THREE })

ReactDOM.render(<App />, document.getElementById("root"))
