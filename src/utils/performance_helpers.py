"""
Performance optimization utilities for dashboard components.
Provides caching, lazy loading, and optimization helpers.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from typing import Dict, Any, Optional, Callable
import time
import hashlib
import json
from functools import wraps


class DataCache:
    """Simple in-memory cache for dashboard data."""
    
    def __init__(self, ttl_seconds: int = 300):  # 5 minute default TTL
        self.cache = {}
        self.ttl = ttl_seconds
    
    def _generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from function arguments."""
        key_data = str(args) + str(sorted(kwargs.items()))
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired."""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        """Cache a value with timestamp."""
        self.cache[key] = (value, time.time())
    
    def clear(self) -> None:
        """Clear all cached data."""
        self.cache.clear()


# Global cache instance
dashboard_cache = DataCache(ttl_seconds=300)


def cached_computation(func: Callable) -> Callable:
    """
    Decorator for caching expensive computations.
    
    Args:
        func: Function to cache
    
    Returns:
        Wrapped function with caching
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        cache_key = dashboard_cache._generate_key(*args, **kwargs)
        
        # Try to get from cache
        cached_result = dashboard_cache.get(cache_key)
        if cached_result is not None:
            return cached_result
        
        # Compute and cache result
        result = func(*args, **kwargs)
        dashboard_cache.set(cache_key, result)
        return result
    
    return wrapper


def create_loading_placeholder(component_id: str, min_height: str = "400px") -> html.Div:
    """
    Create a loading placeholder for components.
    
    Args:
        component_id: ID of the component being loaded
        min_height: Minimum height to maintain layout
    
    Returns:
        Loading placeholder HTML
    """
    return html.Div([
        dbc.Spinner(
            children=[
                html.Div([
                    html.Div(className="placeholder-glow"),
                    html.Div([
                        html.Span(className="placeholder col-6"),
                        html.Span(className="placeholder col-4"),
                        html.Span(className="placeholder col-4"),
                        html.Span(className="placeholder col-6"),
                        html.Span(className="placeholder col-8"),
                    ], className="mt-3")
                ], className="text-center p-4")
            ],
            color="primary",
            type="border"
        )
    ], 
    id=f"{component_id}-loading",
    className="loading-placeholder d-flex align-items-center justify-content-center",
    style={'minHeight': min_height}
    )


def create_intersection_observer_trigger(component_id: str) -> html.Div:
    """
    Create a trigger element for intersection observer lazy loading.
    
    Args:
        component_id: ID of the component to lazy load
    
    Returns:
        Trigger element for intersection observer
    """
    return html.Div(
        id=f"{component_id}-trigger",
        className="intersection-trigger",
        **{"data-component": component_id}
    )


def optimize_plotly_config() -> Dict[str, Any]:
    """
    Get optimized Plotly configuration for better performance.
    Based on context7 documentation for Plotly.py configuration optimization.
    
    Returns:
        Dictionary of Plotly config options
    """
    return {
        # Performance optimizations
        'displayModeBar': True,  # Show modebar but remove unnecessary buttons
        'displaylogo': False,  # Hide Plotly logo for cleaner appearance
        'responsive': True,  # Enable responsive behavior
        'doubleClickDelay': 300,  # Optimize double-click responsiveness
        'scrollZoom': True,  # Enable scroll zoom for better UX
        'showTips': False,  # Disable tips for performance
        'staticPlot': False,  # Keep interactive features
        'plotGlPixelRatio': 1,  # Optimize for high DPI displays
        
        # Remove unnecessary toolbar buttons for cleaner interface
        'modeBarButtonsToRemove': [
            'pan2d',
            'select2d', 
            'lasso2d',
            'zoomIn2d',
            'zoomOut2d',
            'autoScale2d',
            'resetScale2d',
            'hoverClosestCartesian',
            'hoverCompareCartesian',
            'toggleSpikelines'
        ],
        
        # Optimize image export options
        'toImageButtonOptions': {
            'format': 'png',
            'filename': 'dashboard_chart',
            'height': None,  # Use current rendered size
            'width': None,   # Use current rendered size
            'scale': 2  # High quality for export
        }
    }


