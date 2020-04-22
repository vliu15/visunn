/**
 * @file contains styled div components
 * @author Vincent Liu
 */

import styled from 'styled-components';


export const InlineInfo = styled.div`
    display: flex;
    align-items: center;
    white-space: pre;
    padding: 0;
    margin: 0;
`

export const Entry = styled.div`
    padding: 0.1em 0.5em;
    margin: 0.1em 0.5em;
    text-align: left;
`

export const Card = styled.div`
    margin: 1em;
    padding: 0.5em 0;
    background-color: white;
    border: 2px solid #95AFC0;
    border-radius: 10px;
    overflow: scroll;
`
