/**
 * @file container to render the topology feature
 * @author Vincent Liu
 */

import React from 'react';
import styled from 'styled-components';
import { Canvas } from 'react-three-fiber';

import Nodes from '../components/topology/nodes';
import Edges from '../components/topology/edges';
import Controls from '../components/topology/controls';


const Container = styled.div`
    position: relative;
    max-height: 100vh;
    max-width: calc(100vw - 25em);
    width: 100%;
    height: 100%;
`

/**
 * returns the canvas and all its elements draw on it
 * 
 * @param {Object} props.config config data from backend
 */
const Topology = (props) => {
    return (
        <Container>
            <Canvas
                camera={{position: [0, 0, 25]}}
                gl={{physicallyCorrectLights: true}}>
                <ambientLight intensity={0.75} />
                <pointLight position={[0, 0, 5000]} intensity={0.75} castShadow={true} />
                <pointLight position={[0, 0, -5000]} intensity={0.75} castShadow={true} />
                <pointLight position={[5000, 0, 0]} intensity={0.5} castShadow={true} />
                <pointLight position={[-5000, 0, 0]} intensity={0.5} castShadow={true} />
                <pointLight position={[0, 5000, 0]} intensity={0.25} castShadow={true} />
                <pointLight position={[0, -5000, 0]} intensity={0.25} castShadow={true} />
                <Controls rotation={props.rotation} tag={props.tag} position={props.position} />

                <Nodes
                    key={'nodes'}
                    meta={props.config.meta}
                    coords={props.config.coords}
                    inputs={props.config.inputs}
                    outputs={props.config.outputs}
                    setName={props.setName} />
                <Edges
                    key={'edges'}
                    coords={props.config.coords}
                    edges={props.config.edges} />
            </Canvas>
        </Container>
    )
}

export default Topology;
