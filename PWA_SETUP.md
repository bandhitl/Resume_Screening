# PWA Setup Guide

Your Resume Screening application has been converted to a Progressive Web App (PWA) that can be installed on mobile devices!

## What's New

### PWA Features Added:
- ✅ **Installable**: Can be installed on mobile and desktop
- ✅ **Offline Support**: Works with limited offline functionality
- ✅ **Mobile Optimized**: Touch-friendly interface with responsive design
- ✅ **App-like Experience**: Full-screen mode on mobile devices
- ✅ **Service Worker**: Caches static assets for faster loading
- ✅ **Install Prompts**: Automatic install button on supported browsers

## Setup Instructions

### 1. Generate App Icons

Run the icon generator script:

```bash
python generate_icons.py
```

Or use online tools like:
- https://realfavicongenerator.net/
- https://www.pwabuilder.com/imageGenerator

Place icons in `static/icons/` directory.

Required sizes:
- 16x16, 32x32 (favicon)
- 72x72, 96x96, 128x128, 144x144, 152x152 (Android)
- 192x192, 384x384, 512x512 (PWA)

### 2. Serve the Application

Start your Flask app:

```bash
python app.py
```

**Important**: PWAs require HTTPS to work (except on localhost). For production:
- Use a reverse proxy (nginx, Apache) with SSL
- Or use cloud platforms (Heroku, AWS, Google Cloud)
- For testing locally, use `http://localhost:5000`

### 3. Install on Mobile Devices

#### Android (Chrome):
1. Open the app in Chrome browser
2. Tap the menu (three dots)
3. Select "Install app" or "Add to Home Screen"
4. Confirm installation

#### iOS (Safari):
1. Open the app in Safari browser
2. Tap the Share button
3. Scroll down and tap "Add to Home Screen"
4. Tap "Add" to confirm

#### Desktop:
1. Open the app in Chrome/Edge
2. Click the install icon in the address bar
3. Click "Install"

## Mobile Optimizations

The app now includes:
- Touch-friendly buttons (minimum 44x44px)
- No zoom on input focus (iOS fix)
- Safe area support for notched devices
- Responsive layout for all screen sizes
- Full-screen standalone mode
- Smooth scrolling and animations

## Testing PWA

### Chrome DevTools:
1. Open DevTools (F12)
2. Go to "Application" tab
3. Check "Manifest" and "Service Workers" sections
4. Use "Lighthouse" to audit PWA features

### Test Offline:
1. Install the app
2. Put device in airplane mode
3. Open the app - should load cached content

## Files Created/Modified

### New Files:
- `static/manifest.json` - PWA manifest
- `static/service-worker.js` - Service worker for caching
- `generate_icons.py` - Icon generation script
- `PWA_SETUP.md` - This file

### Modified Files:
- `app.py` - Added PWA file serving routes
- `templates/index.html` - Added PWA meta tags and service worker
- `templates/login.html` - Added PWA meta tags and mobile optimization

## Deployment

### For Production with HTTPS:

#### Option 1: ngrok (Testing)
```bash
# Install ngrok
brew install ngrok  # macOS
# Or download from https://ngrok.com

# Run your app
python app.py

# In another terminal, create HTTPS tunnel
ngrok http 5000
```

#### Option 2: Heroku
Create `Procfile`:
```
web: python app.py
```

Deploy:
```bash
heroku create your-app-name
git push heroku main
```

#### Option 3: VPS with nginx
See `WEB_SETUP_GUIDE.md` for detailed nginx setup with SSL.

## Customization

### Change App Name:
Edit `static/manifest.json`:
```json
{
  "name": "Your App Name",
  "short_name": "App",
  ...
}
```

### Change Theme Color:
Update color in:
- `static/manifest.json` - `"theme_color"`
- `templates/*.html` - `<meta name="theme-color">`

### Customize Install Prompt:
Edit the service worker registration script in `templates/index.html`.

## Troubleshooting

### Service Worker Not Installing:
- Ensure you're serving via HTTPS or localhost
- Check browser console for errors
- Clear cache and reload: DevTools > Application > Clear storage

### Install Prompt Not Showing:
- Visit the site at least twice (PWA criteria)
- Ensure HTTPS is enabled
- Check if already installed
- Try on Chrome/Edge for best support

### Icons Not Showing:
- Verify icon files exist in `static/icons/`
- Check file paths in `manifest.json`
- Ensure correct MIME types are served

## Benefits

PWA provides:
- **Better Performance**: Cached assets load instantly
- **Increased Engagement**: Installed apps are used more frequently
- **Cost Effective**: No app store approval needed
- **Automatic Updates**: Always loads latest version
- **Cross-Platform**: Works on iOS, Android, and desktop

## Next Steps

1. Generate and customize icons
2. Test on multiple devices
3. Deploy with HTTPS
4. Add push notifications (optional)
5. Monitor usage with analytics

For questions or issues, refer to:
- https://web.dev/progressive-web-apps/
- https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps
