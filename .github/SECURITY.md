# Security Policy

## 🔒 Supported Versions

We actively support and provide security updates for the following versions of TypoFix:

| Version | Supported          |
| ------- | ------------------ |
| 1.2.x   | ✅ Yes             |
| 1.1.x   | ✅ Yes             |
| 1.0.x   | ⚠️ Limited support |
| < 1.0   | ❌ No              |

## 🚨 Reporting a Vulnerability

We take the security of TypoFix seriously. If you believe you have found a security vulnerability, please follow these guidelines:

### 📧 Contact Information

**Please DO NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them by emailing: **[your-email@domain.com]**

### 📋 What to Include

When reporting a vulnerability, please include:

1. **Description**: A clear description of the vulnerability
2. **Impact**: How the vulnerability could be exploited
3. **Steps to Reproduce**: Detailed steps to reproduce the issue
4. **Environment**: 
   - Operating System version
   - TypoFix version
   - Python version (if applicable)
5. **Evidence**: Screenshots, logs, or code samples (if safe to share)

### 🔄 Response Process

1. **Acknowledgment**: We will acknowledge receipt of your vulnerability report within 48 hours
2. **Investigation**: We will investigate the report and determine its validity and severity
3. **Communication**: We will keep you informed about our progress during the investigation
4. **Resolution**: We will work to resolve the vulnerability as quickly as possible
5. **Disclosure**: We will coordinate with you on public disclosure timing

### ⏱️ Response Timeline

- **Initial Response**: Within 48 hours
- **Severity Assessment**: Within 5 business days
- **Fix Development**: Varies based on complexity and severity
- **Public Disclosure**: After fix is released (coordinated with reporter)

## 🛡️ Security Considerations

### 🔑 API Key Security

TypoFix includes an embedded Google Gemini API key for immediate functionality. However:

- **For production use**: We recommend using your own API key
- **Key rotation**: The embedded key may be rotated periodically
- **Rate limiting**: The embedded key has usage limitations

### 🌐 Network Security

- All API communications use HTTPS encryption
- No sensitive user data is stored locally
- Text data is only sent to Google's Gemini API for processing
- No telemetry or analytics data is collected

### 💻 System Security

- TypoFix requires minimal system permissions
- Global hotkey detection uses standard Windows APIs
- No administrative privileges required for normal operation
- Clipboard access is limited to text correction functionality

### 🔒 Data Privacy

- **Text processing**: User text is sent to Google Gemini API for correction
- **No storage**: Corrected text is not stored anywhere permanently
- **No logging**: User text content is not logged by TypoFix
- **Local operation**: All functionality except AI processing happens locally

## 🚀 Security Best Practices

### For Users

1. **Download from official sources**: Only download TypoFix from official GitHub releases
2. **Verify checksums**: Verify file integrity when provided
3. **Keep updated**: Use the latest version for security patches
4. **Network security**: Ensure your internet connection is secure
5. **Sensitive content**: Be mindful when correcting sensitive/confidential text

### For Developers

1. **Code review**: All code changes undergo security review
2. **Dependencies**: Regular updates of dependencies for security patches
3. **Static analysis**: Automated security scanning of code
4. **Secure coding**: Following secure coding practices
5. **API security**: Proper handling of API keys and responses

## 🔍 Known Security Considerations

### Current Limitations

1. **Text privacy**: Text sent to AI API is processed by Google servers
2. **Network dependency**: Requires internet connection for AI features
3. **API rate limits**: Embedded API key has usage limitations
4. **Windows-only**: Currently only supports Windows operating system

### Mitigation Strategies

1. **Custom API keys**: Users can configure their own API keys
2. **Selective usage**: Users can choose when to use correction features
3. **Local alternatives**: Future versions may include offline correction
4. **Transparency**: Clear documentation of data handling practices

## 📚 Additional Resources

- [Privacy Policy](https://github.com/emiliancristea/typo-fix#-usage)
- [Contributing Guidelines](https://github.com/emiliancristea/typo-fix/blob/main/CONTRIBUTING.md)
- [Code of Conduct](https://github.com/emiliancristea/typo-fix/blob/main/CODE_OF_CONDUCT.md)

## 🏆 Recognition

We appreciate security researchers who help improve TypoFix's security. Responsible disclosure contributors will be acknowledged in our:

- Security advisory (if applicable)
- Release notes
- Hall of fame section (with permission)

Thank you for helping keep TypoFix and our users safe! 🛡️ 