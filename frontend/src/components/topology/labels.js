/**
 * @file component to add label above each node
 * @author Vincent Liu
 */

import React from 'react';
import styled from 'styled-components';
import { Dom, useThree } from 'react-three-fiber';

import { Info } from '../text';


// label container
const Container = styled.div`
    text-align: left;
    white-space: pre;
    background-color: #DFF9FB;
    padding: 0.5em;
    border: 1px solid #C7ECEE;
    border-radius: 5px;
`

/**
 * returns a dom element of metadata label
 * 
 * @param {*} props passed from Node
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
                <Info key={i}>{line}</Info>
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
    );
}

export default Label;
