# Provider layer

The API now has a provider boundary so application code can be developed and tested independently of external account authentication.

## Development mode

Use `AUTH_PROVIDER=mock` to enable the local mock provider. It never contacts Free Fire/Garena and uses synthetic BR account data.

Test login values:

- UID: `TEST_UID`
- Password: `TEST_PASSWORD`

Mock OTP: `123456`

Do not place real account credentials in this repository or in automated tests.
