import { CircleCheck, Eye, EyeOff, ImagePlus } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { Me } from '../../service/APIs/Me'
import { SpecialButton2, SpecialButton3 } from './Buttons'

export const useInput = ({ value, validate, onChange, onStatusChange }) => {
	const [internalValue, setInternalValue] = useState(value || '')
	const [status, setStatus] = useState(false)

	useEffect(() => {
		setInternalValue(value || '')
	}, [value])

	const handleChange = e => {
		const val = e.target.value
		setInternalValue(val)

		onChange?.(e)

		const newStatus = validate ? validate(val) : val.trim() !== ''
		setStatus(newStatus)
		onStatusChange?.(newStatus)
	}

	return {
		value: internalValue,
		status,
		handleChange,
	}
}

export const InputDefault = ({
	type = 'text',
	placeholder,
	title,
	required,
	validate,
	onStatusChange,
	value,
	onChange,
	disabled = false,
	name, // Добавь name, если используешь handleChange в родителе
}) => {
	const {
		value: val,
		status,
		handleChange,
	} = useInput({
		value,
		validate,
		onChange,
		onStatusChange,
		required,
	})

	// Состояние для отображения/скрытия пароля
	const [showPassword, setShowPassword] = useState(false)

	// Определяем текущий тип инпута
	const isPassword = type === 'password'
	const inputType = isPassword ? (showPassword ? 'text' : 'password') : type

	return (
		<div className={`w-full flex flex-col ${disabled && 'opacity-50'}`}>
			{title && (
				<div className='flex items-center gap-2 ml-1 mb-1'>
					<p className='text-[18px] text-[var(--white)] pt-[2px]'>{title}</p>
					{required && (
						<CircleCheck
							className={`${status ? 'text-green-500' : 'text-[var(--white)]'}`}
							size={16}
						/>
					)}
				</div>
			)}

			{/* Обертка для инпута и кнопки */}
			<div className='relative w-full'>
				<input
					type={inputType} // Используем динамический тип
					value={val}
					name={name} // Не забудь прокинуть name
					onChange={handleChange}
					readOnly={disabled}
					placeholder={placeholder}
					className='w-full rounded-2xl p-3 pr-12 bg-[var(--gray-very-lighter)] text-[var(--white)] shadow-inner transition-all focus:outline-none focus:ring-2 focus:ring-[var(--hero)]'
				/>

				{/* Кнопка-глазик, показываем только если изначальный type='password' */}
				{isPassword && (
					<button
						type='button' // Важно, чтобы не отправляло форму
						onClick={() => setShowPassword(!showPassword)}
						className='absolute right-4 top-1/2 -translate-y-1/2 text-[var(--white)] opacity-70 hover:opacity-100 transition-opacity focus:outline-none'
						tabIndex='-1' // Чтобы не мешало навигации табом
					>
						{showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
					</button>
				)}
			</div>
		</div>
	)
}

export const BetInput = ({ value, onChange }) => {
	const [balance, setBalance] = useState(0)
	const [isLoading, setIsLoading] = useState(true) // Стейт загрузки баланса

	// Шаг изменения при клике на стрелки
	const STEP = 1

	// Подгружаем баланс при монтировании
	useEffect(() => {
		setIsLoading(true)
		Me()
			.then(res => {
				const currentBalance = res?.bank_account?.balance || 0
				setBalance(currentBalance)
			})
			.catch(err => {
				console.error('Ошибка загрузки баланса:', err)
				// Можно добавить уведомление пользователю
			})
			.finally(() => {
				setIsLoading(false) // Разблокируем в любом случае
			})
	}, [])

	// Вспомогательная функция для безопасного обновления значения
	const updateBetSafely = newValue => {
		const numValue = parseFloat(newValue)

		// Если ввели не число или пустоту — сбрасываем в 0
		if (isNaN(numValue) || newValue === '') {
			onChange({ target: { value: '' } })
			return
		}

		// Ограничиваем балансом сверху и 0 снизу
		const validatedValue = Math.max(0, Math.min(balance, numValue))

		// Форматируем до 2 знаков после запятой, чтобы избежать проблем с плавающей точкой
		onChange({ target: { value: validatedValue.toFixed(2) } })
	}

	// Обработчик ручного ввода
	const handleChange = e => {
		const val = e.target.value
		// Разрешаем вводить цифры и одну точку
		if (/^\d*\.?\d*$/.test(val)) {
			// Но окончательную валидацию делаем только при потере фокуса или через updateBetSafely,
			// чтобы разрешить пользователю стирать цифры.
			// Здесь просто проверяем, не больше ли баланса сразу
			if (parseFloat(val) > balance) {
				updateBetSafely(balance)
			} else {
				onChange(e)
			}
		}
	}

	const handleMax = () => {
		if (isLoading || balance <= 0) return
		updateBetSafely(balance)
	}

	// Логика кастомных стрелочек
	const handleIncrement = () => {
		if (isLoading) return
		const current = parseFloat(value) || 0
		updateBetSafely(current + STEP)
	}

	const handleQuickAdd = amount => {
		const current = parseFloat(value) || 0
		updateBetSafely(current + amount)
	}

	const handleDecrement = () => {
		if (isLoading) return
		const current = parseFloat(value) || 0
		updateBetSafely(current - STEP)
	}

	// Определяем, заблокирован ли инпут
	const isInputDisabled = isLoading || balance <= 0

	return (
		<>
			{/* CSS для скрытия дефолтных стрелок (Spin Buttons) */}
			<style>{`
                input[type=number]::-webkit-inner-spin-button, 
                input[type=number]::-webkit-outer-spin-button { 
                    -webkit-appearance: none; 
                    margin: 0; 
                }
                input[type=number] {
                    -moz-appearance: textfield; /* Firefox */
                }
            `}</style>

			<div
				className={`w-full flex flex-col gap-2 ${isLoading ? 'opacity-60 pointer-events-none' : ''} transition-opacity`}
			>
				<div className='flex justify-between items-center px-1'>
					<p className='text-[14px] text-[var(--white)] opacity-70'>
						{isLoading ? 'Загрузка баланса...' : 'Ставка'}
					</p>
					<button
						onClick={handleMax}
						disabled={isInputDisabled}
						className='text-[12px] text-[var(--hero)] hover:underline cursor-pointer disabled:opacity-50 disabled:no-underline'
					>
						MAX ({Number(balance).toFixed(2)})
					</button>
				</div>

				<div className='relative w-full flex items-center'>
					{/* Инпут */}
					<input
						type='number' // Оставляем number для мобильной клавиатуры
						value={value}
						onChange={handleChange}
						onBlur={() => updateBetSafely(value)} // Финальная валидация при потере фокуса
						disabled={isInputDisabled}
						placeholder='0.00'
						// Добавляем pr-24, чтобы освободить место под алмаз и стрелочки
						className='w-full rounded-2xl py-3 pl-4 pr-24 bg-[var(--gray-very-lighter)] text-[var(--white)] font-bold text-lg shadow-inner focus:outline-none focus:ring-2 focus:ring-[var(--hero)] disabled:cursor-not-allowed'
					/>

					{/* Блок управления справа внутри инпута */}
					<div className='absolute right-2 flex items-center gap-2'>
						{/* Кастомные стрелочки */}
						<div className='flex flex-col gap-0.5'>
							<button
								onClick={handleIncrement}
								disabled={isInputDisabled || parseFloat(value) >= balance}
								className='text-[var(--white)] opacity-50 hover:opacity-100 disabled:opacity-20 flex items-center justify-center h-4 w-5 bg-[var(--black)]/20 rounded-sm'
							>
								<span className='translate-y-[-1px]'>▲</span>{' '}
								{/* Можно заменить на SVG */}
							</button>
							<button
								onClick={handleDecrement}
								disabled={isInputDisabled || parseFloat(value) <= 0}
								className='text-[var(--white)] opacity-50 hover:opacity-100 disabled:opacity-20 flex items-center justify-center h-4 w-5 bg-[var(--black)]/20 rounded-sm'
							>
								<span className='translate-y-[-1px]'>▼</span>{' '}
								{/* Можно заменить на SVG */}
							</button>
						</div>

						{/* Иконка валюты */}
						<img
							className='h-6 w-6 pointer-events-none'
							src='../animations/diamond.webp'
							alt='diamond'
						/>
					</div>
				</div>
				{/* Блок кнопок +10 +100 +1000 */}
				<div className='grid grid-cols-3 gap-2'>
					{[10, 100, 1000].map(amount => (
						<SpecialButton3
							onClick={() => handleQuickAdd(amount)}
							title={`+${amount}`}
						/>
					))}
				</div>
			</div>
		</>
	)
}

export const TextArea = ({
	placeholder,
	title,
	required,
	validate,
	value,
	onChange,
	onStatusChange,
	readOnly = false,
}) => {
	const {
		value: val,
		status,
		handleChange,
	} = useInput({
		value,
		validate,
		onChange,
		onStatusChange,
	})

	return (
		<div className={`w-full flex flex-col ${readOnly && 'opacity-40'}`}>
			{title && (
				<div className='flex items-center gap-2 ml-1'>
					<p className={`text-[18px] text-[var(--middle)] pt-[2px]`}>{title}</p>
					{required && (
						<CircleCheck
							className={`${status ? 'text-green-500' : 'text-[var(--middle)]'}`}
							size={16}
						/>
					)}
				</div>
			)}

			<textarea
				value={val}
				onChange={handleChange}
				readOnly={readOnly}
				placeholder={placeholder}
				maxLength={300}
				className=' rounded-2xl p-3 shadow-inner border-1 border-[#25252507] transition-all resize-none min-h-25'
			/>
		</div>
	)
}

export const FileInput = ({
	title,
	required,
	onStatusChange,
	onFileChange,
	photoUrl,
}) => {
	const [status, setStatus] = useState(false)
	const [fileInfo, setFileInfo] = useState(null)
	const [preview, setPreview] = useState(null)
	const [drag, setDrag] = useState(false)

	const validFormats = ['image/png', 'image/jpeg', 'image/webp', 'image/gif']
	const maxSize = 10 * 1024 * 1024

	const reset = () => {
		setStatus(false)
		setFileInfo(null)
		setPreview(null)
		onStatusChange?.(false)
	}

	const validate = async file => {
		if (!file) return reset()

		if (!validFormats.includes(file.type)) return reset()
		if (file.size > maxSize) return reset()

		if (file.type.startsWith('image/')) {
			const img = new Image()
			const url = URL.createObjectURL(file)

			await new Promise((res, rej) => {
				img.onload = () => {
					if (img.width > 4000 || img.height > 4000) {
						rej()
					} else res()
					URL.revokeObjectURL(url)
				}
				img.onerror = rej
				img.src = url
			}).catch(reset)
		}

		setStatus(true)
		onStatusChange?.(true)

		setFileInfo({
			name: file.name,
			size: (file.size / 1024 / 1024).toFixed(2),
		})

		setPreview(URL.createObjectURL(file))
		onFileChange?.(file)
	}

	return (
		<div className='flex flex-col gap-3 w-full'>
			{title && (
				<div className='flex items-center gap-2'>
					<p className={`text-[18px] text-[var(--middle)] pt-[2px]`}>{title}</p>
					{required && (
						<CircleCheck
							className={`${status ? 'text-green-500' : 'text-[var(--middle)]'}`}
							size={16}
						/>
					)}
				</div>
			)}

			<label
				className={`grid grid-cols-5 gap-3 p-1 rounded-2xl bg-white shadow-[var(--shadow)] cursor-pointer transition ${
					drag && 'ring-2 ring-[var(--hero-epta)]'
				}`}
				onDragOver={e => {
					e.preventDefault()
					setDrag(true)
				}}
				onDragLeave={() => setDrag(false)}
				onDrop={e => {
					e.preventDefault()
					setDrag(false)
					validate(e.dataTransfer.files[0])
				}}
			>
				<div className='col-span-1 flex justify-center items-center'>
					{preview || photoUrl ? (
						<img
							src={preview || photoUrl}
							alt='preview'
							className='w-[80px] h-[80px] object-cover rounded-xl py-[1px]'
						/>
					) : (
						<ImagePlus size={80} strokeWidth={1.25} color='var(--middle)' />
					)}
				</div>
				<div className='flex items-center col-span-2'>
					<div className='flex flex-wrap gap-1 h-fit'>
						<p
							className={`rounded-lg text-xs font-normal px-2 py-1 h-fit whitespace-nowrap ${
								fileInfo && fileInfo.size <= 10
									? 'bg-[var(--hero-epta)] text-white'
									: 'bg-[var(--bg)] text-[var(--black)]'
							}`}
						>
							до 10 мб
						</p>
						{['.png', '.jpg', '.webp', '.gif'].map(ext => (
							<p
								key={ext}
								className={`rounded-lg text-xs font-normal px-2 py-1 h-fit whitespace-nowrap ${
									fileInfo && fileInfo.name.endsWith(ext)
										? 'bg-[var(--hero-epta)] text-white'
										: 'bg-[var(--bg)] text-[var(--black)]'
								}`}
							>
								{ext}
							</p>
						))}
					</div>
				</div>
				<p
					className={`col-span-2 flex items-center text-xs text-[var(--black)] font-normal ${
						fileInfo && 'truncate'
					}  text-center`}
				>
					{fileInfo ? (
						<>
							{fileInfo.name}
							<br />({fileInfo.size} МБ)
						</>
					) : (
						<>
							Перетащите файл сюда
							<br />
							или
							<br />
							нажмите для загрузки
						</>
					)}
				</p>

				<input
					type='file'
					className='hidden'
					onChange={e => validate(e.target.files[0])}
				/>
			</label>
		</div>
	)
}

export const OptionSearch = ({
	options = [],
	placeholder = '',
	labelKey = 'name',
	onSelect,
	onCreate,
	value = null,
}) => {
	const [query, setQuery] = useState('')
	const [isOpen, setIsOpen] = useState(false)
	const [selected, setSelected] = useState(value)

	// синхра снаружи
	useEffect(() => {
		if (value) {
			setSelected(value)
			setQuery(value[labelKey] || '')
		}
	}, [value])

	// 🔥 локальный поиск
	const filtered = useMemo(() => {
		return options.filter(item =>
			item[labelKey].toLowerCase().includes(query.toLowerCase()),
		)
	}, [query, options])

	const handleSelect = item => {
		setSelected(item)
		setQuery(item[labelKey])
		setIsOpen(false)
		onSelect?.(item)
	}

	return (
		<div className='relative w-full'>
			<div className='flex items-center rounded-2xl shadow-inner px-4 py-3 bg-white'>
				<input
					value={query}
					onChange={e => {
						setQuery(e.target.value)
						setSelected(null)
					}}
					onFocus={() => setIsOpen(true)}
					onBlur={() => setTimeout(() => setIsOpen(false), 150)}
					placeholder={placeholder}
					className='w-full bg-transparent'
				/>
			</div>

			{isOpen && (
				<div className='absolute w-full bg-white shadow-[var(--shadow)] rounded-2xl mt-1 max-h-35 overflow-y-scroll z-10'>
					{filtered.length === 0 ? (
						<button
							type='button'
							onClick={() => {
								onCreate?.(query)
								setIsOpen(false)
							}}
							className='w-full text-left px-3 py-2 flex items-center gap-2 hover:bg-[var(--hero-epta)] hover:text-white'
						>
							<span className='text-lg'>+</span>
							Создать "{query}"
						</button>
					) : (
						filtered.map((item, i) => (
							<button
								key={i}
								type='button'
								onClick={() => handleSelect(item)}
								className='w-full text-left px-3 py-2 hover:bg-[var(--hero-epta)] hover:text-white'
							>
								{item[labelKey]}
							</button>
						))
					)}
				</div>
			)}
		</div>
	)
}

export const OptionInputWithSearch = ({
	options = [],
	placeholder = '',
	labelKey = 'name',
	onSelect,
	onCreate,
	value = null,
	title,
	required,
}) => {
	const [isOpen, setIsOpen] = useState(false)
	const [search, setSearch] = useState('')
	const [selected, setSelected] = useState(value)

	// синхра
	useEffect(() => {
		if (value) {
			setSelected(value)
		}
	}, [value])

	const filtered = useMemo(() => {
		return options.filter(item =>
			item[labelKey].toLowerCase().includes(search.toLowerCase()),
		)
	}, [search, options])

	const handleSelect = item => {
		setSelected(item)
		setSearch('')
		setIsOpen(false)
		onSelect?.(item)
	}

	return (
		<div className='w-full flex flex-col gap-2'>
			{/* 🔥 TITLE */}
			{title && (
				<div className='flex items-center gap-2'>
					<p className={`text-[18px] text-[var(--middle)] pt-[2px]`}>{title}</p>
					{required && (
						<CircleCheck
							className={`${selected ? 'text-green-500' : 'text-[var(--middle)]'}`}
							size={16}
						/>
					)}
				</div>
			)}

			<div className='relative w-full'>
				{/* 🔥 ОСНОВНОЙ INPUT */}
				<div
					onClick={() => setIsOpen(prev => !prev)}
					className='flex items-center rounded-2xl shadow-inner border-1 border-[#00000005] px-4 py-3 bg-white cursor-pointer'
				>
					<input
						readOnly
						value={selected ? selected[labelKey] : ''}
						placeholder={placeholder}
						className='w-full outline-none bg-transparent cursor-pointer'
					/>
				</div>

				{/* 🔥 DROPDOWN */}
				{isOpen && (
					<div className='absolute w-full bg-white shadow-[var(--shadow)] rounded-3xl mt-2 max-h-50 overflow-hidden z-10 flex flex-col'>
						{/* 🔍 ПОИСК ВНУТРИ */}
						<div className='p-2'>
							<InputDefault
								value={search}
								onChange={e => setSearch(e.target.value)}
								placeholder='Поиск...'
								className='w-full px-3 py-2 rounded-lg outline-none bg-[var(--bg)]'
								autoFocus
							/>
						</div>

						{/* 📃 СПИСОК */}
						<div className='overflow-y-scroll max-h-35'>
							{filtered.length === 0 ? (
								<button
									type='button'
									onClick={() => {
										onCreate?.(search)
										setIsOpen(false)
									}}
									className='w-full text-left px-3 py-2 flex items-center gap-2 hover:bg-[var(--hero-epta)] hover:text-white'
								>
									<span className='text-lg'>+</span>
									Создать "{search}"
								</button>
							) : (
								filtered.map((item, i) => (
									<button
										key={i}
										type='button'
										onClick={() => handleSelect(item)}
										className='w-full text-left px-3 py-2 hover:bg-[var(--hero-epta)] hover:text-white cursor-pointer'
									>
										{item[labelKey]}
									</button>
								))
							)}
						</div>
					</div>
				)}
			</div>
		</div>
	)
}
