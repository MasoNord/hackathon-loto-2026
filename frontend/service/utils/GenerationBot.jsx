// /src/utils/generateBotName.js

const prefixes = [
	'Бот',
	'Робот',
	'ИИ',
	'Система',
	'Алгоритм',
	'Модуль',
	'Киборг',
	'Дрон',
	'Процессор',
	'Нейросеть',
	'Терминал',
]

const names = [
	'Вася',
	'Петя',
	'Гриша',
	'Ваня',
	'Саня',
	'Дима',
	'Лёха',
	'Коля',
	'Женя',
	'Макс',
	'Игорь',
]

const generateBotName = () => {
	const prefix = prefixes[Math.floor(Math.random() * prefixes.length)]

	const name = names[Math.floor(Math.random() * names.length)]

	return `${prefix} ${name}`
}
export const createBot = (index, stake) => ({
	id: index,
	isBot: true,
	name: generateBotName(),
	stake: stake,
})
