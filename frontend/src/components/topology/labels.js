/**
 * @file component to add label above each node
 * @author Vincent Liu
 */

import React from 'react';
import styled from 'styled-components';
import { Dom, useThree } from 'react-three-fiber';

// metadata container
const Container = styled.div`
    text-align: left;
    white-space: pre;
    background-color: #DFF9FB;
    padding: 5px;
    border: 1px solid #C7ECEE;
    border-radius: 2px;
`

// line entry in metadata
const Info = styled.p`
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
    const formatName = () => {
        let name = props.name;
        let isModule = false;
        if (name.slice(-1) === '/') {
            name = name.slice(0, -1);
            isModule = true;
        }
        name = name.split('/');

        let formatted = [];
        for (let i = 0; i < name.length; i++) {
            let line = ' '.repeat(3*i) + name[i];
            if (i < name.length - 1 || isModule) {
                line += '/';
            }
            formatted.push(
                <Info>{line}</Info>
            );
        }
        return formatted;
    }

    // add offset to text labels so that they aren't covering the node
    const { scene, camera } = useThree();
    const xOffset = (camera.rotation.x - scene.rotation.x > 0) ? 1 : -1
    const yOffset = (camera.rotation.y - scene.rotation.y > 0) ? 1 : -1
    const zOffset = (camera.rotation.z - scene.rotation.z > 0) ? 1 : -1

    return (
        <Dom position={[props.x+xOffset, props.y+yOffset, zOffset]}>
            <Container>
                {formatName()}
            </Container>
        </Dom>
    )
}

export default Label;