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
        if (props.hasInput) {
            return props.meta.input.map(
                (element) => <Entry key={element}>         {element}</Entry>
            );
        } else {
            return <></>;
        }
    }
    const inputs = getInputs();

    return (
        <Dom position={[props.x, props.y, 0]}>
            <Metadata>
                <Entry>name   : {props.meta.name}</Entry>
                <Entry>op     : {props.meta.op}</Entry>
                <Entry>inputs :</Entry>
                {inputs}
            </Metadata>
        </Dom>
    )
}

export default Label;
