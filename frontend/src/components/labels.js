/**
 * @file component to add label above each node
 * @author Vincent Liu
 */

import React from 'react';
import styled from 'styled-components';
import { Dom } from 'react-three-fiber';

// metadata container
const Metadata = styled.div`
    text-align: left;
    white-space: pre;
    background-color: #F5F5F5;
    padding: 5px;
    border: 1px solid #DCDCDC;
    border-radius: 2px;
`

// line entry in metadata
const Entry = styled.p`
    font-family: "Courier New", Courier, monospace;
    font-size: small;
    padding: 0;
    margin: 0;
`

const parseOutputShapes = (attrDict, keys) => {
    let outputShapes = [];
    for (let key of keys) {
        for (let shape of attrDict[key]['list']['shape']) {
            let outputShape = [];
            for (let dim of shape['dim']) {
                outputShape.push(dim['size']);
            }
            outputShapes.push('[' + outputShape.join(', ') + ']');
        }
    }
    return outputShapes;
}

/**
 * returns a dom element of metadata label
 * 
 * @param {int} props.x x coordinate of label
 * @param {int} props.y y coordinate of label
 * @param {bool} props.hasInput whether this label should display inputs
 * @param {Object} props.meta contains metadata {name, op, (input)}
 */
const Label = (props) => {
    // format list of inputs (if applicable)
    const getInputs = () => {
        if ('input' in props.meta) {
            return props.meta.input.map(
                (element, idx) => 
                    (idx === 0)
                        ? <Entry key={element}>inputs        : {element}</Entry>
                        : <Entry key={element}>                {element}</Entry>
            );
        } else {
            return <Entry>inputs        : </Entry>;
        }
    }
    const inputs = getInputs();

    const getOutputShapes = () => {
        // make sure this node has an attr object
        if (!('attr' in props.meta)) {
            return <Entry>output shapes : </Entry>;
        }

        // make sure the attr object contains output shapes
        let keys = [];
        for (let key in props.meta.attr) {
            if (key.startsWith('_output_shapes')) {
                keys.push(key);
            }
        }
        if (keys.length === 0) {
            return <Entry>output shapes : </Entry>;
        }

        // map output shapes to text entries
        return parseOutputShapes(props.meta.attr, keys).map(
            (element, idx) =>
                (idx === 0)
                    ? <Entry key={element}>output shapes : {element}</Entry>
                    : <Entry key={element}>                {element}</Entry>
        );
    }
    const outputShapes = getOutputShapes();

    return (
        <Dom position={[props.x, props.y, 0]}>
            <Metadata>
                <Entry>name          : {props.meta.name}</Entry>  
                <Entry>op            : {props.meta.op}</Entry>
                {inputs}
                {outputShapes}
            </Metadata>
        </Dom>
    )
}

export default Label;
