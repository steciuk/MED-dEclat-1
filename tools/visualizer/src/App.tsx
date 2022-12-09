import 'react-notifications-component/dist/theme.css';

import React from 'react';
import { ReactNotifications } from 'react-notifications-component';

import Application from './Application';

function App() {
	return (
		<>
			<ReactNotifications />
			<Application />
		</>
	);
}

export default App;
