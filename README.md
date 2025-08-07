# Extraction Accuracy Dashboard

A comprehensive, responsive dashboard for visualizing extraction accuracy metrics using Plotly Dash. Built with accessibility in mind and following modern web development best practices.

## 🎯 Features

### Core Functionality
- **Primary KPI Cards**: Large, color-coded displays for key metrics
- **Interactive Gauge Charts**: Visual representation with threshold indicators
- **Quarterly Trend Analysis**: Line charts showing performance over time
- **Monthly Heatmap**: Detailed drill-down for monthly performance

### Design & Accessibility
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **WCAG 2.1 AA Compliance**: Screen reader support, keyboard navigation, high contrast
- **Color-blind Friendly**: Uses patterns in addition to color coding
- **Progressive Enhancement**: Works without JavaScript for basic functionality

### Technical Features
- **Modular Architecture**: Clean separation of components, data, and layouts
- **Sample Data Generator**: Realistic data with seasonal variations
- **Export Functionality**: CSV download capability
- **Performance Optimized**: Lazy loading and responsive charts

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda for package management

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd plotly-template
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open browser**
   Navigate to `http://localhost:8050`

## 📊 Dashboard Overview

### Primary Metrics
- **Extraction Accuracy**: Overall system performance
- **Document Accuracy**: Document-level processing success
- **All Fields Accuracy**: Comprehensive field extraction performance

### Color Coding System
- 🟢 **Green (≥90%)**: Excellent performance
- 🟡 **Yellow (75-89%)**: Good performance, monitor closely  
- 🔴 **Red (<75%)**: Bad performance, needs immediate attention

### Data Views
1. **Overview**: KPI cards and gauge charts
2. **Monthly Carousel**: Interactive quarter-based monthly performance cards
3. **Monthly Details**: Granular monthly breakdown (heatmap)

## 🏗️ Project Structure

```
plotly-template/
├── app.py                  # Main application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── CLAUDE.md              # AI assistant guidance
├── assets/                # CSS, images, static files
│   └── custom_styles.css  # Dashboard styling
├── src/                   # Source code modules
│   ├── components/        # Reusable UI components
│   │   ├── kpi_cards.py   # KPI card components
│   │   └── gauge_charts.py # Gauge chart components
│   ├── data/              # Data processing
│   │   └── sample_data.py # Sample data generators
│   ├── layouts/           # Page layouts
│   │   └── main_layout.py # Main dashboard layout
│   └── utils/             # Helper functions
└── tests/                 # Test files
```

## 🔧 Configuration

### Environment Variables
- `DASH_DEBUG`: Enable/disable debug mode (default: True)
- `PORT`: Server port (default: 8050)

### Customization
- **Colors**: Modify color schemes in `assets/custom_styles.css`
- **Data**: Replace sample data in `src/data/sample_data.py`
- **Layout**: Adjust responsive breakpoints in `src/layouts/main_layout.py`

## 🎨 Customization Guide

### Adding New Metrics
1. Update `MetricsDataGenerator` in `src/data/sample_data.py`
2. Create new component in `src/components/`
3. Add to main layout in `src/layouts/main_layout.py`
4. Update `app.py` to include new component

### Modifying Thresholds
Update color thresholds in gauge chart configurations:
```python
thresholds = {'excellent': 95, 'good': 90, 'poor': 0}
```

### Custom Styling
Modify `assets/custom_styles.css` for:
- Color schemes
- Typography
- Responsive breakpoints
- Animation preferences

## 🧪 Testing

Run tests with pytest:
```bash
pip install pytest pytest-dash
pytest tests/
```

## 📱 Responsive Design

### Breakpoints
- **Mobile**: < 768px (single column layout)
- **Tablet**: 768px - 1199px (stacked layout)
- **Desktop**: ≥ 1200px (full dashboard layout)

### Mobile Features
- Collapsible navigation sidebar
- Touch-friendly controls
- Optimized chart sizing
- Simplified interactions

## ♿ Accessibility Features

- **Screen Reader Support**: Proper ARIA labels and semantic HTML
- **Keyboard Navigation**: All interactive elements accessible via keyboard
- **High Contrast**: Support for high contrast mode
- **Color Alternatives**: Patterns and text labels in addition to colors
- **Focus Management**: Clear focus indicators

## 🔍 Performance Considerations

- **Lazy Loading**: Charts load on demand
- **Client-side Caching**: Reduces server requests
- **Responsive Images**: Optimized for different screen sizes
- **Minimal Dependencies**: Only essential libraries included

## 🚀 Deployment

### Development
```bash
python app.py
```

### Production (using Gunicorn)
```bash
gunicorn app:server --bind 0.0.0.0:8050
```

### Docker (optional)
```bash
# Build image
docker build -t extraction-dashboard .

# Run container
docker run -p 8050:8050 extraction-dashboard
```

## 📈 Data Integration

### Real Data Integration
Replace sample data generator with your data source:

1. **Database Connection**: Add connection logic in `src/data/`
2. **API Integration**: Create API client for external data
3. **File Processing**: Add CSV/JSON file processors
4. **Real-time Updates**: Implement WebSocket or polling for live data

### Data Format
Expected data structure:
```python
{
    'primary_metrics': {
        'extraction_accuracy': float,
        'document_accuracy': float,
        'all_fields_accuracy': float
    },
    'quarterly_data': pd.DataFrame,  # columns: quarter, field_1_accuracy, etc.
    'monthly_data': pd.DataFrame     # columns: year, month, field_accuracies
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

- **Issues**: Report bugs and feature requests via GitHub Issues
- **Documentation**: Additional docs in `docs/` directory
- **Community**: Join our discussion forum for help

## 🔄 Version History

- **v1.0.0**: Initial release with core dashboard functionality
- **Phase 1**: KPI cards, gauge charts, responsive layout
- **Phase 2**: Interactive features, accessibility enhancements (planned)
- **Phase 3**: Advanced analytics, export features (planned)

---

Built with ❤️ using [Plotly Dash](https://dash.plotly.com/) and [Bootstrap](https://getbootstrap.com/)