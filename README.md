# 12L

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Frontend: Angular](https://img.shields.io/badge/Frontend-Angular-dd0031.svg)](https://angular.dev)
[![Backend: .NET](https://img.shields.io/badge/Backend-.NET-512bd4.svg)](https://dotnet.microsoft.com)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)

12L is an open marketplace for new and used men's clothing in two sizes only: **size 12 shoes** and **size large (L) clothing**. Anyone can join, list what they no longer wear, and buy from people who wear the same size.

The name says it all: **12** for the shoes, **L** for the clothes.

12L is a full-stack, responsive web application with an [Angular](https://angular.dev) frontend and a [.NET](https://dotnet.microsoft.com) backend.

## Table of contents

- [Why 12L](#why-12l)
- [How it works](#how-it-works)
- [What you can sell](#what-you-can-sell)
- [Features](#features)
- [Architecture](#architecture)
- [Getting started](#getting-started)
  - [Prerequisites](#prerequisites)
- [Project structure](#project-structure)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Code of conduct](#code-of-conduct)
- [Security](#security)
- [Support](#support)
- [License](#license)

## Why 12L

General marketplaces make you filter through thousands of listings that will never fit. 12L removes the guesswork. Every listing on 12L is either a size 12 shoe or a size large garment, so every item a buyer sees is one they can wear.

## How it works

1. **Join.** Anyone can create an account. There is no seller approval step.
2. **List.** Sellers photograph an item, describe its condition, and set a price.
3. **Browse.** Buyers browse a catalog where everything is already in their size.
4. **Buy.** Buyers purchase the item and the seller ships it.
5. **Review.** Buyers and sellers rate each other after the sale.

## What you can sell

| Category | Accepted size | Condition |
| --- | --- | --- |
| Shoes (sneakers, boots, dress shoes, sandals) | Men's US 12 | New or used |
| Tops (shirts, t-shirts, sweaters, hoodies) | Men's L | New or used |
| Outerwear (jackets, coats) | Men's L | New or used |
| Bottoms (pants, shorts) | Men's L | New or used |

Listings in any other size are out of scope for 12L and are not accepted.

## Features

- **Open to everyone.** Any member can buy and sell.
- **Size-locked catalog.** Only men's size 12 shoes and size large clothing can be listed.
- **New and used.** Sellers mark each item as new, new with tags, or used, with a condition grade.
- **Seller profiles.** Each seller has a public profile with their listings and ratings.
- **Search and filters.** Filter by category, brand, condition and price.
- **Responsive.** One web app that works on phones, tablets and desktops.

## Architecture

| Layer | Technology | Responsibility |
| --- | --- | --- |
| Frontend | Angular (TypeScript) | Responsive single-page app for browsing, listing, buying and managing an account |
| Backend | .NET (C#, ASP.NET Core Web API) | REST API for members, listings, orders and reviews, and enforcement of the size rules |

The Angular app calls the ASP.NET Core API over HTTPS. The backend is the source of truth for the size rules: it rejects any listing that is not a men's size 12 shoe or a men's size large garment, whatever the client sends.

## Getting started

12L is in its early planning stage. Application code and run instructions will be added here as the project takes shape.

### Prerequisites

- [.NET SDK](https://dotnet.microsoft.com/download) (latest LTS)
- [Node.js](https://nodejs.org) (latest LTS) and npm
- [Angular CLI](https://angular.dev/tools/cli) (`npm install -g @angular/cli`)
- [Git](https://git-scm.com)

### Clone the repository

```bash
git clone https://github.com/QuinntyneBrown/12l.git
cd 12l
```

## Project structure

```text
12l/
├── .agents/skills/        Agent skills (shared, tool-agnostic copy)
├── .claude/skills/        Agent skills for Claude Code
├── .github/               Issue templates, pull request template, Copilot instructions
├── src/backend/           .NET backend (planned)
├── src/frontend/          Angular frontend (planned)
├── AGENTS.md              Working agreement for coding agents
├── CLAUDE.md              Instructions for Claude Code
├── GEMINI.md              Instructions for Gemini
├── CHANGELOG.md           Release history
├── CODE_OF_CONDUCT.md     Contributor Covenant
├── CONTRIBUTING.md        How to contribute
├── LICENSE                MIT License
├── SECURITY.md            Security policy
└── SUPPORT.md             How to get help
```

## Documentation

- [CONTRIBUTING.md](CONTRIBUTING.md) explains how to propose changes.
- [AGENTS.md](AGENTS.md) is the working agreement for AI coding agents.
- [CHANGELOG.md](CHANGELOG.md) records notable changes.

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or a pull request.

## Code of conduct

This project has adopted the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating you are expected to uphold it.

## Security

Please do not report security vulnerabilities through public issues. See [SECURITY.md](SECURITY.md) for how to report them privately.

## Support

See [SUPPORT.md](SUPPORT.md) for how to file issues and get help.

## License

12L is licensed under the [MIT License](LICENSE).
