import { motion } from 'framer-motion'
import { User, UserPlus } from 'lucide-react'
import { SpecialButton, SpecialButton2 } from './Buttons'
import { useNavigate } from 'react-router-dom'

const SidebarElement = ({ type, color, title, number, people }) => {
	const colors = [
		'bg-[var(--pale-color1)]',
		'bg-[var(--pale-color2)]',
		'bg-[var(--pale-color3)]',
		'bg-[var(--pale-color4)]',
		'bg-[var(--pale-color5)]',
		'bg-[var(--pale-color6)]',
	]

	const maxUsers = type === 'dice' ? 6 : 2

	const filledPeople = [
		...people,
		...Array(maxUsers - people.length).fill(null),
	]

	return (
		<div className='w-full bg-[var(--gray-lighter)] p-2 rounded-3xl items-center flex gap-3 shadow-md'>
			<img
				className={`${colors[color]} rounded-2xl p-2 h-24 w-auto aspect-square object-cover`}
				src={
					type === 'dice'
						? '../animations/dice.webp'
						: type === 'basketball' && '../animations/basketball.webp'
				}
				alt=''
			/>

			<div className='flex flex-col w-full justify-between h-20'>
				<div className='flex justify-between items-center w-full'>
					<p className='font-bold text-2xl text-[var(--white)]'>{title}</p>
					<p className='text-sm text-[var(--gray-very-lighter)]'>
						Комната #{String(number).padStart(5, '0')}
					</p>
				</div>
				<div className='flex justify-between'>
					<div className='flex'>
						{filledPeople.map((person, index) =>
							person ? (
								<img
									key={index}
									className='rounded-[10px] border-3 border-[var(--gray-lighter)] w-9 h-auto aspect-square -ml-2 first:ml-0'
									src={person.avatar}
									alt=''
									style={{ zIndex: filledPeople.length - index }}
								/>
							) : (
								<UserPlus
									key={index}
									className='rounded-[10px] border-3 text-[var(--gray-lighter)] border-[var(--gray-lighter)] w-9 p-1 h-auto aspect-square -ml-2 first:ml-0 bg-[var(--gray-very-lighter)]'
									style={{ zIndex: filledPeople.length - index }}
								/>
							),
						)}
					</div>
					<SpecialButton title={'Присоединится'} to={`/room/${number}`} />
				</div>
			</div>
		</div>
	)
}

const Sidebar = () => {
	const navigate = useNavigate()
	const games = [
		{
			type: 'dice',
			color: 0,
			name: 'Кубики',
			number: 1,
			people: [
				{
					avatar:
						'https://i.pinimg.com/1200x/77/cc/25/77cc252792f12e666f654770309faee3.jpg',
				},
				{
					avatar:
						'https://i.pinimg.com/1200x/77/cc/25/77cc252792f12e666f654770309faee3.jpg',
				},
				{
					avatar:
						'https://i.pinimg.com/1200x/77/cc/25/77cc252792f12e666f654770309faee3.jpg',
				},
			],
		},
		{
			type: 'basketball',
			color: 1,
			name: 'Баскетбол',
			number: 22,
			people: [
				{
					avatar:
						'https://i.pinimg.com/1200x/77/cc/25/77cc252792f12e666f654770309faee3.jpg',
				},
			],
		},
		{
			type: 'dice',
			color: 2,
			name: 'Кубики',
			number: 333,
			people: [
				{
					avatar:
						'https://i.pinimg.com/1200x/77/cc/25/77cc252792f12e666f654770309faee3.jpg',
				},
				{
					avatar:
						'https://i.pinimg.com/1200x/77/cc/25/77cc252792f12e666f654770309faee3.jpg',
				},
			],
		},
		{
			type: 'basketball',
			color: 3,
			name: 'Баскетбол',
			number: 4444,
			people: [
				{
					avatar:
						'https://i.pinimg.com/1200x/77/cc/25/77cc252792f12e666f654770309faee3.jpg',
				},
			],
		},
	]
	return (
		<div className='h-screen w-120 bg-[var(--gray)] shadow-lg p-2'>
			<div className='flex flex-col gap-2 w-full h-full'>
				<SpecialButton2 title={'Создать комнату'} />
				{games.map((game, index) => (
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
						<SidebarElement
							key={index}
							type={game.type}
							color={game.color}
							title={game.name}
							number={game.number}
							people={game.people}
						/>
					</motion.div>
				))}
			</div>
		</div>
	)
}
export default Sidebar
