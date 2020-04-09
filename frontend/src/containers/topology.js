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
            let config = await fetch('http://127.0.0.1:5000/topology/' + props.tag);
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
        console.log(config);
        graph = [
            <Nodes
                key={'nodes'}
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
            <Canvas>
                <ambientLight />
                <pointLight color={'white'} position={[0, 0, 50]} castShadow={true} />
                <Controls />
                {graph}
            </Canvas>
        </CanvasContainer>
    )
}

export default Topology;
