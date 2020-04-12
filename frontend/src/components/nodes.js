/**
 * @file component to render nodes
 * @author Vincent Liu
 */

import React, { useState } from 'react';

import Label from './labels';
import * as C from '../constants';


const Node = (props) => {
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

    // node position
    const [x, y] = props.coords;

    // parent state update handler
    const onClickHandler = (e) => {
        if (props.type === C.MODULE_TYPE) {
            return props.tagHandler(props.name);
        }
    }

    return (
        <>
            {hover
                ? <Label
                    meta={props.meta}
                    x={x+2}
                    y={y+2} />
                : <></>}
            <mesh
                position={[x, y, 0]}
                rotation={[0, 0, 0]}
                receiveShadow={true}
                onClick={onClickHandler}
                onPointerOver={() => setHover(true)}
                onPointerOut={() => setHover(false)}>
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
 * returns a list of nodes to draw on canvas
 * 
 * @param {Array} props.inputs list of input node names
 * @param {Array} props.outputs list of output node names
 * @param {Object} props.coords mapping of name to (x,y) coordinates
 * @param {Object} props.meta mapping of name to metadata Object
 * @param {function} props.tagHandler callback to update parent state
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
        (name) =>
            <Node
                key={name}
                name={name}
                meta={props.meta[name]}
                coords={props.coords[name]}
                type={type(name)}
                tagHandler={props.tagHandler} />
    );
    return nodes;
}

export default Nodes;
