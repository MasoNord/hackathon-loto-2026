export const SubmitButton = ({
	onClick,
	icon: Icon,
	title,
	IconColor,
	disabled = false,
}) => {
	return (
		<button
			disabled={disabled}
			onClick={onClick}
			className={`${
				!disabled
					? 'active:scale-99 active:brightness-90 hover:bg-[var(--hero-epta)] hover:text-white  cursor-pointer'
					: 'opacity-25 cursor-not-allowed'
			} bg-[var(--black)] text-[var(--white)] rounded-xl h-full flex gap-4 items-center justify-center transition-all py-4`}
		>
			{Icon && <Icon size={size / 1.75 || 24} color={IconColor} />}
			{title && (
				<span className='font-medium truncate text-ellipsis'>{title}</span>
			)}
		</button>
	)
}

import { NavLink } from 'react-router-dom'
import styled from 'styled-components'

export const SpecialButton = ({ title, to }) => {
	return (
		<StyledWrapper>
			<NavLink to={to}>
				<button className='cursor-pointer'>{title}</button>
			</NavLink>
		</StyledWrapper>
	)
}

export const SpecialButton2 = ({ title, onClick }) => {
	return (
		<StyledWrapper2>
			<button onClick={onClick} className='cursor-pointer'>
				{title}
			</button>
		</StyledWrapper2>
	)
}

export const SpecialButton3 = ({ title, onClick }) => {
	return (
		<StyledWrapper3>
			<button onClick={onClick} className='cursor-pointer'>
				{title}
			</button>
		</StyledWrapper3>
	)
}

const StyledWrapper3 = styled.div`
	button {
		width: 100%;
		position: relative;
		padding: 6px;
		border-radius: 12px;
		background: var(--gray-very-lighter);
		font-size: 16px;
		text-transform: uppercase;
		font-weight: 400;
		letter-spacing: 2px;
		color: var(--white);
		overflow: hidden;
		box-shadow: 0 0 0 0 transparent;
		-webkit-transition: all 0.2s ease-in;
		-moz-transition: all 0.2s ease-in;
		transition: all 0.2s ease-in;
	}

	button:hover {
		background: rgb(43, 186, 243);
		box-shadow: 0 0 30px 5px rgba(83, 196, 283, 0.175);
		-webkit-transition: all 0.2s ease-out;
		-moz-transition: all 0.2s ease-out;
		transition: all 0.2s ease-out;
	}

	button:hover::before {
		-webkit-animation: sh02 0.5s 0s linear;
		-moz-animation: sh02 0.5s 0s linear;
		animation: sh02 0.5s 0s linear;
	}

	button::before {
		content: '';
		display: block;
		width: 0px;
		height: 86%;
		position: absolute;
		top: 7%;
		left: 0%;
		opacity: 0;
		background: #fff;
		box-shadow: 0 0 50px 30px #fff;
		-webkit-transform: skewX(-20deg);
		-moz-transform: skewX(-20deg);
		-ms-transform: skewX(-20deg);
		-o-transform: skewX(-20deg);
		transform: skewX(-20deg);
	}

	@keyframes sh02 {
		from {
			opacity: 0;
			left: 0%;
		}

		50% {
			opacity: 1;
		}

		to {
			opacity: 0;
			left: 100%;
		}
	}

	button:active {
		box-shadow: 0 0 0 0 transparent;
		-webkit-transition: box-shadow 0.2s ease-in;
		-moz-transition: box-shadow 0.2s ease-in;
		transition: box-shadow 0.2s ease-in;
	}
`

