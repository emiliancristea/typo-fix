# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- Custom keyboard shortcuts configuration
- Offline correction mode
- Plugin system for popular text editors
- Team/Enterprise features
- Mobile companion app
- Advanced formatting preservation

## [1.2.0] - 2024-01-XX

### Added
- Enhanced widget positioning algorithm for better placement near selected text
- Multi-monitor support with intelligent screen detection
- Improved Windows API integration for text selection positioning
- System tray icon with context menu
- Comprehensive testing scenarios and documentation

### Changed
- Upgraded to modern rounded button design with better visual feedback
- Improved error handling and debug output
- Enhanced UI with transparent backgrounds and better positioning
- Optimized API response processing and cleanup

### Fixed
- Widget positioning issues on high-DPI displays
- Text selection detection improvements
- Memory management and cleanup processes
- Focus handling for paste operations

## [1.1.0] - 2024-01-XX

### Added
- **Multi-language support** with automatic language detection
  - English, Spanish, French, German, Romanian, and more
- **Language preservation** - no unwanted translations
- Two distinct correction modes:
  - **Fix Mode**: Corrects typos and grammar errors only
  - **Rewrite Mode**: Improves clarity, structure, and logical flow
- Enhanced AI prompts for better accuracy
- Improved user interface with 3-button widget design

### Changed
- Switched to Google Gemini AI for better language processing
- Enhanced text processing pipeline with language detection
- Improved widget design with better button layout
- Updated API integration for more reliable responses

### Fixed
- Language detection accuracy improvements
- Better handling of special characters and formatting
- Improved clipboard operations reliability

## [1.0.0] - 2024-01-XX

### Added
- **Initial release** of TypoFix
- Core functionality for typo correction and text improvement
- Global Ctrl+C hotkey detection across all Windows applications
- Floating widget interface with Fix/Cancel options
- System tray integration for background operation
- PyInstaller executable packaging
- Google Gemini AI integration for text processing
- Multi-application compatibility (browsers, Office, text editors, etc.)

### Features
- Zero-configuration setup
- Portable single executable
- Real-time text correction
- Smart clipboard integration
- Universal Windows application support
- Embedded API key for immediate use

---

## Version Numbering

- **Major version (X.y.z)**: Breaking changes or major feature additions
- **Minor version (x.Y.z)**: New features, improvements, non-breaking changes
- **Patch version (x.y.Z)**: Bug fixes, small improvements, documentation updates

## Contributing

When contributing, please:
1. Update this changelog with your changes
2. Follow the format above
3. Add entries to the "Unreleased" section
4. Use clear, descriptive language
5. Include issue numbers where applicable 