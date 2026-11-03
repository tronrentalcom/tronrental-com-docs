# Changelog

What's new in TronRental. The same log, with tag filters and an RSS feed, is published at https://docs.tronrental.com/changelog.

## 2026-10-30 · Energy Broadcaster for TRC-20 tokens, swaps and contract calls

Tags: Broadcaster

The Energy Broadcaster now serves more than USDT: transfers of other TRC-20 tokens, swaps on SunSwap and calls to other smart contracts get energy and bandwidth, and TRX transfers get bandwidth. The cost of each call is calculated from its simulation; less common tokens, swaps and contract calls are served within your account's limits and can be switched off in the broadcaster settings. [Energy Broadcaster](https://tronrental.com/en/energy-broadcaster)

## 2026-10-29 · Sign-up confirmed with an email code

Tags: API

New accounts registered with an email address are confirmed with a 6-digit code sent to that address. Breaking change for scripts that sign up through the API: `POST /auth/register` now answers `requires_email_code: true` instead of returning tokens, and the account is created by `POST /auth/email-code/verify`. Existing accounts are not affected. [Authentication](https://docs.tronrental.com/authentication)

## 2026-10-29 · Bandwidth rental from 5 minutes

Tags: Bandwidth, API

Rent bandwidth for any term from 5 to 59 minutes at a discount off the hourly rate, not only for an hour or a day. The new quote endpoint returns the exact amount, and the optional `max_price_trx` refuses a purchase whose price changed after the quote. [Quote Bandwidth](https://docs.tronrental.com/api-reference/bandwidth/quote)

## 2026-10-28 · Energy and bandwidth from 1 unit

Tags: Energy, Bandwidth, API

The minimum order is now 1 unit of energy or bandwidth, below the usual market minimum: on the website, in the API, in the Telegram bot and in Auto-Refill rules. Invoices and Instant Buy for energy still start at 32,000. [Buy Energy](https://docs.tronrental.com/api-reference/energy/buy-energy)

## 2026-10-28 · Auto-Bandwidth

Tags: Auto-Bandwidth

Turn on Auto-Bandwidth for an address and its outgoing transfers get bandwidth, so the network does not burn TRX for it. It works for USDT, TRX, USDD and any TRC-20 token, waits while the address's free daily bandwidth is enough, and is billed per day plus per transfer that used our bandwidth. [Auto-Bandwidth](https://tronrental.com/en/auto-bandwidth)

## 2026-10-27 · API keys with the withdraw scope confirmed with 2FA

Tags: API, Withdrawals

Enabling the `withdraw` scope on an API key, changing the IP whitelist of such a key and regenerating it are now confirmed with your 2FA code or passkey. Keys issued earlier keep working. [API key scopes](https://docs.tronrental.com/api-reference/account/api-key-scopes)

## 2026-10-20 · Safe retries for withdrawals

Tags: Withdrawals, API

`POST /account/withdrawal` accepts an optional `Idempotency-Key` header: a repeated request with the same key returns the first withdrawal instead of creating a second one. With the header, the pause between withdrawals is 5 seconds instead of 60. [Withdrawals](https://docs.tronrental.com/api-reference/account/withdrawals)

## 2026-10-19 · Node API

Tags: Node API

Subscription access to the TRON HTTP and gRPC API at `node.tronrental.com`: plans with monthly quotas, a 7-day trial plan, auto-renewal and API keys managed in your dashboard. [Node API](https://tronrental.com/en/node-api)

## 2026-10-16 · Transfer Packages: at least 2 transfers per package

Tags: Transfer Packages, API

Breaking change: `POST /transfer-packages/buy` and `POST /transfer-packages/buy-invoice` reject `package_size: 1` with HTTP 422. A package holds 2 to 10,000 transfers; a single transfer is bought with `single_transfer: true`. [Buy a package](https://docs.tronrental.com/api-reference/transfer-packages/buy)

## 2026-10-16 · Transfer Packages webhooks

Tags: Transfer Packages, API

The package owner's webhook now receives 4 events: `package.transfer` for each transfer with the remaining balance, `package.completed`, `package.activated` and `package.expired`. The Telegram notification for the final transfer of a package now arrives as well. [Webhooks](https://docs.tronrental.com/api-reference/webhooks/overview)

## 2026-10-13 · Auto-Refill for energy and bandwidth

Tags: Auto-Refill, Energy, Bandwidth, API

Set a threshold for an address: when its available energy or bandwidth falls below it, we top it up from your balance automatically. Rules are managed in the dashboard, in the Telegram bot and through the API, and every refill appears in your orders. [Auto-Refill](https://tronrental.com/en/auto-refill)

## 2026-09-24 · Fee savings analyzer

Tags: Energy

The free fee savings analyzer shows what any TRON address spent on transfers over 7 days, 30 days, a year or all time and what renting energy would have cost instead, with a shareable report link. No sign-up and no wallet connection needed. [Fee savings analyzer](https://tronrental.com/en/fee-savings-analyzer)

## 2026-09-21 · Cancel a withdrawal within 20 seconds

Tags: Withdrawals, API

After you confirm a withdrawal in the dashboard, you have 20 seconds to cancel it, and the full amount including the fee returns to your balance. Withdrawals in the API show the statuses `scheduled`, `processing` and `cancelled`. [Withdrawals](https://docs.tronrental.com/api-reference/account/withdrawals)

## 2026-09-14 · Energy price quote

Tags: Energy, API

`GET /energy/quote` returns the exact total for a volume: the rental plus the fixed fee, in TRX and USD. With an API key it uses your personal price; without a key, the market price. [Quote Energy](https://docs.tronrental.com/api-reference/energy/quote)

## 2026-09-11 · Webhooks: set up in the dashboard, signed deliveries

Tags: API

Your webhook URL is now one per account and is set in the dashboard, where you also find the signing secret. Each delivery carries an `X-Webhook-Signature` header and a `timestamp` field and is made in up to 3 attempts. Breaking change: `POST /webhooks/configure` called with an API key returns HTTP 403 `FORBIDDEN_SESSION_TYPE`. [Configure webhooks](https://docs.tronrental.com/api-reference/webhooks/configure)

## 2026-09-10 · Energy Broadcaster

Tags: Broadcaster

Paste your broadcaster URL into TronLink, TokenPocket or your own code once, and your USDT transfers get energy and bandwidth automatically, paid from your TronRental balance instead of burning TRX. You decide whether a transfer is blocked or sent as usual when the balance runs out. [Energy Broadcaster](https://tronrental.com/en/energy-broadcaster)

## 2026-09-03 · API key request log

Tags: API

Open an API key in the dashboard to see its requests from the last 7 days: method, path, status, latency and IP. The key list also shows how many requests each key made in 7 days and when it was last used. [Authentication](https://docs.tronrental.com/authentication)

## 2026-08-13 · Balance history

Tags: API, Payments

Every change of your balance (orders, refunds, deposits, withdrawals, staking rewards) is listed in the All history tab of your orders and in `GET /account/history`. An order also shows the cost of activating the recipient address when it had to be activated. [Balance history](https://docs.tronrental.com/api-reference/account/history)

## 2026-08-06 · Activating an already active address

Tags: API

Activating an address that is already active on-chain no longer fails: the API answers HTTP 200 with `status: "already_activated"`, and nothing is charged. [Activate address](https://docs.tronrental.com/api-reference/energy/activate-address)

## 2026-08-03 · Buy bandwidth for any address without an account

Tags: Bandwidth, Payments

The Buy TRON Bandwidth page rents bandwidth to any address without registration: pay the invoice in TRX or USDT, or from your balance, for 1 hour or 1 day. One invoice can also combine energy and bandwidth. [Buy TRON Bandwidth](https://tronrental.com/en/buy-tron-bandwidth)

## 2026-08-02 · USDT withdrawals

Tags: Withdrawals, API

Withdraw your balance in USDT: you receive exactly the USDT amount you enter, and the exchange rate is locked while you confirm. In the API, pass `currency: "USDT"` to `POST /account/withdrawal`. [Withdrawals](https://docs.tronrental.com/api-reference/account/withdrawals)

## 2026-08-02 · Staking from your balance

Tags: Staking

Stake TRX straight from your TronRental balance, from 1 TRX and without a wallet: choose automatic compounding or simple rewards that you claim to your balance. [Staking](https://tronrental.com/en/staking)

## 2026-03-14 · Webhooks

Tags: API

Set a webhook URL in the dashboard and receive order status updates for orders placed through the API. [Webhooks](https://docs.tronrental.com/api-reference/webhooks/overview)

## 2026-02-27 · Transfer Packages

Tags: Transfer Packages, Bandwidth

Prepaid packages of USDT transfers: buy a package for an address, and each USDT transfer from it uses 1 transfer of the package. Optional BW Guarantee delegates bandwidth for the transfers too. [Transfer Packages](https://docs.tronrental.com/api-reference/transfer-packages/overview)

## 2026-02-27 · Bandwidth API

Tags: Bandwidth, API

Buy bandwidth for any TRON address through the API, for 1 hour or 1 day.

Since 2026-10-29: also for any term from 5 to 59 minutes. [Buy Bandwidth](https://docs.tronrental.com/api-reference/bandwidth/buy-bandwidth)

## 2026-02-27 · IP whitelist for API keys

Tags: API

Limit an API key to a list of IP addresses in the dashboard; requests from other addresses are rejected. [Authentication](https://docs.tronrental.com/authentication)

## 2026-02-23 · Withdrawal API

Tags: Withdrawals, API

Withdraw TRX from your balance to any TRON address through the API.

Since 2026-08-02: USDT as well. [Withdrawals](https://docs.tronrental.com/api-reference/account/withdrawals)

## 2026-02-22 · Smart Mode

Tags: Smart Mode

Automatic energy for USDT transfers: connect an address, and every USDT transfer from it gets energy without separate orders.

Since 2026-02-27: optional BW Guarantee delegates bandwidth for the transfers too. [Smart Mode](https://docs.tronrental.com/api-reference/smart-mode/overview)

## 2026-02-20 · Invoices

Tags: Energy, API

Buy energy for any address without an account: create an invoice, pay it from any wallet, and the energy is delegated after the payment arrives. [Create invoice](https://docs.tronrental.com/api-reference/invoices/create-invoice)

## 2026-02-10 · TronRental launch

Tags: Energy, Bandwidth, Payments, API

Rent TRON energy and bandwidth for any address to cut USDT transfer fees: an account balance with deposits, real-time prices, and the same features on the website and through the API. [TronRental](https://tronrental.com/en)
