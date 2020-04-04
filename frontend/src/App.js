/**
 * @file javascript app main file
 * @author Vincent Liu
 */

import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import styled from 'styled-components';
import './App.css';

import Sidebar from './containers/sidebar';
import Topology from './containers/topology';
import Toolbar from './containers/toolbar';


const Container = styled.div`
    display: flex;
`

const App = () => {
    return (
        <div className='App'>
            <Router>
                <Toolbar />
                <Switch>
                    <Route exact path='/' />
                    <Route path='/topology/:tag' component={Topology} />
                    <Route path='/metrics' />
                </Switch>
            </Router>
        </div>
    );
}

export default App;