def optimize_chart_layout(base_layout: Dict[str, Any]) -> Dict[str, Any]:
    """
    Optimize chart layout for better performance.
    Uses context7 best practices for Plotly layout optimization.
    
    Args:
        base_layout: Base Plotly layout configuration
    
    Returns:
        Optimized layout configuration
    """
    optimized_layout = base_layout.copy()
    
    # Performance and UX optimizations based on context7 documentation
    optimized_layout.update({
        'autosize': True,  # Enable automatic resizing
        'showlegend': True,
        'hovermode': 'closest',  # Optimize hover interactions
        'dragmode': 'zoom',  # Enable zoom by default
        'font': {'family': 'Inter, Arial, sans-serif', 'size': 12},
        'paper_bgcolor': 'rgba(0,0,0,0)',  # Transparent background
        'plot_bgcolor': 'rgba(255,255,255,1)',  # White plot area
        'margin': {'l': 50, 'r': 50, 't': 70, 'b': 50},  # Adequate margins
        
        # Axis optimizations
        'xaxis': {
            'showgrid': True,
            'gridcolor': 'rgba(128,128,128,0.2)',
            'showline': True,
            'linecolor': 'rgba(128,128,128,0.3)',
            'zeroline': False  # Remove zero line for cleaner look
        },
        'yaxis': {
            'showgrid': True,
            'gridcolor': 'rgba(128,128,128,0.2)',
            'showline': True,
            'linecolor': 'rgba(128,128,128,0.3)',
            'zeroline': False
        },
        
        # Legend optimization
        'legend': {
            'orientation': 'h',
            'yanchor': 'bottom',
            'y': -0.2,
            'xanchor': 'center',
            'x': 0.5,
            'bgcolor': 'rgba(255,255,255,0.8)',
            'bordercolor': 'rgba(0,0,0,0.2)',
            'borderwidth': 1
        }
    })
    
    return optimized_layout


