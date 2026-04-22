import { NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom'
import { Header } from '../../components/Header'
import { use, useContext, useEffect, useState } from 'react'
import { GraduationCap, ShieldAlert } from 'lucide-react'
import Sidebar from '../../components/Sidebar'

export default function DashboardLayout({ onChange }) {
	return (
		<>
			<div className='relative'>
				<Header />
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
