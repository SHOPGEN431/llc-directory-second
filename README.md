# LLC Directory Website

A Flask-based business directory website similar to Angie's List, designed to showcase LLCs and businesses organized by state and city.

## Features

- **Homepage**: Search functionality with filters for state, city, and business category
- **State Pages**: Browse all businesses in a specific state
- **City Pages**: View businesses in a specific city within a state
- **SEO Optimized**: XML sitemap, robots.txt, and meta tags for search engines
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5
- **Modern UI**: Clean, professional design with hover effects and animations

## Data Source

The website uses data from the CSV file located at:
```
C:\Users\webd5\Downloads\LLC Data.csv
```

The CSV contains business information including:
- Business name
- Category/type
- Address (street, city, state)
- Phone number
- Website URL
- Ratings and reviews
- Business description

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure the CSV file is available**:
   Make sure the file `C:\Users\webd5\Downloads\LLC Data.csv` exists and is accessible.

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the website**:
   Open your browser and go to `http://localhost:5000`

## Project Structure

```
llc directory second/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Homepage template
│   ├── state.html        # State page template
│   └── city.html         # City page template
└── static/               # Static files
    ├── css/
    │   └── style.css     # Custom CSS styles
    └── js/
        └── main.js       # JavaScript functionality
```

## URL Structure

- **Homepage**: `/`
- **State Page**: `/state/<state-name>` (e.g., `/state/florida`)
- **City Page**: `/state/<state-name>/<city-name>` (e.g., `/state/florida/tampa`)
- **API Search**: `/api/search?q=<query>`
- **Sitemap**: `/sitemap.xml`
- **Robots**: `/robots.txt`

## Features Explained

### Search and Filtering
- Search by business name, category, or location
- Filter by state, city, and business category
- Real-time search suggestions (AJAX)

### Business Listings
- Display business cards with key information
- Show ratings and reviews when available
- Contact information (phone, website)
- Location details

### Navigation
- Breadcrumb navigation for easy browsing
- State and city navigation menus
- Related cities suggestions

### SEO Features
- SEO-friendly URLs
- Meta descriptions and keywords
- Open Graph tags for social media
- XML sitemap generation
- Robots.txt file

## Customization

### Adding New Features
1. **New Routes**: Add new route functions in `app.py`
2. **New Templates**: Create HTML templates in the `templates/` folder
3. **Styling**: Modify `static/css/style.css` for design changes
4. **Functionality**: Update `static/js/main.js` for JavaScript features

### Data Modifications
- The application automatically reads from the CSV file
- No database setup required
- Data is loaded into memory on startup

### Styling
- Uses Bootstrap 5 for responsive design
- Custom CSS for enhanced styling
- Font Awesome icons for visual elements

## Performance Considerations

- Data is loaded once on startup for better performance
- Search results are limited to 50 items per page
- Images use lazy loading for better page load times
- AJAX search for real-time suggestions

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile-responsive design
- Progressive enhancement for older browsers

## Deployment

For production deployment:

1. **Set environment variables**:
   ```bash
   export FLASK_ENV=production
   ```

2. **Use a production WSGI server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Configure a reverse proxy** (nginx recommended)

4. **Set up SSL certificates** for HTTPS

## Troubleshooting

### Common Issues

1. **CSV file not found**:
   - Ensure the file path is correct
   - Check file permissions

2. **Port already in use**:
   - Change the port in `app.py` or kill the existing process

3. **Template errors**:
   - Check that all template files exist
   - Verify Jinja2 syntax

4. **Performance issues**:
   - Consider pagination for large datasets
   - Implement caching for frequently accessed data

## Support

For issues or questions:
1. Check the console output for error messages
2. Verify the CSV file format and content
3. Ensure all dependencies are installed correctly

## License

This project is open source and available under the MIT License.







