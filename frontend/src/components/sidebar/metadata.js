/**
 * @file contains parts for rendering metadata of hovered node
 * @author Vincent Liu
 */

import React from 'react';
import styled from 'styled-components';

import { Header, Info } from '../text';
import { Entry, Card } from '../div';
import Instructions from './instructions';
import * as C from '../../constants';

// lists for enumerated data
const Ul = styled.ul`
    margin: 0;
    padding-left: 20px;
`

const Li = styled.li`
    margin: 0;
    padding: 0;
`

// container for metadata
const Container = styled.div`
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: left;
    order: 2;
    overflow: auto;
`

/**
 * returns cards containing metadata and `visuai: how to` instructions
 *
 * @param {*} props passed from Sidebar
 */
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
        // all nodes have name and op
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

        // input and param nodes don't show anything about inputs
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

        // output nodes don't show anything about outputs
        if (props.type !== C.OUTPUT_TYPE) {
            meta.push(
                <Entry key='output shapes'>
                    {getShapes('output_shapes', 'output shapes')}
                </Entry>
            );
        }

        // only modules show params
        if (props.type === C.MODULE_TYPE) {
            meta.push(
                <Entry key='params'>
                    {getParams()}
                </Entry>
            );
        }

        meta = <Card>{meta}</Card>;
    }

    return (
        <Container>
            <Instructions />
            {meta}
        </Container>
    );
}

export default Metadata;
