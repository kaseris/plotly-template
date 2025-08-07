# Installation Guide

Quick setup guide for the Extraction Accuracy Dashboard.

## Prerequisites
- Python 3.8 or higher
- pip package manager

## Installation Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

If you encounter issues, install packages individually:
```bash
pip install dash plotly pandas numpy dash-bootstrap-components
```

### 2. Test Installation
Run the data generation test:
```bash
python3 test_data_simple.py
```

You should see: `🎉 All basic tests passed!`

### 3. Run Dashboard
```bash
python app.py
```

### 4. Open Browser
Navigate to: http://localhost:8050

## Troubleshooting

### Common Issues

**Import Errors**: Make sure all dependencies are installed
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Port Already in Use**: Change port in app.py or set environment variable
```bash
export PORT=8051
python app.py
```

**Chart Display Issues**: 
- Make sure browser JavaScript is enabled
- Try refreshing the page
- Check browser console for errors

### Dependencies
- `dash`: Web framework for Python
- `plotly`: Interactive charts
- `pandas`: Data manipulation  
- `numpy`: Numerical operations
- `dash-bootstrap-components`: UI components

## Development Mode
For development with auto-reload:
```bash
export DASH_DEBUG=True
python app.py
```

## Performance Tips
- Use Chrome or Firefox for best performance
- Close other browser tabs to free memory
- Dashboard works best on desktop screens