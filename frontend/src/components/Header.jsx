import { PlusSquare } from 'lucide-react'
import { Plus } from 'lucide-react'
import { X } from 'lucide-react'
import { DiamondPlus } from 'lucide-react'
import { User } from 'lucide-react'
import { useState } from 'react'
import { FILE_API } from '../API'
import Modal from './Modal'
import { BetInput } from './Inputs'
import { SpecialButton2 } from './Buttons'

const Header = ({ userInfo }) => {
	const [isModalOpen, setIsModalOpen] = useState(false)
	const [bet, setBet] = useState('')
	return (
		<>
			<Modal
				width={'w-100'}
				isOpen={isModalOpen}
				onClose={() => setIsModalOpen(false)}
			>
				<div className='flex flex-col gap-4 mt-5'>
					<BetInput value={bet} onChange={e => setBet(e.target.value)} />
					<SpecialButton2
						onClick={() => console.log('[eq')}
						title={'Пополнить'}
					/>
				</div>
			</Modal>
			<header className='bg-[var(--gray-lighter)] flex justify-between items-center px-10 h-20 py-4 shadow-md'>
				<div className='flex gap-4 items-center h-full'>
					<img
						className='h-full w-auto'
						src='../animations/diamond.webp'
						alt=''
					/>
					<p className='text-2xl font-semibold text-[var(--white)]'>
						КристаЛото
					</p>
				</div>
				<div className='flex gap-4 items-center h-full'>
					{userInfo !== null ? (
						<>
							<div className='flex bg-[var(--gray)] items-center rounded-xl py-2 px-3 gap-2'>
								<img
									className='h-6 w-6 aspect-auto'
									src='../animations/diamond.webp'
									alt=''
								/>
								<p className='text-[var(--hero)]'>
									{Number(userInfo?.bank_account?.balance || 0).toFixed(2)}
								</p>
								<div
									onClick={() => setIsModalOpen(true)}
									className='bg-[var(--white)] text-[var(--gray)] h-5 w-5 p-[2px] flex items-center rounded-md rotate-45 justify-center ml-5 cursor-pointer'
								>
									<X strokeWidth='3.5' />
								</div>
							</div>
							<div className='h-full w-auto aspect-square rounded-xl overflow-hidden bg-[var(--gray)]'>
								{userInfo?.avatar ? (
									<img
										className='h-full w-full object-cover'
										src={FILE_API + userInfo?.avatar}
										alt=''
									/>
								) : (
									<User className='h-full w-full p-2 text-[var(--gray-very-lighter)]' />
								)}
							</div>
						</>
					) : (
						<></>
					)}
				</div>
			</header>
		</>
	)
}

export { Header }
