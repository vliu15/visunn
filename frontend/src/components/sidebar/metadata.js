import React from 'react';
import styled from 'styled-components';

import * as C from '../../constants';

/* styled text */
const Title = styled.h2`
    font-size: large;
    word-wrap: break-word;
    margin: 0;
`

const Info = styled.p`
    font-size: small;
    word-wrap: break-word;
    padding: 0;
    margin: 0;
`

const BoldInfo = styled.p`
    font-weight: bold;
    font-size: small;
    word-wrap: break-word;
    padding: 0;
    margin: 0;
`

/* styled lists */
const Ul = styled.ul`
    margin: 0;
    padding-left: 20px;
`

const Li = styled.li`
    margin: 0;
    padding: 0;
`

/* styled divs */
const InlineInfo = styled.div`
    display: flex;
    align-items: center;
    white-space: pre;
    padding: 0;
    margin: 0;
`

const Entry = styled.div`
    padding: 0.25em 1em;
    text-align: left;
`

const Card = styled.div`
    margin: 1em;
    padding: 0.5em 0;
    background-color: white;
    border: 2px solid #95AFC0;
    border-radius: 10px;
    overflow: scroll;
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
                    <BoldInfo style={{color: convertColor(C.MODULE_COLOR)}}>purple</BoldInfo>
                    <Info> blocks are op modules</Info>
                </InlineInfo>
                <InlineInfo>
                    <BoldInfo style={{color: convertColor(C.INPUT_COLOR)}}>yellow</BoldInfo>
                    <Info> blocks are i/o nodes</Info>
                </InlineInfo>
                <InlineInfo>
                    <BoldInfo style={{color: convertColor(C.NODE_COLOR)}}>gray</BoldInfo>
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
                <Li><Info key={idx}>{formatShape(element)}</Info></Li>
        );
        return [<BoldInfo>{label}</BoldInfo>, <Ul>{shapes}</Ul>];
    }

    const getInputs = () => {
        if ('input' in props.meta) {
            let inputs = props.meta.input.map(
                (element, idx) => 
                    <Li><Info key={idx}>{element}</Info></Li>
            );
            return [<BoldInfo>inputs</BoldInfo>, <Ul>{inputs}</Ul>];
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
                <Li><Info key={idx}>{element}</Info></Li>
        );
        return [<BoldInfo>params</BoldInfo>, <Ul>{params}</Ul>];
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
                <Info style={{marginLeft: margin+'px'}}>{line}</Info>
            );
        }
        return formatted;
    }

    let meta = <></>;
    if (props.meta !== null) {
        meta = [
            <Entry>
                <BoldInfo>name</BoldInfo>
                {formatName()}
            </Entry>,
            <Entry>
                <BoldInfo>op</BoldInfo>
                <Info>{props.meta.op}</Info>
            </Entry>
        ];

        if (props.type !== C.INPUT_TYPE && props.meta.op !== C.PARAM_NODE_OP) {
            meta.push(
                <Entry>
                    {getInputs()}
                </Entry>,
                <Entry>
                    {getShapes('input_shapes', 'input shapes')}
                </Entry>
            );
        }
        if (props.type !== C.OUTPUT_TYPE && props.meta.op !== C.IO_NODE_OP) {
            meta.push(
                <Entry>
                    {getShapes('output_shapes', 'output shapes')}
                </Entry>
            );
        }
        if (props.type === C.MODULE_TYPE) {
            meta.push(
                <Entry>
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
