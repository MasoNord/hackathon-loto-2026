--- Initialize User Roles
insert into roles (id, name)
values
	('019d6762-7d15-7b7b-9ce5-e85ad2f76203', 'administrator'),
	('019d6762-a930-78d9-b8ed-1698c7a2e659', 'player'),
on conflict(id, name) do nothing


--- Create base administrator

BEGIN;

INSERT INTO bank_account (
    id,
    balance
) VALUES (
    'a1d4e5f6-2c3b-7d10-8f2a-9b1c4d5e6f70',
    10000.00
);

INSERT INTO users (
    id,
    email,
    username,
    hashed_password,
    avatar_url,
    bank_account_id,
    role_id
) VALUES (
    '6f2a9c3d-11b4-7c3e-9a8b-3d5e7f9012ab',
    'ivan@example.com',
    'ivan123',
    '$argon2id$v=19$m=65536,t=4,p=1$N1ZuenViNDlSVk9tWU04Mw$WihL962UPPemzDgKc9ELXNGDWaEUis8R3OhZj7TTfcg',
    'media/avatars/019db434-004e-75a3-b413-ab049caaed87.png',
    'a1d4e5f6-2c3b-7d10-8f2a-9b1c4d5e6f70',
    '019d6762-7d15-7b7b-9ce5-e85ad2f76203'
);

COMMIT;