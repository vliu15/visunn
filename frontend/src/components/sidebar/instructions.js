/**
 * @file contains card for visuai instructions
 * @author Vincent Liu
 */

import React from 'react';

import { Entry, Card, InlineInfo } from '../div';
import { Title, Header, Info } from '../text';
import * as C from '../../constants';


/**
 * returns card component with `visuai: how to` instructions
 */
const Instructions = () => {
    const convertColor = (hex) => {
        return '#' + hex.toString(16);
    }

    return (
        <Card style={{overflow: 'visible'}}>
            <Entry>
                <Title><strong>visuai</strong>: how to</Title>
            </Entry>
            <Entry>
                <Info><strong>hover</strong> over a node to display its info below</Info>
                <Info><strong>left click</strong> on a module to open its contents</Info>
            </Entry>
            <Entry>
                <Info><strong>left click + drag</strong> to rotate</Info>
                <Info><strong>right click + drag</strong> to pan</Info>
                <Info><strong>scroll</strong> to zoom</Info>
            </Entry>
            <Entry>
                <InlineInfo>
                    <Header style={{color: convertColor(C.MODULE_COLOR)}}>purple</Header>
                    <Info> blocks are op modules</Info>
                </InlineInfo>
                <InlineInfo>
                    <Header style={{color: convertColor(C.INPUT_COLOR)}}>blue</Header>
                    <Info> blocks are input nodes</Info>
                </InlineInfo>
                <InlineInfo>
                    <Header style={{color: convertColor(C.OUTPUT_COLOR)}}>orange</Header>
                    <Info> blocks are output nodes</Info>
                </InlineInfo>
                <InlineInfo>
                    <Header style={{color: convertColor(C.NODE_COLOR)}}>gray</Header>
                    <Info> blocks are op nodes</Info>
                </InlineInfo>
            </Entry>
        </Card>
    );
}

export default Instructions;
