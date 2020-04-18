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

/**
 * returns a dom element of metadata label
 * 
 * @param {int} props.x x coordinate of label
 * @param {int} props.y y coordinate of label
 * @param {bool} props.showShapes whether this label should display i/o shapes
 * @param {bool} props.showParams whether this label should display parameters
 * @param {Object} props.meta contains metadata {name, op, (input)}
 */
const Label = (props) => {
    // format list of inputs (if applicable)
    const getInputs = () => {
        if ('input' in props.meta) {
            return props.meta.input.map(
                (element, idx) => 
                    (idx === 0)
                        ? <Entry key={idx}>inputs        : {element}</Entry>
                        : <Entry key={idx}>                {element}</Entry>
            );
        } else {
            return <></>;
        }
    }
    
    // get input/output shapes for the node
    const getShapes = (key, label) => {
        // make sure this node has an shapes
        if (props.meta[key].length === 0) {
            return <></>;
        }

        const formatShape = (shape) => {
            return '[' + shape.join(', ') + ']';
        }

        // map shapes to text entries
        return props.meta[key].map(
            (element, idx) =>
                (idx === 0)
                    ? <Entry key={idx}>{label} : {formatShape(element)}</Entry>
                    : <Entry key={idx}>                {formatShape(element)}</Entry>
        );
    }

    // get params for the node
    const getParams = () => {
        // make sure this node has a param attribute
        if (!('params' in props.meta)) {
            return <></>;
        }

        // grab the params
        return props.meta.params.map(
            (element, idx) => 
            (idx === 0)
                ? <Entry key={idx}>params        : {element}</Entry>
                : <Entry key={idx}>                {element}</Entry>
        );
    }

    // format dom elements if the node is considered an input
    const name = (props.showShapes)
        ? <Entry>name          : {props.meta.name}</Entry>
        : <Entry>name : {props.meta.name}</Entry>
    const op = (props.showShapes)
        ? <Entry>op            : {props.meta.op}</Entry>
        : <Entry>op   : {props.meta.op}</Entry>
    const inputs = (props.showShapes)
        ? getInputs()
        : <></>;
    const inputShapes = (props.showShapes)
        ? getShapes('input_shapes', 'input shapes ')
        : <></>;
    const outputShapes = (props.showShapes)
        ? getShapes('output_shapes', 'output shapes')
        : <></>;

    // format dom element if the node is considered a module
    const params = (props.showParams)
        ? getParams()
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
                {params}
            </Metadata>
        </Dom>
    )
}

export default Label;
