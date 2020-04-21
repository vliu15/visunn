import React from 'react';
import styled from 'styled-components';


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

const Container = styled.div`
    display: flex;
    flex-direction: row;
    order: 1;
    align-items: center;
    justify-content: center;
`

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
            <ActiveButton id='resetRotation'>
                reset<br />rotation
            </ActiveButton>
            <ActiveButton id='resetPosition'>
                reset <br />position
            </ActiveButton>
        </Container>
    )
}

export default Buttons