def debounce_callback(delay_ms: int = 300):
    """
    Decorator for debouncing callback functions.
    
    Args:
        delay_ms: Delay in milliseconds
    
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # This would need to be implemented with clientside callbacks
            # for true debouncing in Dash
            return func(*args, **kwargs)
        return wrapper
    return decorator


def create_performance_monitor() -> html.Div:
    """
    Create a performance monitoring component (for development).
    
    Returns:
        Performance monitor HTML
    """
    return html.Div([
        html.Div(id="performance-metrics", className="d-none"),
        dcc.Interval(
            id="performance-interval",
            interval=5000,  # Update every 5 seconds
            n_intervals=0,
            disabled=True  # Enable only in development
        )
    ])


def get_lazy_loading_script() -> str:
    """
    Get JavaScript for intersection observer lazy loading.
    
    Returns:
        JavaScript code as string
    """
    return """
    // Intersection Observer for lazy loading
    window.dashLazyLoader = {
        observer: null,
        
        init: function() {
            if ('IntersectionObserver' in window) {
                this.observer = new IntersectionObserver(
                    this.handleIntersection,
                    {
                        rootMargin: '50px',
                        threshold: 0.1
                    }
                );
                
                // Observe all trigger elements
                document.querySelectorAll('.intersection-trigger').forEach(trigger => {
                    this.observer.observe(trigger);
                });
            }
        },
        
        handleIntersection: function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const componentId = entry.target.dataset.component;
                    const event = new CustomEvent('lazyLoad', {
                        detail: { componentId: componentId }
                    });
                    document.dispatchEvent(event);
                    
                    // Stop observing this element
                    window.dashLazyLoader.observer.unobserve(entry.target);
                }
            });
        }
    };
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.dashLazyLoader.init();
        });
    } else {
        window.dashLazyLoader.init();
    }
    """


def create_data_store_with_cache(store_id: str, data: Any, ttl_seconds: int = 300) -> dcc.Store:
    """
    Create a dcc.Store component with automatic cache management.
    
    Args:
        store_id: ID for the store component
        data: Data to store
        ttl_seconds: Time to live for cached data
    
    Returns:
        dcc.Store component
    """
    return dcc.Store(
        id=store_id,
        data={
            'payload': data,
            'timestamp': time.time(),
            'ttl': ttl_seconds
        },
        storage_type='session'  # Use session storage for better performance
    )


def is_cache_valid(store_data: Dict[str, Any]) -> bool:
    """
    Check if cached data is still valid.
    
    Args:
        store_data: Data from dcc.Store
    
    Returns:
        True if cache is valid, False otherwise
    """
    if not store_data or 'timestamp' not in store_data:
        return False
    
    ttl = store_data.get('ttl', 300)
    return (time.time() - store_data['timestamp']) < ttl


def get_optimized_chart_data(data, max_points: int = 1000, use_webgl: bool = True):
    """
    Optimize chart data by sampling for better performance.
    Implements context7 recommendations for large dataset handling.
    
    Args:
        data: Chart data (list or pandas DataFrame)
        max_points: Maximum number of data points
        use_webgl: Whether to recommend WebGL for large datasets
    
    Returns:
        Optimized data and rendering recommendation
    """
    if hasattr(data, '__len__') and len(data) > max_points:
        # For very large datasets, recommend WebGL rendering
        render_mode = 'webgl' if use_webgl and len(data) > 10000 else 'svg'
        
        if len(data) > 100000:  # Use aggressive sampling for very large datasets
            step = len(data) // (max_points // 2)  # More aggressive sampling
        else:
            step = len(data) // max_points
        
        if hasattr(data, 'iloc'):  # pandas DataFrame
            optimized_data = data.iloc[::step]
        else:  # list or other sequence
            optimized_data = data[::step]
            
        return optimized_data, render_mode
    
    return data, 'svg'


# Memory usage tracking (for development)
def track_memory_usage():
    """Track memory usage for performance monitoring."""
    try:
        import psutil
        process = psutil.Process()
        return {
            'memory_mb': process.memory_info().rss / 1024 / 1024,
            'memory_percent': process.memory_percent()
        }
    except ImportError:
        return {'memory_mb': 0, 'memory_percent': 0}


def create_optimized_scatter_trace(x_data, y_data, name: str, use_webgl: bool = False):
    """
    Create optimized scatter trace with WebGL support for large datasets.
    Based on context7 performance recommendations.
    
    Args:
        x_data: X-axis data
        y_data: Y-axis data
        name: Trace name
        use_webgl: Whether to use WebGL rendering
        
    Returns:
        Optimized Plotly trace
    """
    import plotly.graph_objects as go
    
    # Optimize data if needed
    optimized_data, recommended_mode = get_optimized_chart_data(
        list(zip(x_data, y_data)) if hasattr(x_data, '__len__') else [(x_data, y_data)],
        max_points=10000,
        use_webgl=use_webgl
    )
    
    # Use WebGL for large datasets (context7 recommendation)
    trace_type = go.Scattergl if recommended_mode == 'webgl' or use_webgl else go.Scatter
    
    if optimized_data != [(x_data, y_data)] and hasattr(optimized_data, '__len__'):
        # Data was optimized
        if len(optimized_data) > 0 and hasattr(optimized_data[0], '__len__'):
            x_opt = [point[0] for point in optimized_data]
            y_opt = [point[1] for point in optimized_data]
        else:
            x_opt, y_opt = x_data, y_data
    else:
        x_opt, y_opt = x_data, y_data
    
    return trace_type(
        x=x_opt,
        y=y_opt,
        mode='lines+markers',
        name=name,
        marker=dict(
            size=6,
            line=dict(width=1, color='rgba(255,255,255,0.8)')
        ),
        line=dict(width=2)
    )


def get_animation_config(duration: int = 300, redraw: bool = False):
    """
    Get optimized animation configuration.
    Based on context7 animation performance guidelines.
    
    Args:
        duration: Animation duration in milliseconds
        redraw: Whether to redraw entire plot (expensive)
        
    Returns:
        Animation configuration dict
    """
    return {
        'frame': {
            'duration': duration,
            'redraw': redraw  # False for scatter plots optimization
        },
        'transition': {
            'duration': duration,
            'easing': 'cubic-in-out'
        },
        'mode': 'immediate'
    }


def optimize_numpy_dtypes(data):
    """
    Optimize NumPy dtypes for better Plotly performance.
    Based on context7 NumPy optimization recommendations.
    
    Args:
        data: NumPy array or data structure
        
    Returns:
        Optimized data with appropriate dtypes
    """
    try:
        import numpy as np
        
        if isinstance(data, np.ndarray):
            # Use optimized dtypes as recommended by context7
            if data.dtype in [np.float64]:
                return data.astype(np.float32)  # Reduce precision for performance
            elif data.dtype in [np.int64, np.int32]:
                # Use smaller int types if possible
                if data.max() < 256 and data.min() >= 0:
                    return data.astype(np.uint8)
                elif data.max() < 32768 and data.min() >= -32768:
                    return data.astype(np.int16)
                    
        return data
    except ImportError:
        return data


def create_performance_optimized_config():
    """
    Create comprehensive performance-optimized configuration.
    Combines all context7 recommendations for maximum performance.
    
    Returns:
        Complete optimized configuration dict
    """
    return {
        # Chart configuration
        'config': optimize_plotly_config(),
        
        # Layout optimizations
        'layout_template': {
            'font': {'family': 'Inter, Arial, sans-serif', 'size': 12},
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(255,255,255,1)',
            'hovermode': 'closest',
            'showlegend': True,
            'autosize': True,
            'margin': {'l': 50, 'r': 50, 't': 70, 'b': 50}
        },
        
        # Animation settings
        'animation': get_animation_config(),
        
        # Data processing
        'max_points': 10000,
        'use_webgl_threshold': 1000,
        'sampling_strategy': 'uniform'
    }