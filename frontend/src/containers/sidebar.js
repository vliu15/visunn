/**
 * @file contains the sidebar component
 * @author Vincent Liu
 */

import React, { useEffect } from 'react';
import styled from 'styled-components';

import Buttons from '../components/sidebar/buttons';
import Metadata from '../components/sidebar/metadata';


// sidebar container
const Container = styled.div`
    position: relative;
    max-height: 100vh;
    max-width: 100vw;
    height: 100%;
    width: 25em;
    display: flex;
    flex-direction: column-reverse;
    background-color: #DFF9FB;
    border-color: #C7ECEE;
    border: none;
`

/**
 * returns sidebar, which contains buttons and instruction + data cards
 *
 * @param {*} props passed from App
 */
const Sidebar = (props) => {
    // add onclick event handlers
    useEffect(() => {
        let previousModule = document.getElementById('previousModule');
        let resetRotation = document.getElementById('resetRotation');
        let resetPosition = document.getElementById('resetPosition');

        if (previousModule !== null) {
            previousModule.onclick = () => {
                let path = window.location.pathname;
                path = path.substring(0, path.lastIndexOf('/'));
                window.location.pathname = path;
                return true;
            }
        }
        resetRotation.onclick = () => {
            props.setRotation(true);
            return true;
        }
        resetPosition.onclick = () => {
            props.setPosition(true);
            return true;
        }
    });

    return (
        <Container>
            <Buttons hasPrevious={props.hasPrevious} />
            <Metadata meta={props.meta} type={props.type} />
        </Container>
    );
}

export default Sidebar;
