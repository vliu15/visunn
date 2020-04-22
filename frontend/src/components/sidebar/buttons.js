/**
 * @file contains button parts and button compnent
 * @author Vincent Liu
 */

import React from 'react';
import styled from 'styled-components';


// clickable button
const ActiveButton = styled.button`
    width: auto;
    height: auto;
    padding: 1em;
    background-color: #000000;
    border: 2px solid #000000;
    border-radius: 5px;
    color: #FFFFFF;
    font-weight: 600;
    margin: 1em;
    &:hover {
        color: #000000;
        background-color: #DFF9FB;
        cursor: pointer;
    }
`

// unclickable button
const InactiveButton = styled.button`
    width: auto;
    height: auto;
    padding: 1em;
    background-color: #B2BEC3;
    border: 2px solid #B2BEC3;
    border-radius: 5px;
    color: #FFFFFF;
    font-weight: 600;
    margin: 1em;
`

// container for buttons
const Container = styled.div`
    display: flex;
    flex-direction: row;
    order: 1;
    align-items: center;
    justify-content: center;
    margin-bottom: 1em;
`

/**
 * returns a div of buttons for controlling canvas actions
 *
 * @param {*} props passed from Sidebar
 */
const Buttons = (props) => {
    return (
        <Container>
            {(props.hasPrevious)
                ? <ActiveButton id='previousModule'>
                    previous<br />module
                </ActiveButton>
                : <InactiveButton>
                    previous<br />module
                </InactiveButton>}
            <ActiveButton id='rootModule'>
            root<br />module
            </ActiveButton>
            <ActiveButton id='resetRotation'>
                reset<br />rotation
            </ActiveButton>
            <ActiveButton id='resetPosition'>
                reset<br />position
            </ActiveButton>
        </Container>
    );
}

export default Buttons;
