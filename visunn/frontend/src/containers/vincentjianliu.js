/**
 * @file contains component with credits and contact
 * @author Vincent Liu
 */

import React from 'react';
import styled from 'styled-components';

import { Info, Link } from '../components/text';

// vincentjianliu container
const Container = styled.div`
    display: flex;
    flex-direction: column;
    position: absolute;
    align-items: right;
    justify-content: right;
    text-align: right;
    background-color: #F6E58D80;
    right: 0;
    bottom: 0;
    padding: 0.5em;
    border-top-left-radius: 0.5em;
`

/**
 * renders a component with credits and contact in bottom right corner
 */
const VincentJianLiu = () => {
    return (
        <Container>
            <Info><strong>vincent liu</strong>, &copy;2020</Info>
            <div style={{display: 'flex', whiteSpace: 'pre'}}>
                <Link href='mailto:vliu15@stanford.edu'>email</Link>
                <Info> <strong>|</strong> </Info>
                <Link href='https://www.github.com/vliu15/visunn'>github</Link>
            </div>
        </Container>
    );
}

export default VincentJianLiu;
