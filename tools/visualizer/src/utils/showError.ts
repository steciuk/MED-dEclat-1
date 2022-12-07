import { Store } from 'react-notifications-component';

export function showFileError(file: string) {
	Store.addNotification({
		title: 'Invalid file format!',
		message: 'Cannot read file: ' + file,
		type: 'danger',
		insert: 'top',
		container: 'top-right',
		animationIn: ['animate__animated', 'animate__fadeIn'],
		animationOut: ['animate__animated', 'animate__fadeOut'],
		dismiss: {
			duration: 5000,
			onScreen: true,
		},
	});
}
