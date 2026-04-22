import api, { API } from '../../src/API'

export const Registration = async (username, password, repeatPassword) => {
	try {
		const response = await api.post(`${API}/auth/signup`, {
			username,
			password,
			repeat_password: repeatPassword,
		})
		return response.data
	} catch (error) {
		throw error
	}
}

export const Login = async (username, password) => {
	try {
		const response = await api.post(`${API}/auth/login`, {
			username,
			password,
		})
		return response.data
	} catch (error) {
		throw error
	}
}
