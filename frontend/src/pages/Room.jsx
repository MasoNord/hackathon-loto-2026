import { useEffect, useMemo, useState } from 'react'
import { useParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Bot, Crown, Plus, User, UserPlus } from 'lucide-react'
import { formatTime } from '../../service/utils/FormatTimer'
import { createBot } from '../../service/utils/GenerationBot'

const PlayerCard = ({ person, id, stake, winner, inGame, type }) => {
	const colors = [
		'bg-[var(--color1)]',
		'bg-[var(--color2)]',
		'bg-[var(--color3)]',
		'bg-[var(--color4)]',
		'bg-[var(--color5)]',
		'bg-[var(--color6)]',
	]

	const name = person?.name

	console.log(winner && id)

	return (
		<div
			className={`h-22 ${
				inGame ? 'bg-[var(--gray-lighter)] w-fit' : 'bg-[var(--gray)] w-full'
			} flex justify-between items-center rounded-3xl p-4`}
		>
			<div className='flex gap-5 h-full'>
				{/* AVATAR */}
				<div className='h-full aspect-square rounded-xl overflow-hidden bg-[var(--gray)] flex items-center justify-center text-[var(--white)]'>
					{type === 'empty' ? (
						<UserPlus />
					) : person?.avatar ? (
						<img src={person.avatar} />
					) : (
						<Bot className='h-full w-full p-2' />
					)}
				</div>

				{/* NAME + ID */}
				<div className='flex gap-3 items-center'>
					<p className='text-[var(--white)] first-letter:uppercase'>
						{type === 'empty' ? 'Ожидание игрока...' : name}
					</p>

					{type !== 'empty' && (
						<div
							className={`${colors[id - 1]} relative rounded-lg text-[var(--gray-lighter)] aspect-square h-6 flex justify-center items-center`}
						>
							{winner && (
								<Crown className='absolute -top-4 h-4 text-amber-300' />
							)}
							{id}
						</div>
					)}
				</div>
			</div>

			{/* STAKE */}
			{type !== 'empty' && (
				<div className={`flex gap-1 items-center ${inGame && 'ml-25'}`}>
					<img className='h-6 w-6' src='../animations/diamond.webp' />
					<p className='text-[var(--hero)]'>
						{winner && '+'}
						{Number(stake ?? person?.stake ?? 0).toFixed(2)}
					</p>
				</div>
			)}
		</div>
	)
}

const BasketballGame = ({ people }) => {
	const maxUsers = 2

	const [winner, setWinner] = useState(0)
	const [waiting, setWaiting] = useState(true)

	useEffect(() => {
		winner !== null && setWaiting(false)
	}, [winner])

	const filledPeople = [
		...people,
		...Array(maxUsers - people.length).fill(null),
	]

	const getAnimation = (winner, index) => {
		if (winner === index) {
			const winAnimations = ['001', '002']
			return `../animations/basketball/win/${
				winAnimations[Math.floor(Math.random() * winAnimations.length)]
			}.webp`
		} else {
			const loseAnimations = ['001', '002', '003']
			return `../animations/basketball/lose/${
				loseAnimations[Math.floor(Math.random() * loseAnimations.length)]
			}.webp`
		}
	}
	return (
		<>
			<div className='grid grid-cols-2 gap-3 h-full'>
				{filledPeople.map((person, index) => (
					<motion.div
						key={index}
						initial={{ scale: 0.8, opacity: 0 }}
						animate={{ scale: 1, opacity: 1 }}
						transition={{
							duration: 0.3,
							delay: index * 0.1,
							ease: 'easeOut',
						}}
						className='w-full'
					>
						<div className='bg-[var(--gray)] w-full flex flex-col gap-10 justify-center items-center h-full rounded-3xl mt-3'>
							{winner !== null && (
								<p
									className={`text-5xl font-bold ${winner === index ? 'text-[var(--color2)]' : 'text-[var(--color6)]'}`}
								>
									{winner === index ? 'Победитель!' : 'Проигравший'}
								</p>
							)}

							{person ? (
								<PeopleCard
									personInfo={filledPeople[index]}
									winner={false}
									inGame={true}
								/>
							) : (
								<FoundPeople inGame={true} />
							)}
							{waiting ? (
								<img
									className='h-auto w-2/3'
									src='../animations/basketball.webp'
									alt=''
								/>
							) : (
								<img
									className='h-auto w-2/3'
									src={getAnimation(winner, index)}
									alt=''
								/>
							)}
						</div>
					</motion.div>
				))}
			</div>
		</>
	)
}

