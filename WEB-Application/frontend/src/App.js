import React from 'react'
import {BrowserRouter, Switch, Route} from 'react-router-dom'
import logo from './logo.svg'
import './App.css'
import { About } from './components/About'
import { Users } from './components/Users'
import { Navbar} from './components/Navbar'

function App() {
	return (
		<BrowserRouter>
			<div>
				<Switch>
					<Route path="/about" component={About} />
					<Route path="/users" component={Users} />
					<Route path="/navbar" component={Navbar} />
				</Switch>
			</div>
		</BrowserRouter>
	);
}

export default App;
