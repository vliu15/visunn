/**
 * @file component to render nodes
 * @author Vincent Liu
 */

import React, { useState, useEffect } from 'react';
import { Dom } from 'react-three-fiber';

import { MODULE_COLOR, MODULE_HOVER_COLOR, NODE_COLOR } from '../constants';


const Text = (props) => {
    return (
        <Dom position={[props.x, props.y, 0]}>
            <p>{props.text}</p>
        </Dom>
    )
}

const Node = (props) => {
    let [hover, setHover] = useState(false);
    let tag = props.tag.replace(/\//g, ';').slice(0, -1);
    let baseColor = props.isModule ? MODULE_COLOR : NODE_COLOR;
    let hoverColor = props.isModule ? MODULE_HOVER_COLOR : NODE_COLOR;

    return (
        <>
            <Text text={hover ? props.tag : ''} x={props.x} y={props.y} />
            <mesh
                position={[props.x, props.y, 0]}
                rotation={[0, 0, 0]}
                receiveShadow={true}
                onClick={props.isModule ? () => props.tagHandler(tag) : () => {}}
                onPointerOver={() => setHover(true)}
                onPointerOut={() => setHover(false)}>
                <boxGeometry
                    attach='geometry'
                    args={[1, 1, 1]}
                    key={'geo'} />
                <meshLambertMaterial
                    attach='material'
                    color={hover ? hoverColor : baseColor}
                    key={'mat'} />
            </mesh>
        </>
    );
}

const Nodes = (props) => {
    let nodes = Object.keys(props.coords).map(
        (node) => 
            <Node
                key={node}
                isModule={node.slice(-1) === '/'}
                x={props.coords[node][0]}
                y={props.coords[node][1]}
                tag={'root/' + node} 
                tagHandler={props.tagHandler} />
    );
    return nodes;
}

export default Nodes;
