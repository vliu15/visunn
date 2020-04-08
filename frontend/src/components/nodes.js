/**
 * @file component to render nodes
 * @author Vincent Liu
 */

import React, { useState, useEffect } from 'react';
import { Dom } from 'react-three-fiber';


const Text = (props) => {
    return (
        <Dom position={[props.x, props.y, 0]}>
            <p>{props.text}</p>
        </Dom>
    )
}

const Node = (props) => {
    let [hover, setHover] = useState(false);
    let [active, setActive] = useState(false);
    let tag = props.tag.replace(/\//g, ';').slice(0, -1);

    useEffect(() => {
        props.tagHandler(tag);
        setActive(false);
    }, [active]);

    return (
        <>
            <Text text={hover ? props.tag : ''} x={props.x} y={props.y} />
            <mesh
                position={[props.x, props.y, 0]}
                rotation={[0, 0, 0]}
                receiveShadow={true}
                // onClick={props.isModule ? () => props.tagHandler(tag) : () => {}}
                onClick={props.isModule ? () => setActive(true) : () => {}}
                onPointerOver={() => setHover(true)}
                onPointerOut={() => setHover(false)}>
                <boxGeometry
                    attach='geometry'
                    args={[1, 1, 1]}
                    key={'geo'} />
                <meshLambertMaterial
                    attach='material'
                    color={hover ? 0x00cec9 : 0x6c5ce7}
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
