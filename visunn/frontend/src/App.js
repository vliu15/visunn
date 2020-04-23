/**
 * @file javascript app main file
 * @author Vincent Liu
 */

import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import './App.css';

import Sidebar from './containers/sidebar';
import Topology from './containers/topology';
import VincentJianLiu from './containers/vincentjianliu';
import * as C from './constants';


export const AppContainer = styled.div`
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    width: 100vw;
    height: 100vh;
`

const App = () => {
    let [tag, setTag] = useState(C.ROOT);
    let [ready, setReady] = useState(false);
    let [config, setConfig] = useState({});
    let [rotation, setRotation] = useState(true);
    let [position, setPosition] = useState(true);
    let [name, setName] = useState(null);

    // retrieve the metadata corresponding to tag
    useEffect(() => {
        const getConfig = async () => {
            let config = await fetch('/api/' + tag);
            let json = await config.json();
            setConfig(json);
            setRotation(true);
            setPosition(true);
            setReady(true);
        }

        getConfig();
    }, [tag]);

    // add event listeners
    useEffect(() => {
        window.addEventListener('mousedown', (e) => {
            if (!e) {
                e = window.event;
            }
            if (e.target && e.target.tagName === 'CANVAS') {
                setRotation(false);
            }
            setPosition(false);
        })
    })

    const type = (name) => {
        if (name === null) {
            return '';
        }
        if (name.slice(-1) === '/') {
            return C.MODULE_TYPE;
        } else if (config.inputs.includes(name)) {
            return C.INPUT_TYPE;
        } else if (config.outputs.includes(name)) {
            return C.OUTPUT_TYPE;
        } else {
            return C.NODE_TYPE;
        }
    }

    return (
        <div className='App'>
            <AppContainer>
                <Sidebar
                    hasPrevious={tag !== C.ROOT}
                    setRotation={setRotation}
                    setPosition={setPosition}
                    tag={tag}
                    setTag={setTag}
                    meta={(ready && (name in config.meta)) ? config.meta[name] : null}
                    type={(type(name))} />
                {ready
                    ? <Topology
                        rotation={rotation}
                        position={position}
                        config={config}
                        setName={setName}
                        setTag={setTag} />
                    : <></>}
                <VincentJianLiu />
            </AppContainer>
        </div>
    );
}

export default App;
