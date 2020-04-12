/**
 * @file component to enable mouse controls
 * @author Vincent Liu
 */

import React, { useRef, useState, useEffect } from 'react';
import { useThree, useFrame, extend } from 'react-three-fiber';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';


extend({ OrbitControls });

/**
 * component for camera orbitcontrols for three.js
 * 
 * @param {string} props.tag global module tag, tracked to set default rotation
 */
function Controls(props) {
    // allow user to stop rotation by clicking
    window.addEventListener('mousedown', () => setClicked(true));

    // state control (for auto rotation)
    const [, setTag] = useState();
    const [clicked, setClicked] = useState(false);

    const controls = useRef();
    const { camera, scene, gl } = useThree();

    // update controls / rotation
    useFrame(() => controls.current.update());
    useFrame(() => {
        if (!clicked) {
            scene.rotation.y += 0.01;
            if (scene.rotation.y > 2 * Math.PI) {
                scene.rotation.y -= 2 * Math.PI;
            }
        }
    });

    // reset click state when tag changes
    useEffect(() => {
        setTag(props.tag);
        setClicked(false);
    }, [props.tag]);

    return (
        <orbitControls
            ref={controls}
            args={[camera, gl.domElement]} 
            enableKeys={true}
            enableDamping={true}
            dampingFactor={0.1}
            rotateSpeed={0.75} />
    )
}

export default Controls;
