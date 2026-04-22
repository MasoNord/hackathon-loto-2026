const env = import.meta.env.VITE_ENV
const config = {
	dev: {
		API: import.meta.env.VITE_API_URL,
		FILE_API: import.meta.env.VITE_IMG_URL,
	},
	prod: {
		API: import.meta.env.VITE_API_URL_VDS,
		FILE_API: import.meta.env.VITE_IMG_URL_VDS,
	},
}

if (!config[env]) {
	throw new Error(`Неизвестное окружение: ${env}`)
}
export const { API, FILE_API } = config[env]

//====================== Axios API Error Context ===========================//

import axios from 'axios'

const api = axios.create({
	withCredentials: true,
})

const showError = status => {
	const messages = {
		401: 'Ошибка авторизации',
		403: 'Доступ запрещён',
		404: 'Ничего не найдено',
		500: 'Сервер временно умер',
	}

	// toast.error(messages[status] || `Ошибка ${status}`, {
	// 	id: 'api-error',
	// })
}

api.interceptors.response.use(
	r => r,
	error => {
		if (axios.isCancel(error)) {
			return Promise.reject(error)
		}

		// if (error.response.status === 401) {
		// 	window.location.href = '/authorization'
		// 	return Promise.reject(error)
		// }

		const status = error.response?.status || 500
		showError(status)

		return Promise.reject(error)
	},
)

export default api
