import CameraControls from "camera-controls"
import React from "react"
import Stats from "stats.js"
import * as THREE from "three"
import { makeBasePlaneMesh, makeCylMesh, makeSkyMesh } from "./renderables"
import {
  CAMERA_DISTANCE,
  doDispose,
  MAX_RAYCASTER_DISTANCE,
  timeout
} from "./utils"

class Renderer extends React.Component {
  componentDidMount() {
    window.addEventListener("resize", this.onResize)
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this.onResize)

    doDispose(this.scene)

    this.renderer.dispose()
    this.renderer.forceContextLoss()
    this.renderer.context = undefined
    this.renderer.domElement = undefined
  }

  shouldComponentUpdate() {
    return false
  }

  get width() {
    return window.innerWidth - 1
    // return (
    //   (this.rendererRef
    //     ? this.rendererRef.getBoundingClientRect().width
    //     : window.innerWidth) - 1
    // )
  }

  get height() {
    return window.innerHeight - 4
    // return (
    //   (this.rendererRef
    //     ? this.rendererRef.getBoundingClientRect().height
    //     : window.innerHeight) - 4
    // )
  }

  onResize = () => {
    const width = this.width
    const height = this.height
    if (this.camera) {
      this.camera.aspect = width / height
      this.camera.updateProjectionMatrix()
      this.controls.update()
    }
    if (this.renderer) {
      this.renderer.setSize(width, height)
    }
  }

  setupRenderer = ref => {
    this.renderer = new THREE.WebGLRenderer({
      powerPreference: "high-performance",
      antialias: true,
      logarithmicDepthBuffer: true
    })

    this.renderer.setPixelRatio(window.devicePixelRatio)
    this.renderer.setSize(this.width, this.height)
    if (ref) {
      this.rendererRef = ref
      this.rendererRef.appendChild(this.renderer.domElement)
    }
  }

  setupStats = ref => {
    if (ref) {
      this.stats = new Stats()
      this.stats.domElement.style.position = "absolute"
      this.stats.domElement.style.top = "0px"
      this.rendererRef.appendChild(this.stats.domElement)
    }
  }

  setupCamera = () => {
    this.camera = new THREE.PerspectiveCamera(
      70,
      this.width / this.height,
      // 0.1,
      0.01,
      MAX_RAYCASTER_DISTANCE
    )
    this.camera.position.y = CAMERA_DISTANCE
  }

  setupWorld = () => {
    this.scene = new THREE.Scene()

    this.scene.add(makeSkyMesh())

    const ambientLight = new THREE.AmbientLight(0xffffff)
    this.scene.add(ambientLight)

    this.scene.add(makeBasePlaneMesh())

    this.scene.add(...makeCylMesh(15))
  }

  onRendererRef = async ref => {
    this.setupRenderer(ref)
    this.setupStats(ref)
    this.setupCamera()
    this.setupWorld()

    this.dragging = false
    this.clock = new THREE.Clock()
    this.controls = new CameraControls(this.camera, this.renderer.domElement)

    this.renderWebGL()
    await timeout(100)
    this.onResize()
  }

  renderWebGL = () => {
    const delta = this.clock.getDelta()
    this.controls.update(delta)

    window.requestAnimationFrame(this.renderWebGL)

    this.stats.update()
    this.renderer.render(this.scene, this.camera)
  }

  render() {
    return <div ref={this.onRendererRef} />
  }
}

export default Renderer
