/**
 * @file component to enable mouse controls
 * @author Vincent Liu
 */

import React, { useRef } from 'react';
import { useThree, useFrame, extend } from 'react-three-fiber';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';


extend({ OrbitControls });

function Controls() {
    const controls = useRef();
    const { camera, gl } = useThree();

    useFrame(() => controls.current.update());
    return (
        <orbitControls
            ref={controls}
            args={[camera, gl.domElement]} 
            enableKeys={true}
            enableDamping={true}
            dampingFactor={0.1}
            rotateSpeed={0.5} />
    )
}

export default Controls;
