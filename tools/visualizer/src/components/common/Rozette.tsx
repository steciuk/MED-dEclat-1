import './Rozette.css';

import React, { ReactNode, useState } from 'react';

import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';

const Rozette = ({
	children,
	title,
	defaultHidden = false,
}: {
	children: ReactNode;
	title: string;
	defaultHidden?: boolean;
}) => {
	const [hidden, setHidden] = useState<boolean>(defaultHidden);

	return (
		<div
			style={{
				height: '100%',
				flexGrow: hidden ? '0' : '1',
				display: 'flex',
				border: 'solid 1px gray',
				flexBasis: '0',
			}}
		>
			<div
				style={{
					width: '1.5rem',
					display: 'flex',
					flexDirection: 'column',
					alignItems: 'center',
					cursor: 'pointer',
					backgroundColor: 'lightgray',
				}}
				onClick={() => setHidden(!hidden)}
			>
				<ArrowForwardIosIcon className={`arrow-icon ${hidden ? 'rotated' : ''}`} />
				<div style={{ writingMode: 'vertical-lr', textAlign: 'center', margin: 'auto 0' }}>
					<b>{title}</b>
				</div>
			</div>
			<div style={{ flexGrow: '1', display: hidden ? 'none' : 'block' }}>{children}</div>
		</div>
	);
};

export default Rozette;
