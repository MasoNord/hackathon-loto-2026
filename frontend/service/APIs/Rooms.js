import api, { API } from '../../src/API'

export const CreateRoom = async (
	name,
	enter_price,
	seats,
	boosted,
	boost_price,
	prize_percentage,
	type,
) => {
	try {
		const response = await api.post(`${API}/auth/signup`, {
			name,
			enter_price,
			seats,
			boosted,
			boost_price,
			prize_percentage,
			type,
		})
		return response.data
	} catch (error) {
		throw error
	}
}

export const getAllRooms = async () => {
	try {
		const response = await api.get(`${API}/room/`)
		return response.data
	} catch (error) {
		throw error
	}
}
