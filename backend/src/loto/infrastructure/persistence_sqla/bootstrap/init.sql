--- Initialize User Roles
insert into roles (id, name)
values
	('019d6762-7d15-7b7b-9ce5-e85ad2f76203', 'administrator'),
	('019d6762-a930-78d9-b8ed-1698c7a2e659', 'player'),
on conflict(id, name) do nothing