/**
 * @file javascript app main file
 * @author Vincent Liu
 */

import React, { useState } from 'react';
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';
import './App.css';

import { Toolbar, Title, Header } from './components/toolbar';
import Topology from './containers/topology';


const App = () => {
    let [tag, setTag] = useState('root');

    const updateTag = async (newTag) => {
        setTag(newTag);
    }

    return (
        <div className='App'>
            <Router>
                <Toolbar>
                    <Link to='/' style={{textDecoration: 'none'}}>
                        <Title>v i s u a i</Title>
                    </Link>
                    <Link to='/topology' style={{textDecoration: 'none'}}>
                        <Header onClick={() => setTag('root')}>topology</Header>
                    </Link>
                    <Link to='/metrics' style={{textDecoration: 'none'}}>
                        <Header>metrics</Header>
                    </Link>
                </Toolbar>

                <Switch>
                    <Route exact path='/' />
                    <Route path='/topology'>
                        <Topology tag={tag} tagHandler={updateTag} />
                    </Route>
                    <Route path='/metrics' />
                </Switch>
            </Router>
        </div>
    );
}

export default App;
