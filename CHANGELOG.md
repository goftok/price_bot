# Changelog

All notable changes to the Price Bot project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1](https://github.com/goftok/price_bot/releases/tag/0.0.1) - 03-04.2024

### Added

- Initial release of the Price Bot project.
- Functionality to track changes in prices on Marktplaats.nl and 2dehands.be.
- Feature to send notifications to specified Telegram channels when new ads are detected.
- Basic config implementation for setting up tracking parameters and preferences.

### Known Issues

- 429 errors appear frequently when scraping websites
- For some ads, the price is not detected correctly (e.g. 4.5 instead of 4500)

## [0.0.2](https://github.com/goftok/price_bot/releases/tag/0.0.2) - 27-08.2024

### Added
- Implemented parsing of 2dehands ads into Otomoto search.
- Integrated price comparison between the ad and Otomoto listings.
- Introduced regex-based extraction for the vehicle's year from the title and description.
- Added more unit tests

### Known Issues
- Parameters for determining the suggested price from Otomoto need fine-tuning to improve accuracy.
- Regex logic for extracting the car’s year requires further refinement for cases where the year is not directly available from 2dehands parameters.