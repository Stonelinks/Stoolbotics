export const BASE_PLANE_DIMENSION = 100
export const CAMERA_DISTANCE = BASE_PLANE_DIMENSION / 5
export const MAX_RAYCASTER_DISTANCE = 5000

export const timeout = ms => new Promise(resolve => setTimeout(resolve, ms))

export const doDispose = obj => {
  if (obj !== null) {
    for (var i = 0; i < obj.children.length; i++) {
      doDispose(obj.children[i])
    }
    if (obj.geometry) {
      obj.geometry.dispose()
      obj.geometry = undefined
    }
    if (obj.material) {
      if (obj.material.map) {
        obj.material.map.dispose()
        obj.material.map = undefined
      }
      obj.material.dispose()
      obj.material = undefined
    }
  }
  obj = undefined
}
