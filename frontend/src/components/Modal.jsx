import { X } from 'lucide-react'
import React from 'react'
import ReactDOM from 'react-dom'

const Modal = ({ isOpen, onClose, children, width }) => {
	if (!isOpen) return null

	return ReactDOM.createPortal(
		<div
			className='bg-[#00000050] fixed top-0 left-0 right-0 bottom-0 flex justify-center items-center'
			onClick={onClose}
		>
			<div
				className={`bg-[var(--gray)] ${width} p-5 relative rounded-3xl text-[var(--white)]`}
				onClick={e => e.stopPropagation()}
			>
				<X
					className='text-[var(--white)] absolute top-2 right-2 hover:scale-115 cursor-pointer transition-all'
					onClick={onClose}
				/>
				{children}
			</div>
		</div>,
		document.body,
	)
}

const styles = {
	overlay: {
		position: 'fixed',
		top: 0,
		left: 0,
		right: 0,
		bottom: 0,
		backgroundColor: 'rgba(0,0,0,0.7)',
		display: 'flex',
		alignItems: 'center',
		justifyContent: 'center',
		zIndex: 1000,
	},
	content: {
		backgroundColor: '#fff',
		padding: '20px',
		borderRadius: '8px',
		position: 'relative',
		minWidth: '300px',
	},
	closeButton: {
		position: 'absolute',
		top: '10px',
		right: '10px',
		border: 'none',
		background: 'none',
		cursor: 'pointer',
		fontSize: '20px',
	},
}

export default Modal
