# TypoFix Testing Scenarios

## 🧪 **Comprehensive Test Cases**

### **1. Multi-Language Testing**
Try these texts in different languages:

**English with typos:**
```
Ths is a tets with som etypos and gramar erors.
```

**Spanish with errors:**
```
Hola, me gsta mucho este aplicacon para corregr textos.
```

**French with mistakes:**
```
Bonjor, j'ai besoins d'aide pour corriger ce texte.
```

**German with typos:**
```
Hallo, das ist ein Test mit Rechtschreibfhlern.
```

### **2. Application Compatibility Testing**
Test in these applications:
- ✅ **Web Browsers**: Chrome, Firefox, Edge, Safari
- ✅ **Microsoft Office**: Word, Excel, PowerPoint, Outlook  
- ✅ **Text Editors**: Notepad, VS Code, Sublime Text
- ✅ **Chat Apps**: Discord, Slack, WhatsApp Web, Teams
- ✅ **Email**: Gmail, Yahoo Mail, Outlook Web
- ✅ **Social Media**: Twitter, Facebook, LinkedIn

### **3. Text Type Testing**

**Professional Email:**
```
Dears Collegues, I hope this emial finds you wel. I wanted to discus the projekt timeline.
```

**Technical Documentation:**
```
The API endpont returnes a JSON responce with the user data and acess token.
```

**Creative Writing:**
```
The qick brown fox jumpd over the layz dog in the beatiful garden.
```

**Academic Text:**
```
The researc metodology empleyed in this studie was a mixed-method aproach.
```

### **4. Edge Cases Testing**

**Very Short Text:**
```
teh cat
```

**Very Long Text:**
```
This is a very long text with multiple sentences that contains various types of errors including spelling mistakes, grammatical errors, and formatting issues that need to be corrected by the application to test its capabilities with longer content.
```

**Mixed Languages:**
```
Hello, me llamo Juan and ich bin ein developer.
```

**Special Characters:**
```
The API costs $19.99/month & includes 100% uptime garantee!
```

### **5. Button Function Testing**

**✓ Fix Button Test:**
- Should only correct spelling/grammar errors
- Should preserve original meaning exactly
- Should maintain same language

**📝 Rewrite Button Test:**
- Should improve clarity and flow
- Should preserve all original information
- Should maintain same tone and style

**✗ Cancel Button Test:**
- Should close widget immediately
- Should not make any changes to original text

### **6. System Integration Testing**

**Multi-Monitor Setup:**
- Test widget positioning across different monitors
- Verify it appears on the active monitor

**High DPI Displays:**
- Check button rendering quality
- Verify text readability

**Window Focus:**
- Test with different applications in focus
- Verify paste operation works correctly

### **7. Performance Testing**

**API Response Time:**
- Monitor response times for different text lengths
- Test with poor internet connection

**Memory Usage:**
- Leave app running for extended periods
- Monitor system resource usage

**Multiple Corrections:**
- Perform many corrections in sequence
- Check for memory leaks or slowdowns

## ✅ **Success Criteria**

For each test:
1. **Widget appears** within 2 seconds of Ctrl+C
2. **Correct positioning** near selected text
3. **API processing** completes within 10 seconds
4. **Language preservation** - no unwanted translations
5. **Automatic paste** works correctly
6. **System tray** remains functional

## 🐛 **What to Report**

If you encounter issues, note:
- Exact text that caused the problem
- Which application you were using
- Which button you clicked
- Any error messages in the terminal
- Expected vs. actual behavior

## 💡 **Pro Testing Tips**

1. **Keep terminal visible** to see debug output
2. **Test different text lengths** (short, medium, long)
3. **Try various applications** to ensure compatibility
4. **Test both buttons** (Fix vs. Rewrite) to see differences
5. **Use languages you're familiar with** to verify quality
6. **Check positioning** on different screen areas 