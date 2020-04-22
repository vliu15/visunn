/**
 * @file contains styled text components
 * @author Vincent Liu
 */

import styled from 'styled-components';


export const Title = styled.h2`
    font-size: large;
    word-wrap: break-word;
    margin: 0;
    &:hover {
        cursor: text;
    }
`

export const Info = styled.p`
    font-size: small;
    word-wrap: break-word;
    padding: 0;
    margin: 0;
    &:hover {
        cursor: text;
    }
`

export const Header = styled.p`
    font-weight: bold;
    font-size: small;
    word-wrap: break-word;
    padding: 0;
    margin: 0;
    &:hover {
        cursor: text;
    }
`

export const Link = styled.a`
    font-size: small;
    word-wrap: break-word;
    padding: 0;
    margin: 0;
    text-decoration: none;
    color: #4834D4;
    &:hover {
        cursor: pointer;
    }
    &:active {
        color: #EB4D4B;
    }
`
