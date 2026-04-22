import { useState } from 'react'
import { InputDefault } from '../components/Inputs'
import { Login, Registration } from '../../service/APIs/Authorization'
import { motion } from 'framer-motion'
import styled from 'styled-components'
import { useNavigate } from 'react-router-dom'

const AuthToggle = ({ select, setSelect }) => {
	return (
		<div className='bg-[var(--black)] relative shadow-inner w-2/3 h-12 rounded-xl border border-[#25252507] overflow-hidden'>
			{/* Переключатель (фон) */}
			<div
				className={`absolute top-[2px] left-[2px] w-[calc(50%-4px)] h-[calc(100%-4px)] bg-[var(--white)] rounded-[10px] transition-transform duration-300`}
				style={{
					transform: `translateX(${select === 1 ? '100%' : '0%'})`,
				}}
			/>

			{/* Текст */}
			<div className='relative flex h-full w-full items-center z-10'>
				<p
					onClick={() => setSelect?.(0)}
					className={`w-1/2 text-center cursor-pointer font-medium transition-colors duration-300 ${
						select === 0 ? 'text-[var(--black)]' : 'text-[var(--white)]'
					}`}
				>
					Авторизация
				</p>
				<p
					onClick={() => setSelect?.(1)}
					className={`w-1/2 text-center cursor-pointer font-medium transition-colors duration-300 ${
						select === 1 ? 'text-[var(--black)]' : 'text-[var(--white)]'
					}`}
				>
					Регистрация
				</p>
			</div>
		</div>
	)
}

const Authorization = () => {
	const navigate = useNavigate()

	const [selected, setSelected] = useState(0)

	// Общие поля (логин использует почту/пароль, регистрация - все)
	const [formData, setFormData] = useState({
		username: '',
		password: '',
		repeatPassword: '',
	})

	const handleChange = e => {
		const { name, value } = e.target
		setFormData(prev => ({ ...prev, [name]: value }))
	}

	const handleSubmit = async e => {
		// 1. Предотвращаем дефолтное поведение браузера (отправку формы)
		if (e && e.preventDefault) {
			e.preventDefault()
		}

		try {
			if (selected === 0) {
				// Вход
				const res = await Login(formData.username, formData.password)
				console.log('Успешный вход:', res)
				navigate('/')
			} else {
				// Регистрация
				const res = await Registration(
					formData.username,
					formData.password,
					formData.repeatPassword,
				)
				console.log('Успешная регистрация:', res)
				navigate('/')
			}
		} catch (err) {
			console.error(err)
		}
	}

	const isAuthValid = formData.username && formData.password
	const isRegValid =
		isAuthValid && formData.password === formData.repeatPassword

	return (
		<div className='w-screen h-screen flex justify-center items-center'>
			<div className='w-2/5 h-fit p-6 bg-[var(--gray)] rounded-3xl'>
				<div className='flex flex-col items-center gap-6'>
					<div className='flex gap-5 items-center'>
						<img
							className='w-20 h-auto'
							src='../animations/diamond.webp'
							alt='logo'
						/>
						<p className='text-[var(--white)] text-2xl font-bold'>КристаЛото</p>
					</div>

					<AuthToggle select={selected} setSelect={setSelected} />

					<form onSubmit={handleSubmit} className='w-full flex flex-col gap-4'>
						<InputDefault
							title='Логин'
							name='username'
							placeholder='Введите логин...'
							value={formData.username}
							onChange={handleChange}
						/>
						<InputDefault
							title='Пароль'
							name='password'
							type='password'
							placeholder='Введите пароль...'
							value={formData.password}
							onChange={handleChange}
						/>

						{selected === 1 ? (
							<motion.div
								key={1}
								initial={{ scale: 0.8, opacity: 0 }}
								animate={{ scale: 1, opacity: 1 }}
								transition={{
									duration: 0.3,
									delay: 0.1,
									ease: 'easeOut',
								}}
								className='w-full mb-15'
							>
								<InputDefault
									title='Повторите пароль'
									name='repeatPassword'
									type='password'
									placeholder='Повторите пароль...'
									value={formData.repeatPassword}
									onChange={handleChange}
								/>
							</motion.div>
						) : (
							<div className='w-full h-19.5 mb-15'></div>
						)}
						<StyledWrapper>
							<button
								type='submit'
								disabled={selected === 0 ? !isAuthValid : !isRegValid}
								className={`${
									(selected === 0 ? isAuthValid : isRegValid)
										? 'hover:opacity-90 cursor-pointer'
										: 'opacity-50 cursor-not-allowed'
								}`}
							>
								{selected === 0 ? 'Войти' : 'Зарегистрироваться'}
							</button>
						</StyledWrapper>
					</form>
				</div>
			</div>
		</div>
	)
}

const StyledWrapper = styled.div`
	button {
		width: 100%;
		position: relative;
		padding: 12px;
		border-radius: 18px;
		border: 1px solid rgb(43, 186, 243);
		background: rgb(43, 186, 243);
		font-size: 14px;
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

export default Authorization
