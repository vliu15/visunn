/**
 * @file component to render edges
 * @author Vincent Liu
 */

import React from 'react';


/**
 * returns a line between to points (edge between nodes)
 * 
 * @param {Array} props.vertices 6-element array of 2 sets of endpoints
 */
const Edge = (props) => {
    const vertices = new Float32Array(props.vertices);
    return (
        <line>
            <bufferGeometry attach='geometry' key={'geo'}>
                <bufferAttribute
                    attachObject={['attributes', 'position']}
                    count={vertices.length/3}
                    array={vertices}
                    itemSize={3} />
            </bufferGeometry>
            <lineBasicMaterial attach='material' color='gray' key={'mat'} />
        </line>
    );
}

/**
 * returns a set of lines to be drawn onto the canvas
 * 
 * @param {Object} props.edges mapping from a node name to a list of its inputs
 * @param {Object} props.coords mapping from a node name to (x,y) coordinates
 */
const Edges = (props) => {
    let parts = [];
    for (let node of Object.keys(props.edges)) {
        let [nodeX, nodeY] = props.coords[node];

        for (let input of props.edges[node]) {
            let [inputX, inputY] = props.coords[input];
            let vertices = [nodeX, nodeY, 0, inputX, inputY, 0];

            parts.push(
                <Edge vertices={vertices} key={input + '->' + node} />
            );
        }
    }

    return parts;
}

export default Edges;
