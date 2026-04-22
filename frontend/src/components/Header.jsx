import { PlusSquare } from 'lucide-react'
import { Plus } from 'lucide-react'
import { X } from 'lucide-react'
import { DiamondPlus } from 'lucide-react'
import { User } from 'lucide-react'
import { useState } from 'react'

const Header = () => {
	const [userInfo, setUserInfo] = useState({
		username: 'хуятина',
		avatar:
			'https://i.pinimg.com/1200x/77/cc/25/77cc252792f12e666f654770309faee3.jpg',
		balance: 124321.42432,
	})

	return (
		<header className='bg-[var(--gray-lighter)] flex justify-between items-center px-10 h-20 py-4 shadow-md'>
			<div className='flex gap-4 items-center h-full'>
				<img
					className='h-full w-auto'
					src='../animations/diamond.webp'
					alt=''
				/>
				<p className='text-2xl font-semibold text-[var(--white)]'>КристаЛото</p>
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
								{Number(userInfo?.balance).toFixed(2)}
							</p>
							<div className='bg-[var(--white)] text-[var(--gray)] h-5 w-5 p-[2px] flex items-center rounded-md rotate-45 justify-center ml-5'>
								<X strokeWidth='3.5' />
							</div>
						</div>
						<div className='h-full w-auto aspect-square rounded-xl overflow-hidden bg-[var(--gray)]'>
							{userInfo?.avatar?.length !== 0 ? (
								<img
									className='h-full w-full object-cover'
									src={userInfo?.avatar}
									alt=''
								/>
							) : (
								<User className='h-full w-full p-2' />
							)}
						</div>
					</>
				) : (
					<></>
				)}
			</div>
		</header>
	)
}

export { Header }
