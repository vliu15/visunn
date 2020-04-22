/**
 * @file component to render nodes
 * @author Vincent Liu
 */

import React, { useState } from 'react';

import Label from './labels';
import * as C from '../../constants';


/**
 * returns a mesh component corresponding to a node to be drawn on the canvas
 * 
 * @param {*} props props passed from Nodes
 */
const Node = (props) => {
    const [x, y] = props.coords;
    let [hover, setHover] = useState(false);

    // node colors and size
    const [baseColor, hoverColor, size] = (
        (props.type === C.MODULE_TYPE)
            ? [C.MODULE_COLOR, C.MODULE_HOVER_COLOR, C.MODULE_SIZE]
            : (props.type === C.INPUT_TYPE)
                ? [C.INPUT_COLOR, C.INPUT_HOVER_COLOR, C.INPUT_SIZE]
                : (props.type === C.OUTPUT_TYPE)
                    ? [C.OUTPUT_COLOR, C.OUTPUT_HOVER_COLOR, C.OUTPUT_SIZE]
                    : [C.NODE_COLOR, C.NODE_HOVER_COLOR, C.NODE_SIZE]
    );

    const onClick = () => {
        // only modules should have clickable actions
        if (props.type !== C.MODULE_TYPE) {
            return false;
        }
        let host = window.location.hostname;
        let port = window.location.port;
        let href = 'http://' + host + ':' + port + '/' + props.name.slice(0, -1);
        window.location.href = href;
        return true;
    }

    const onPointerOver = (e) => {
        setHover(true);
        if (props.type === C.MODULE_TYPE) {
            document.body.style.cursor = 'pointer';
        }
        props.setName(props.name);
        return true;
    }

    const onPointerOut = (e) => {
        setHover(false);
        if (props.type === C.MODULE_TYPE) {
            document.body.style.cursor = 'default';
        }
        return true;
    }

    return (
        <>
            {hover
                ? <Label
                    name={props.meta.name}
                    op={props.meta.op}
                    x={x}
                    y={y} />
                : <></>}
            <mesh
                position={[x, y, 0]}
                rotation={[0, 0, 0]}
                receiveShadow={true}
                onClick={onClick}
                onPointerOver={onPointerOver}
                onPointerOut={onPointerOut}>
                <boxGeometry
                    attach='geometry'
                    args={size}
                    key={'geo'} />
                <meshLambertMaterial
                    attach='material'
                    color={hover ? hoverColor : baseColor}
                    key={'mat'} />
            </mesh>
        </>
    );
}

/**
 * returns a list of meshes (nodes) to draw on the canvas
 * 
 * @param {*} props passed from Topology
 */
const Nodes = (props) => {
    const type = (name) => {
        if (name.slice(-1) === '/') {
            return C.MODULE_TYPE;
        } else if (props.inputs.includes(name)) {
            return C.INPUT_TYPE;
        } else if (props.outputs.includes(name)) {
            return C.OUTPUT_TYPE;
        } else {
            return C.NODE_TYPE;
        }
    }

    let nodes = Object.keys(props.coords).map(
        (name, idx) =>
            <Node
                key={idx}
                name={name}
                meta={props.meta[name]}
                coords={props.coords[name]}
                type={type(name)}
                setName={props.setName} />
    );
    return nodes;
}

export default Nodes;
