import * as THREE from "three"
import Sky from "three-sky"
import { BASE_PLANE_DIMENSION } from "./utils"

export const makeSkyMesh = () => {
  // sky
  const sky = new Sky()
  sky.scale.setScalar(10 * BASE_PLANE_DIMENSION)

  const uniforms = sky.material.uniforms
  uniforms.turbidity.value = 5.1
  uniforms.rayleigh.value = 2.116
  uniforms.luminance.value = 1
  uniforms.mieCoefficient.value = 0.003
  uniforms.mieDirectionalG.value = 0.984

  const inclination = 0.45
  const azimuth = 0.25
  const theta = Math.PI * (inclination - 0.5)
  const phi = 2 * Math.PI * (azimuth - 0.5)

  let sunPosition = new THREE.Vector3()
  sunPosition.x = BASE_PLANE_DIMENSION * Math.cos(phi)
  sunPosition.y = BASE_PLANE_DIMENSION * Math.sin(phi) * Math.sin(theta)
  sunPosition.z = BASE_PLANE_DIMENSION * Math.sin(phi) * Math.cos(theta)
  uniforms.sunPosition.value.copy(sunPosition)
  // sky.position.copy(normalizeSceneCoords(dsmLayer))

  return sky
}

export const makeBasePlaneMesh = () => {
  const basePlaneGeom = new THREE.PlaneBufferGeometry(
    BASE_PLANE_DIMENSION * 10,
    BASE_PLANE_DIMENSION * 10,
    100,
    100
  )
  const basePlaneMat = new THREE.MeshBasicMaterial({
    opacity: 0,
    // transparent: true,
    wireframe: true
  })

  const plane = new THREE.Mesh(basePlaneGeom, basePlaneMat)
  plane.rotation.x = -0.5 * Math.PI
  // plane.position.copy(normalizeSceneCoords(dsmLayer))
  return plane
}

export const makeCylMesh = (radius = 5, height = 20) => {
  const ret = []
  const cylGeometry = new THREE.CylinderGeometry(radius, radius, height, 32)
  const cylMaterial = new THREE.MeshToonMaterial({
    color: 0xffff00
  })
  const cylMesh = new THREE.Mesh(cylGeometry, cylMaterial)
  ret.push(cylMesh)
  const cylCapGeometry = new THREE.TorusGeometry(radius, 0.1, 5, 32)
  const cylCapMaterial = new THREE.MeshToonMaterial({
    color: 0x000000
  })
  const cylCapTopMesh = new THREE.Mesh(cylCapGeometry, cylCapMaterial)
  cylCapTopMesh.rotation.x = -0.5 * Math.PI
  cylCapTopMesh.position.y = cylCapTopMesh.position.y - height / 2
  ret.push(cylCapTopMesh)
  const cylCapBottomMesh = new THREE.Mesh(cylCapGeometry, cylCapMaterial)
  cylCapBottomMesh.rotation.x = -0.5 * Math.PI
  cylCapBottomMesh.position.y = cylCapBottomMesh.position.y + height / 2
  ret.push(cylCapBottomMesh)
  return ret
}
