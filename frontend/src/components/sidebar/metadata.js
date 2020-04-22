import React from 'react';
import styled from 'styled-components';

import { Title, Header, Info } from '../text';
import { InlineInfo, Entry, Card } from '../div';
import * as C from '../../constants';

/* styled lists */
const Ul = styled.ul`
    margin: 0;
    padding-left: 20px;
`

const Li = styled.li`
    margin: 0;
    padding: 0;
`

const Container = styled.div`
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: left;
    order: 2;
    overflow: auto;
`

const Instructions = () => {
    const convertColor = (hex) => {
        return '#' + hex.toString(16);
    }

    return (
        <Card style={{overflow: 'visible'}}>
            <Entry>
                <Title>visuai: how to</Title>
            </Entry>
            <Entry>
                <Info><strong>hover</strong> over a node to display its info below</Info>
                <Info><strong>click</strong> on a module to open its contents</Info>
            </Entry>
            <Entry>
                <Info><strong>drag</strong> to rotate</Info>
                <Info><strong>scroll</strong> to zoom</Info>
            </Entry>
            <Entry>
                <InlineInfo>
                    <Header style={{color: convertColor(C.MODULE_COLOR)}}>purple</Header>
                    <Info> blocks are op modules</Info>
                </InlineInfo>
                <InlineInfo>
                    <Header style={{color: convertColor(C.INPUT_COLOR)}}>blue</Header>
                    <Info> blocks are i/o nodes</Info>
                </InlineInfo>
                <InlineInfo>
                    <Header style={{color: convertColor(C.NODE_COLOR)}}>gray</Header>
                    <Info> blocks are op nodes</Info>
                </InlineInfo>
            </Entry>
        </Card>
    )
}

const Metadata = (props) => {
    const getShapes = (key, label) => {
        // make sure this node has a shapes
        if (props.meta[key].length === 0) {
            return <></>;
        }

        const formatShape = (shape) => {
            return '(' + shape.join(', ') + ')';
        }

        // map shapes to text entries
        let shapes = props.meta[key].map(
            (element, idx) =>
                <Li key={idx}><Info>{formatShape(element)}</Info></Li>
        );
        return [
            <Header key='header'>{label}</Header>,
            <Ul key='contents'>{shapes}</Ul>
        ];
    }

    const getInputs = () => {
        if ('input' in props.meta) {
            let inputs = props.meta.input.map(
                (element, idx) => 
                    <Li key={idx}><Info>{element}</Info></Li>
            );

            return [
                <Header key='header'>inputs</Header>,
                <Ul key='contents'>{inputs}</Ul>
            ];
        } else {
            return <></>;
        }
    }

    const getParams = () => {
        // make sure this node has a param attribute
        if (!('params' in props.meta)) {
            return <></>;
        }

        // grab the params
        let params = props.meta.params.map(
            (element, idx) => 
                <Li key={idx}><Info>{element}</Info></Li>
        );
        return [
            <Header key='header'>params</Header>,
            <Ul key='contents'>{params}</Ul>
        ];
    }

    const formatName = () => {
        let name = props.meta.name;
        let isModule = false;
        if (name.slice(-1) === '/') {
            name = name.slice(0, -1);
            isModule = true;
        }
        name = name.split('/');

        let formatted = [];
        for (let i = 0; i < name.length; i++) {
            let line = name[i];
            if (i < name.length - 1 || isModule) {
                line += '/';
            }
            let margin = String(10 * i);
            formatted.push(
                <Info key={i} style={{marginLeft: margin+'px'}}>{line}</Info>
            );
        }
        return formatted;
    }

    let meta = <></>;
    if (props.meta !== null) {
        meta = [
            <Entry key='name'>
                <Header>name</Header>
                {formatName()}
            </Entry>,
            <Entry key='op'>
                <Header>op</Header>
                <Info>{props.meta.op}</Info>
            </Entry>
        ];

        if (props.type !== C.INPUT_TYPE && props.meta.op !== C.PARAM_NODE_OP) {
            meta.push(
                <Entry key='inputs'>
                    {getInputs()}
                </Entry>,
                <Entry key='input shapes'>
                    {getShapes('input_shapes', 'input shapes')}
                </Entry>
            );
        }
        if (props.type !== C.OUTPUT_TYPE && props.meta.op !== C.IO_NODE_OP) {
            meta.push(
                <Entry key='output shapes'>
                    {getShapes('output_shapes', 'output shapes')}
                </Entry>
            );
        }
        if (props.type === C.MODULE_TYPE) {
            meta.push(
                <Entry key='params'>
                    {getParams()}
                </Entry>
            )
        }

        meta = <Card>{meta}</Card>;
    }

    return (
        <Container>
            <Instructions />
            {meta}
        </Container>
    )
}

export default Metadata;
