/**
 * @file component to add label above each node
 * @author Vincent Liu
 */

import React from 'react';
import styled from 'styled-components';
import { Dom, useThree } from 'react-three-fiber';

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

const parseShapes = (attrDict, keys) => {
    let shapeStrs = [];
    for (let key of keys) {
        for (let shape of attrDict[key]['list']['shape']) {
            let shapeStr = [];
            for (let dim of shape['dim']) {
                shapeStr.push(dim['size']);
            }
            shapeStrs.push('[' + shapeStr.join(', ') + ']');
        }
    }
    return shapeStrs;
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
    
    // get input/output shapes for the node
    const getShapes = (prefix, label) => {
        // make sure this node has an attr object
        if (!('attr' in props.meta)) {
            return <></>;
        }

        // make sure the attr object contains output shapes
        let keys = [];
        for (let key in props.meta.attr) {
            if (key.startsWith(prefix)) {
                keys.push(key);
            }
        }
        if (keys.length === 0) {
            return <></>;
        }
        // map shapes to text entries
        return parseShapes(props.meta.attr, keys).map(
            (element, idx) =>
                (idx === 0)
                    ? <Entry key={element}>{label} : {element}</Entry>
                    : <Entry key={element}>                {element}</Entry>
        );
    }

    // format dom elements if the node is considered an input
    const name = (!props.isInput)
        ? <Entry>name          : {props.meta.name}</Entry>
        : <Entry>name : {props.meta.name}</Entry>
    const op = (!props.isInput)
        ? <Entry>op            : {props.meta.op}</Entry>
        : <Entry>op   : {props.meta.op}</Entry>
    const inputs = (!props.isInput)
        ? getInputs()
        : <></>;
    const inputShapes = (!props.isInput)
        ? getShapes('_input_shapes', 'input shapes ')
        : <></>;
    const outputShapes = (!props.isInput)
        ? getShapes('_output_shapes', 'output shapes')
        : <></>;

    // add offset to text labels so that they aren't covering the node
    const { scene, camera } = useThree();
    const xOffset = (camera.rotation.x - scene.rotation.x > 0) ? 1 : -1
    const yOffset = (camera.rotation.y - scene.rotation.y > 0) ? 1 : -1
    const zOffset = (camera.rotation.z - scene.rotation.z > 0) ? 1 : -1

    return (
        <Dom position={[props.x+xOffset, props.y+yOffset, zOffset]}>
            <Metadata>
                {name}
                {op}
                {inputs}
                {inputShapes}
                {outputShapes}
            </Metadata>
        </Dom>
    )
}

export default Label;
