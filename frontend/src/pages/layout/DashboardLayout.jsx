import { NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom'
import { Header } from '../../components/Header'
import { use, useContext, useEffect, useState } from 'react'
import { GraduationCap, ShieldAlert } from 'lucide-react'
import Sidebar from '../../components/Sidebar'
import { Me } from '../../../service/APIs/Me'

export default function DashboardLayout({ onChange }) {
	const [userInfo, setUserInfo] = useState()
	useEffect(() => {
		const handleUserInfo = async () => {
			try {
				const res = await Me()
				setUserInfo(res)
			} catch (err) {
				console.error(err)
			}
		}
		handleUserInfo()
	}, [])

	return (
		<>
			<div className='relative'>
				<Header userInfo={userInfo} />
				<div className='flex'>
					<div className='w-120'>
						<Sidebar />
					</div>
					<Outlet />
				</div>
			</div>
		</>
	)
}
