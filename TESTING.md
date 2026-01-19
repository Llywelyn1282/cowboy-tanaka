## Testing

### Responsiveness

All pages were tested to ensure responsiveness on screen sizes from 320px and upwards as defined in [WCAG 2.1 Reflow criteria for responsive design](https://www.w3.org/WAI/WCAG21/Understanding/reflow.html) on Chrome, Edge, Firefox and Opera browsers.

Steps to test:

1. Open browser and navigate to [cowboytanaka]()
2. Open the developer tools (right click and inspect)
3. Set to responsive and decrease width to 320px
4. Set the zoom to 50%
5. Click and drag the responsive window to maximum width

Expected:

Website is responsive on all screen sizes and no images are pixelated or stretched.
No horizontal scroll is present.
No elements overlap.

Actual:

Website behaved as expected.

Website was also opened on the following devices and no responsive issues were seen:

- Samsung A15
- iPad Pro
- Lenovo Ideapad S540

### Accessibility

Wave Accessibility tool was used throughout development and for final testing of the deployed website to check for any aid accessibility testing.

Testing was focused to ensure the following criteria were met:

- All forms have associated labels or aria-labels so that this is read out on a screen reader to users who tab to form inputs
- Color contrasts meet a minimum ratio as specified in WCAG 2.1 Contrast Guidelines
- Heading levels are not missed or skipped to ensure the importance of content is relayed correctly to the end user
- All content is contained within landmarks to ensure ease of use for assistive technology, allowing the user to navigate by page regions
- All not textual content had alternative text or titles so descriptions are read out to screen readers
- HTML page lang attribute has been set
- Aria properties have been implemented correctly
- WCAG 2.1 Coding best practices being followed
- Manual tests were also performed to ensure the website was accessible as possible and an accessibility issue was identified.

### Lighthouse Testing

#### __Home Page__

![Home Page](static/media/home-lighthouse.png)

#### __Info Page__

![Info Page](static/media/info-lighthouse.png)

#### __News Page__

![News Page](static/media/news-lighthouse.png)

#### __Tour Dates Page__

![Tour Dates Page](static/media/tour-dates-lighthouse.png)

#### __Sign Up Page__

![Sign Up](static/media/signup-lighthouse.png)

#### __Sign In Page__

![Sign In](static/media/signin-lighthouse.png)

#### __Sign Out Page__

![Sign Out](static/media/signout-lighthouse.png)


### Testing User Stories

| Goals                 | How are they achiemedia
| --------------------- | ---------------------- | 


### Functional Testing

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
|---------|------------------|-------------------|--------|-----------|


### Validator Testing 

HTML
  - No errors were returned when passing through the official [W3C Validator](https://validator.w3.org)

  ![Home HTML Validator Results](static/media/home-validation.png)

  ![About HTML Validator Results](static/media/about-validation.png)

  ![Contact HTML Validator Results](static/media/contact-validation.png)

CSS
  - No errors were found when passing through the official [Jigsaw Validator](https://jigsaw.w3.org)
  
  ![CSS Validator Results](static/media/css-validation.png)

JavaScript
 - No errors were found when passing through the official [JSHint Validator](https://www.jshint.com/)
  
  ![JavaScript Validator Results ](static/media/filters-validation.png)

  ![JavaScript Validator Results ](static/media/comments-validation.png)

Python
- No errors were found when passing through the Code Institute Python Linter [Python Validator](https://pep8ci.herokuapp.com/)



### Fixed Bugs

| Bug | Solution |
|------|-----------|

| Issue with targetting allauth buttons | Fixed with more precise targetting | 
| Favicon not displaying sitewide | Fixed incorrect href syntax |
| Product size diplay issue in bag | Found and corrected incorrectly titled parameter names in both views and bag.html. |
| Django secret key not hidden | Moved to env.py and linked in settings.py |
| Admin edit function not working on merch | Found and corrected incorrectly titled parameter names in both views and urls. |

issue with country box



### Unfixed Bugs

* No known bugs.