/**
 * @file component to enable mouse controls on canvas
 * @author Vincent Liu
 */

import React, { useRef } from 'react';
import { useThree, useFrame, extend } from 'react-three-fiber';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';


extend({ OrbitControls });

/**
 * component for camera orbitcontrols for three.js
 * 
 * @param {*} props passed from Topology
 */
const Controls = (props) => {
    const controls = useRef();
    const { camera, scene, gl } = useThree();

    if (props.position) {
        camera.position.x = 0;
        camera.position.y = 0;
        camera.position.z = props.z;
    }

    // update controls / rotation
    useFrame(() => {
        controls.current.update();
        if (props.rotation) {
            scene.rotation.y += 0.01;
            if (scene.rotation.y > 2 * Math.PI) {
                scene.rotation.y -= 2 * Math.PI;
            }
        }
    });

    return (
        <orbitControls
            ref={controls}
            args={[camera, gl.domElement]} 
            enableKeys={true}
            enableDamping={true}
            enablePan={true}
            dampingFactor={0.1}
            rotateSpeed={0.75}
            maxPolarAngle={Math.PI * 5/8}
            minPolarAngle={Math.PI * 2/8} />
    )
}

export default Controls;
