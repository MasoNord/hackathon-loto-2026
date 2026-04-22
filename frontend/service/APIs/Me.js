import api, { API } from '../../src/API'

export const Me = async () => {
	try {
		const response = await api.get(`${API}/auth/me`)
		return response.data
	} catch (error) {
		throw error
	}
}
