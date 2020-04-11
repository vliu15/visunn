/**
 * @file web app toolbar components
 * @author Vincent Liu
 */

import styled from 'styled-components';


// container of toolbar contents
export const Toolbar = styled.div`
    display: flex;
    background-color: #6C5CE7;
    justify-content: flex-start;
    align-content: center;
    height: 50px;
    width: 100%;
    margin: 0;
`

// visuai title
export const Title = styled.h2`
    font-size: medium;
    font-weight: 600;
    color: #FFFFFF;
    padding: 0px 15px;
    vertical-align: middle;
`

// all other headers
export const Header = styled.h2`
    font-size: medium;
    font-weight: 400;
    color: #FFFFFF;
    padding: 0px 15px;
    vertical-align: middle;
`
