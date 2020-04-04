/**
 * @file container to render the topology feature
 * @author Vincent Liu
 */

import React from 'react';
import { Canvas } from 'react-three-fiber';
import { useParams } from 'react-router-dom';

import CanvasContainer from '../components/canvas';
import Graph from '../components/graph';
import Controls from '../components/controls';


const Topology = () => {
    let { tag } = useParams();

    return (
        <CanvasContainer>
            <Canvas>
                <ambientLight />
                <pointLight color={'white'} position={[0, 0, 50]} castShadow={true} />
                <Controls />
                <Graph tag={tag} />
            </Canvas>
        </CanvasContainer>
    )
}

export default Topology;