const StyledWrapper2 = styled.div`
	button {
		width: 100%;
		position: relative;
		padding: 12px;
		border-radius: 18px;
		border: 1px solid rgb(43, 186, 243);
		background: rgb(43, 186, 243);
		font-size: 16px;
		text-transform: uppercase;
		font-weight: 600;
		letter-spacing: 2px;
		color: #fff;
		overflow: hidden;
		box-shadow: 0 0 0 0 transparent;
		-webkit-transition: all 0.2s ease-in;
		-moz-transition: all 0.2s ease-in;
		transition: all 0.2s ease-in;
	}

	button:hover {
		background: rgb(43, 186, 243);
		box-shadow: 0 0 30px 5px rgba(83, 196, 283, 0.175);
		-webkit-transition: all 0.2s ease-out;
		-moz-transition: all 0.2s ease-out;
		transition: all 0.2s ease-out;
	}

	button:hover::before {
		-webkit-animation: sh02 0.5s 0s linear;
		-moz-animation: sh02 0.5s 0s linear;
		animation: sh02 0.5s 0s linear;
	}

	button::before {
		content: '';
		display: block;
		width: 0px;
		height: 86%;
		position: absolute;
		top: 7%;
		left: 0%;
		opacity: 0;
		background: #fff;
		box-shadow: 0 0 50px 30px #fff;
		-webkit-transform: skewX(-20deg);
		-moz-transform: skewX(-20deg);
		-ms-transform: skewX(-20deg);
		-o-transform: skewX(-20deg);
		transform: skewX(-20deg);
	}

	@keyframes sh02 {
		from {
			opacity: 0;
			left: 0%;
		}

		50% {
			opacity: 1;
		}

		to {
			opacity: 0;
			left: 100%;
		}
	}

	button:active {
		box-shadow: 0 0 0 0 transparent;
		-webkit-transition: box-shadow 0.2s ease-in;
		-moz-transition: box-shadow 0.2s ease-in;
		transition: box-shadow 0.2s ease-in;
	}
`

const StyledWrapper = styled.div`
	button {
		height: 100%;
		position: relative;
		padding: 0px 12px;
		border-radius: 10px;
		border: 1px solid rgb(43, 186, 243);
		font-size: 10px;
		text-transform: uppercase;
		font-weight: 600;
		letter-spacing: 2px;
		background: transparent;
		color: #fff;
		overflow: hidden;
		box-shadow: 0 0 0 0 transparent;
		-webkit-transition: all 0.2s ease-in;
		-moz-transition: all 0.2s ease-in;
		transition: all 0.2s ease-in;
	}

	button:hover {
		background: rgb(43, 186, 243);
		box-shadow: 0 0 30px 5px rgba(83, 196, 283, 0.175);
		-webkit-transition: all 0.2s ease-out;
		-moz-transition: all 0.2s ease-out;
		transition: all 0.2s ease-out;
	}

	button:hover::before {
		-webkit-animation: sh02 0.5s 0s linear;
		-moz-animation: sh02 0.5s 0s linear;
		animation: sh02 0.5s 0s linear;
	}

	button::before {
		content: '';
		display: block;
		width: 0px;
		height: 86%;
		position: absolute;
		top: 7%;
		left: 0%;
		opacity: 0;
		background: #fff;
		box-shadow: 0 0 50px 30px #fff;
		-webkit-transform: skewX(-20deg);
		-moz-transform: skewX(-20deg);
		-ms-transform: skewX(-20deg);
		-o-transform: skewX(-20deg);
		transform: skewX(-20deg);
	}

	@keyframes sh02 {
		from {
			opacity: 0;
			left: 0%;
		}

		50% {
			opacity: 1;
		}

		to {
			opacity: 0;
			left: 100%;
		}
	}

	button:active {
		box-shadow: 0 0 0 0 transparent;
		-webkit-transition: box-shadow 0.2s ease-in;
		-moz-transition: box-shadow 0.2s ease-in;
		transition: box-shadow 0.2s ease-in;
	}
`
export const ToggleButton = ({ select, setSelect }) => {
	return (
		<div className='bg-[var(--black)] relative shadow-inner w-full h-12 rounded-2xl border border-[#25252507] overflow-hidden'>
			{/* Переключатель (фон) */}
			<div
				className={`absolute top-[2px] left-[2px] w-[calc(50%-4px)] h-[calc(100%-4px)] bg-[var(--white)] rounded-xl transition-transform duration-300`}
				style={{
					transform: `translateX(${select === 1 ? '100%' : '0%'})`,
				}}
			/>

			{/* Текст */}
			<div className='relative flex h-full w-full items-center z-10'>
				<p
					onClick={() => setSelect?.(0)}
					className={`w-1/2 flex justify-center gap-2 text-center cursor-pointer font-medium transition-colors duration-300 ${
						select === 0 ? 'text-[var(--black)]' : 'text-[var(--white)]'
					}`}
				>
					Кости <img className='h-5 w-5' src='../img/dice.png' alt='' />
				</p>
				<p
					onClick={() => setSelect?.(1)}
					className={`w-1/2 flex gap-2 justify-center text-center cursor-pointer font-medium transition-colors duration-300 ${
						select === 1 ? 'text-[var(--black)]' : 'text-[var(--white)]'
					}`}
				>
					Баскетбол{' '}
					<img className='h-5 w-5' src='../img/basketball.png' alt='' />
				</p>
			</div>
		</div>
	)
}
