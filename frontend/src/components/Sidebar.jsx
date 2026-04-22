import { motion } from 'framer-motion'
import { User, UserPlus } from 'lucide-react'
import { SpecialButton, SpecialButton2, ToggleButton } from './Buttons'
import { useNavigate } from 'react-router-dom'
import Modal from './Modal'
import { useEffect, useState } from 'react'
import { BetInput, InputDefault } from './Inputs'
import { Me } from '../../service/APIs/Me'
import { getAllRooms } from '../../service/APIs/Rooms'

const SidebarElement = ({ type, title, number, people, price }) => {
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
	const randomNumber = Math.floor(Math.random() * 6)

	return (
		<>
			<div className='w-full bg-[var(--gray-lighter)] p-2 rounded-3xl items-center flex gap-3 shadow-md'>
				<img
					className={`${colors[randomNumber]} rounded-2xl p-2 h-24 w-auto aspect-square object-cover`}
					src={
						type === 'dice'
							? '../animations/dice.webp'
							: type === 'basketball' && '../animations/basketball.webp'
					}
					alt=''
				/>

				<div className='flex flex-col w-full justify-between h-20'>
					<div className='flex justify-between items-center w-full'>
						<div className='flex gap-2 items-center'>
							<p className='font-bold text-2xl text-[var(--white)]'>{title}</p>
							<p className='text-sm text-[var(--gray-very-lighter)]'>
								#{String(number).padStart(5, '0')}
							</p>
						</div>
						<div className='flex bg-[var(--gray)] items-center rounded-xl py-1 px-2 gap-2'>
							<img
								className='h-5 w-5 aspect-auto'
								src='../animations/diamond.webp'
								alt=''
							/>
							<p className='text-[var(--hero)]'>
								{Number(price || 0).toFixed(2)}
							</p>
						</div>
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
		</>
	)
}

const Sidebar = () => {
	const navigate = useNavigate()

	const [isModalOpen, setIsModalOpen] = useState(false)
	const [selected, setSelected] = useState(0)
	const [bet, setBet] = useState('')

	const [formData, setFormData] = useState({
		roomName: '',
		gameType: selected,
		stake: bet,
	})

	const handleChange = e => {
		const { name, value } = e.target
		setFormData(prev => ({ ...prev, [name]: value }))
	}
	const isValid = formData.stake > 0

	const [rooms, setRooms] = useState([])
	useEffect(() => {
		const handleRooms = async () => {
			try {
				const res = await getAllRooms()
				setRooms(res)
			} catch (err) {
				console.error(err)
			}
		}
		handleRooms()
	}, [])

	return (
		<>
			<Modal
				width={'w-100'}
				isOpen={isModalOpen}
				onClose={() => setIsModalOpen(false)}
			>
				<div className='flex flex-col gap-4'>
					<InputDefault
						title='Название комнаты'
						name='roomName'
						placeholder='Введите название...'
						value={formData.roomName}
						onChange={handleChange}
					/>
					<ToggleButton select={selected} setSelect={setSelected} />
					<BetInput value={bet} onChange={e => setBet(e.target.value)} />
					<SpecialButton2
						onClick={() => console.log('[eq')}
						title={'Создать комнату'}
					/>
				</div>
			</Modal>
			<div className='h-screen w-120 bg-[var(--gray)] shadow-lg p-2'>
				<div className='flex flex-col gap-2 w-full h-full'>
					<SpecialButton2
						onClick={() => setIsModalOpen(true)}
						title={'Создать комнату'}
					/>
					{rooms.map((game, index) => (
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
								title={game.name}
								number={game.id}
								price={game.enter_price}
								people={[]}
							/>
						</motion.div>
					))}
				</div>
			</div>
		</>
	)
}
export default Sidebar
