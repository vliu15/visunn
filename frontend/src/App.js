/**
 * @file javascript app main file
 * @author Vincent Liu
 */

import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import './App.css';

import Sidebar from './containers/sidebar';
import Topology from './containers/topology';
import * as C from './constants';
import { ROOT } from './constants';


export const AppContainer = styled.div`
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    width: 100vw;
    height: 100vh;
`

const App = () => {
    // retrieve the metadata corresponding to tag
    useEffect(() => {
        const getConfig = async () => {
            let tag = window.location.pathname;
            if (tag === '/') {
                tag += ROOT;
            } else {
                tag = '/' + tag.slice(1).replace(/\//g, ';');
            }

            let config = await fetch('http://127.0.0.1:5000/topology' + tag);
            let json = await config.json();
            setConfig(json);
            setReady(true);
        }

        getConfig();
    }, []);

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

    let [ready, setReady] = useState(false);
    let [config, setConfig] = useState({});
    let [rotation, setRotation] = useState(true);
    let [position, setPosition] = useState(false);
    let [name, setName] = useState(null);

    return (
        <div className='App'>
            <AppContainer>
                <Sidebar
                    hasPrevious={window.location.pathname !== '/'}
                    setRotation={setRotation}
                    setPosition={setPosition}
                    meta={(ready && name !== null) ? config.meta[name] : null}
                    type={(type(name))} />
                {ready
                    ? <Topology
                        rotation={rotation}
                        position={position}
                        config={config}
                        setName={setName} />
                    : <></>}
            </AppContainer>
        </div>
    );
}

export default App;