const DiceGame = ({ people = [] }) => {
	const MAX_USERS = 6
	const [fixedStake, setFixedStake] = useState(175)
	const [winner, setWinner] = useState(null)
	const [countdown, setCountdown] = useState(null)
	const [waiting, setWaiting] = useState(true)
	const [time, setTime] = useState(0)
	const [bots, setBots] = useState([])
	const [showResult, setShowResult] = useState(false)

	// Все игроки: реальные люди + сгенерированные боты
	const allPlayers = useMemo(() => [...people, ...bots], [people, bots])

	// Пересчёт времени ожидания
	useEffect(() => {
		const remainingSlots = MAX_USERS - people.length
		setTime(remainingSlots * 1)
	}, [people.length])

	// Таймер ожидания + спавн ботов
	useEffect(() => {
		if (!waiting || time <= 0) return
		const interval = setInterval(() => {
			setTime(prev => {
				if (prev <= 1) {
					clearInterval(interval)
					const remainingSlots = MAX_USERS - people.length
					const newBots = Array.from({ length: remainingSlots }, (_, i) =>
						createBot(people.length + i + 1, fixedStake),
					)
					setBots(newBots)
					return 0
				}
				return prev - 1
			})
		}, 1000)
		return () => clearInterval(interval)
	}, [waiting, time, people.length, fixedStake])

	// Старт игры когда набралось MAX_USERS
	useEffect(() => {
		if (allPlayers.length === MAX_USERS && waiting) {
			setCountdown(3)
			setWaiting(false)
		}
	}, [allPlayers.length, waiting])

	// Логика отсчета и определения победителя
	useEffect(() => {
		if (countdown === null) return
		if (countdown === 0) {
			const randomWinner = Math.floor(Math.random() * allPlayers.length)
			setWinner(randomWinner)
			setTimeout(() => setShowResult(true), 500)
			return
		}
		const interval = setInterval(() => {
			setCountdown(prev => prev - 1)
		}, 1000)
		return () => clearInterval(interval)
	}, [countdown, allPlayers.length])

	return (
		<>
			{/* PLAYERS GRID */}
			<div className='grid grid-cols-3 gap-3'>
				{Array.from({ length: MAX_USERS }).map((_, index) => {
					const person = allPlayers[index]
					return (
						<motion.div
							key={person?.id || `empty-${index}`}
							initial={{ opacity: 0, scale: 0.9 }}
							animate={{ opacity: 1, scale: 1 }}
							transition={{ duration: 0.3, delay: index * 0.1 }}
						>
							{!person ? (
								<PlayerCard type='empty' id={index + 1} />
							) : (
								<PlayerCard
									person={person}
									id={index + 1}
									inGame={false}
									// ВАЖНО: передаем ставку явно, чтобы она была доступна в компоненте
									stake={fixedStake}
								/>
							)}
						</motion.div>
					)
				})}
			</div>

			{/* BOTTOM PANEL */}
			<div className='bg-[var(--gray)] w-full flex flex-col gap-3 justify-center items-center h-full rounded-3xl mt-3'>
				{winner !== null && (
					<motion.div
						initial={{ scale: 0.8, opacity: 0 }}
						animate={{ scale: 1, opacity: 1 }}
						transition={{ duration: 0.5, delay: 2.5, ease: 'easeOut' }}
						className='flex flex-col items-center gap-3 justify-center'
					>
						<p className='text-4xl font-bold text-[var(--color2)]'>
							Победитель!
						</p>
						<PlayerCard
							type={allPlayers[winner]?.isBot ? 'bot' : 'player'}
							person={allPlayers[winner]}
							id={allPlayers[winner]?.id}
							stake={fixedStake * MAX_USERS} // Весь банк
							inGame
							winner
						/>
					</motion.div>
				)}

				{waiting && countdown === null && (
					<p className='text-[var(--white)] text-4xl font-semibold'>
						Ожидание игроков {time}
					</p>
				)}

				{countdown !== null && countdown > 0 && (
					<p className='text-6xl text-[var(--white)] font-bold'>
						{countdown}...
					</p>
				)}

				<div className='relative h-50 w-50'>
					<img
						className={`absolute inset-0 w-full h-full object-contain transition-opacity ${
							showResult ? 'opacity-0' : 'opacity-100'
						}`}
						src='/animations/dice.webp'
						alt='Dice'
					/>
					{showResult && winner !== null && (
						<video
							className='absolute inset-0 w-full h-full object-contain'
							src={`/animations/dice/00${winner + 1}.webm`}
							autoPlay
							muted
							playsInline
						/>
					)}
				</div>

				{winner !== null && (
					<motion.div
						initial={{ scale: 0.8, opacity: 0 }}
						animate={{ scale: 1, opacity: 1 }}
						transition={{ duration: 0.3, delay: 2.75, ease: 'easeOut' }}
						className='text-sm font-light text-[var(--gray-very-lighter)]'
					>
						Выпало число {winner + 1}
					</motion.div>
				)}
			</div>
		</>
	)
}

const Room = () => {
	const { id } = useParams()
	const [roomInfo, setRoomInfo] = useState({
		type: 'dice',
		name: 'Кости кубики',
		number: id,
		people: [
			{
				id: 1,
				name: 'хуйкин',
				avatar:
					'https://i.pinimg.com/1200x/77/cc/25/77cc252792f12e666f654770309faee3.jpg',

				winner: true,
			},
			{
				id: 2,
				name: 'хуйкин',
				avatar:
					'https://i.pinimg.com/1200x/77/cc/25/77cc252792f12e666f654770309faee3.jpg',

				winner: true,
			},
			{
				id: 3,
				name: 'хуйкин',
				avatar:
					'https://i.pinimg.com/1200x/77/cc/25/77cc252792f12e666f654770309faee3.jpg',

				winner: true,
			},
		],
	})

	return (
		<div className='flex flex-col py-10 w-full px-5'>
			<div className='flex w-full justify-between items-center'>
				<p className='text-[var(--white)] font-bold text-5xl'>
					{roomInfo.name}
				</p>
				<p className='text-[var(--gray-lighter)] font-light text-4xl'>
					Комната #{String(roomInfo.number).padStart(5, '0')}
				</p>
			</div>
			{roomInfo?.type === 'dice' ? (
				<DiceGame people={roomInfo.people} />
			) : (
				roomInfo?.type === 'basketball' && (
					<BasketballGame people={roomInfo.people} />
				)
			)}
		</div>
	)
}

export default Room
