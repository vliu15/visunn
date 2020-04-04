/**
 * @file component to fetch and display graph topology
 * @author Vincent Liu
 */

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Switch, Route, Redirect } from 'react-router-dom';

import Nodes from './nodes';
import Edges from './edges';


const Graph = (props) => {
    let tag = props.tag;
    let [ready, setReady] = useState(false);
    let [config, setConfig] = useState({});

    useEffect(() => {
        const getConfig = async () => {
            let config = await fetch('http://127.0.0.1:5000/topology/' + tag);
            let json = await config.json();
            setConfig(json);
            setReady(true);
        }

        getConfig();
    }, [tag]);


    if (ready) {
        return (
            <>
                <Nodes coords={config.coords} tag={tag} />
                <Edges coords={config.coords} edges={config.edges} />
            </> 
        );
    } else {
        return <></>;
    }
}

export default Graph;
