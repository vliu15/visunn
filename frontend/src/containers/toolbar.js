/**
 * @file web app toolbar
 * @author Vincent Liu
 */

import React from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom';


// container of toolbar contents
const Container = styled.div`
    display: flex;
    background-color: #6C5CE7;
    justify-content: flex-start;
    align-content: center;
    height: 50px;
    width: 100%;
    margin: 0;
`

// visuai title
const Title = styled.h2`
    font-size: medium;
    font-weight: 600;
    color: #FFFFFF;
    padding: 0px 15px;
    vertical-align: middle;
`

// all other headers
const Header = styled.h2`
    font-size: medium;
    font-weight: 400;
    color: #FFFFFF;
    padding: 0px 15px;
    vertical-align: middle;
`

const Toolbar = () => {
    return (
        <Container>
            <Link to='/' style={{textDecoration: 'none'}}>
                <Title>v i s u a i</Title>
            </Link>
            <Link to='/topology/root' style={{textDecoration: 'none'}}>
                <Header>topology</Header>
            </Link>
            <Link to='/metrics' style={{textDecoration: 'none'}}>
                <Header>metrics</Header>
            </Link>
        </Container>
    )
}

export default Toolbar;
