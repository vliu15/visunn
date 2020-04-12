/**
 * @file container to render the topology feature
 * @author Vincent Liu
 */

import React, { useState, useEffect } from 'react';
import { Canvas } from 'react-three-fiber';

import CanvasContainer from '../components/canvas';
import Nodes from '../components/nodes';
import Edges from '../components/edges';
import Controls from '../components/controls';


const Topology = (props) => {
    let [ready, setReady] = useState(false);
    let [config, setConfig] = useState({});

    // retrieves the metadata corresponding to tag every time tag changes;
    useEffect(() => {
        const getConfig = async () => {
            let tag = props.tag.replace(/\//g, ';');
            let config = await fetch('http://127.0.0.1:5000/topology/' + tag);
            let json = await config.json();
            setConfig(json);
            setReady(true);
        }

        getConfig();
    }, [props.tag]);

    const updateTagHandler = (newTag) => {
        props.tagHandler(newTag)
    }

    let graph = [];
    if (ready) {
        graph = [
            <Nodes
                key={'nodes'}
                meta={config.meta}
                coords={config.coords}
                inputs={config.inputs}
                outputs={config.outputs}
                tag={props.tag}
                tagHandler={updateTagHandler} />,
            <Edges key={'edges'} coords={config.coords} edges={config.edges} />
        ];
    }

    return (
        <CanvasContainer>
            <Canvas camera={{position: [0, 0, 25]}} gl={{physicallyCorrectLights: true}}>
                <ambientLight />
                <pointLight color={'white'} position={[0, 0, 5000]} castShadow={true} />
                {/* <pointLight color={'white'} position={[0, 50, 0]} castShadow={true} /> */}
                <pointLight color={'white'} position={[5000, 0, 0]} castShadow={true} />
                <Controls tag={props.tag}/>
                {graph}
            </Canvas>
        </CanvasContainer>
    )
}

export default Topology;
