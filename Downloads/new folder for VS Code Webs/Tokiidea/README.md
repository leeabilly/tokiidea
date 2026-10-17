# Tokiidea - Handmade Plushie Store

## What's Been Set Up

This repository contains a starter template for your Tokiidea handmade plushie store, built with:

- **HTML5/CSS3** (vanilla, no frameworks)
- **Responsive design** (mobile-friendly)
- **Pastel + neutral color scheme** inspired by choutopia.com and thepigroom.com
- **Clean, simple layout** inspired by yeezy.com
- **Basic pages**: Homepage, Product detail page
- **Placeholder sections** for About, Contact, FAQ, and policy pages
- **Stripe-ready structure** (you'll add your Stripe integration)

## File Structure
```
Tokiidea/
├── index.html              # Homepage
├── product.html            # Product detail page template
├── css/
│   └── style.css           # Main stylesheet with design tokens
├── images/                 # Add your product photos here
├── assets/                 # For logo, icons, etc.
└── [Other pages to create: about.html, contact.html, faq.html, etc.]
```

## Next Steps for You

### 1. Add Your Assets
- Place your **logo** in the `assets/` folder
- Add your **product photos** to the `images/` folder
- Consider adding a favicon

### 2. Customize the Content
- Update `index.html`:
  - Replace the placeholder product card with your actual product
  - Update hero text to match your brand voice
  - Add real links in the navigation
- Update `product.html`:
  - Replace placeholder text with your actual product description, details, and pricing
  - Add real product images
- Create additional pages:
  - `about.html` - Your story and maker bio
  - `contact.html` - Contact form or information
  - `faq.html` - Frequently asked questions
  - Policy pages: `shipping.html`, `returns.html`, `privacy.html`, `terms.html`, `cookies.html`

### 3. Refine the Design (Optional)
- Open `css/style.css` to adjust:
  - **Color variables** (`--pastel-pink`, `--pastel-blue`, etc.) to match your exact preferences
  - **Typography** (font families in `:root`)
  - **Spacing** and layout preferences
- The CSS uses CSS variables, so changing them in `:root` updates everything

### 4. Add E-commerce Functionality
For the MVP, you have a few options:

**Option A: Simple Stripe Buy Buttons** (Recommended for start)
- Add Stripe Checkout buttons on product pages
- Use Stripe's pre-built checkout for security and simplicity
- I can help you add this once you're ready

**Option B: Full Cart System**
- More complex, requires JavaScript
- Better for larger inventories
- Can be added later

### 5. Create Your Policies
Refer to `POLICIES_GUIDANCE.md` for templates you can customize for:
- Shipping policy
- Returns & refunds
- Privacy policy
- Terms of service
- Cookies policy

### 6. Test & Launch
- Test locally by opening `index.html` in your browser
- Check mobile responsiveness
- Test any forms or Stripe integration
- Deploy to:
  - GitHub Pages (free)
  - Netlify (free tier)
  - Vercel (free tier)
  - Or any static web host

## Design Notes

### Color Palette (Customize in css/style.css):
- **Pastel Pink**: `#F8EDEB` (--pastel-pink)
- **Pastel Blue**: `#E8F4FD` (--pastel-blue)
- **Pastel Green**: `#E8F5E9` (--pastel-green)
- **Pastel Lavender**: `#F3E5F5` (--pastel-lavender)
- **Neutral White**: `#FFFFFF` (--neutral-white)
- **Neutral Light**: `#F5F5F5` (--neutral-light)
- **Accent Sage**: `#D4B483` (--accent-sage)
- **Accent Rose**: `#E6B3AA` (--accent-rose)

### Typography:
- **Headings**: Quicksand, Nunito, or system-ui sans-serif
- **Body**: Inter, Helvetica Neue, or Arial sans-serif

### Whimsical Touches to Consider:
- Subtle doodle icons in headers/footers
- Playful badges on products ("Made to Order", "Limited Edition")
- Slightly rounded corners on elements
- Handwritten-style accents for headings or quotes
- Small illustrated details (stars, hearts, etc.) as bullet points or dividers

## Need Help?

Just ask! I can help you:
- Add your actual product photos and descriptions
- Set up Stripe Checkout
- Create additional pages
- Refine the design based on your feedback
- Add any features you envision for Tokiidea

Remember: You're in charge of the design and build process. I'm here to provide technical guidance and implementation help while you make all the creative decisions for your beautiful handmade plushie store! 🧸✨