"""
Screenshot-based PDF export functionality.
Takes actual screenshots of each dashboard tab and combines them into a PDF.
"""

import asyncio
import io
import base64
from datetime import datetime
from typing import List, Optional
from playwright.async_api import async_playwright
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from PIL import Image


class ScreenshotPDFExporter:
    """Handle screenshot-based PDF export for dashboard tabs."""
    
    def __init__(self):
        """Initialize the screenshot PDF exporter."""
        self.a4_width, self.a4_height = A4  # 595.2 x 841.89 points
        
    async def capture_tab_screenshots(
        self, 
        base_url: str = "http://localhost:8050",
        tabs: Optional[List[dict]] = None
    ) -> List[bytes]:
        """
        Capture screenshots of all dashboard tabs.
        
        Args:
            base_url: Base URL of the dashboard
            tabs: List of tab configurations
            
        Returns:
            List of screenshot image bytes
        """
        if tabs is None:
            tabs = [
                {"id": "tab-1", "name": "Accuracy Overview"},
                {"id": "tab-2", "name": "Airline Analysis"},
                {"id": "tab-3", "name": "Field Analysis"}
            ]
        
        screenshots = []
        
        async with async_playwright() as playwright:
            # Launch browser
            browser = await playwright.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={'width': 1200, 'height': 1600},  # A4-like ratio
                device_scale_factor=1.0
            )
            page = await context.new_page()
            
            try:
                # Navigate to dashboard
                await page.goto(base_url, wait_until="networkidle", timeout=30000)
                
                # Wait for initial load
                await page.wait_for_selector("#main-tabs", timeout=10000)
                await asyncio.sleep(2)  # Allow dynamic content to load
                
                for tab in tabs:
                    try:
                        print(f"📸 Capturing screenshot for {tab['name']}...")
                        
                        # Find and click on the tab using multiple selector strategies
                        tab_selectors = [
                            f"a[href='#{tab['id']}']",  # Bootstrap tabs with href
                            f".nav-link[data-value='{tab['id']}']",  # Custom data-value
                            f"button[data-bs-target='#{tab['id']}']",  # Bootstrap 5 button
                            f"[role='tab'][aria-controls='{tab['id']}']",  # ARIA tab
                            f".nav-link:has-text('{tab['name']}')",  # Text-based selector
                        ]
                        
                        tab_clicked = False
                        for selector in tab_selectors:
                            try:
                                if await page.locator(selector).count() > 0:
                                    await page.click(selector)
                                    tab_clicked = True
                                    print(f"   ✅ Clicked tab using selector: {selector}")
                                    break
                            except Exception:
                                continue
                        
                        if not tab_clicked:
                            print(f"   ⚠️  Could not find tab selector, trying to capture current view")
                            # Just take screenshot of current state
                        
                        # Wait for tab content to load
                        await page.wait_for_selector("#tab-content", timeout=5000)
                        await asyncio.sleep(3)  # Allow charts to render
                        
                        # Take screenshot of the entire page
                        screenshot_bytes = await page.screenshot(
                            full_page=True,
                            type='png'
                            # quality parameter not supported for PNG
                        )
                        
                        screenshots.append(screenshot_bytes)
                        print(f"✅ Captured {tab['name']} ({len(screenshot_bytes):,} bytes)")
                        
                    except Exception as e:
                        print(f"❌ Failed to capture {tab['name']}: {e}")
                        continue
                
            except Exception as e:
                print(f"❌ Failed to load dashboard: {e}")
                raise
                
            finally:
                await browser.close()
        
        return screenshots
    
    def create_pdf_from_screenshots(
        self, 
        screenshots: List[bytes], 
        title: str = "Dashboard Export"
    ) -> bytes:
        """
        Create a PDF from screenshot images.
        
        Args:
            screenshots: List of screenshot image bytes
            title: PDF document title
            
        Returns:
            PDF document as bytes
        """
        buffer = io.BytesIO()
        pdf_canvas = canvas.Canvas(buffer, pagesize=A4)
        
        # Set PDF metadata
        pdf_canvas.setTitle(title)
        pdf_canvas.setAuthor("Dashboard Export Tool")
        pdf_canvas.setSubject("Dashboard Screenshots")
        
        for i, screenshot_bytes in enumerate(screenshots):
            try:
                # Convert screenshot to PIL Image
                screenshot_image = Image.open(io.BytesIO(screenshot_bytes))
                
                # Calculate scaling to fit A4 while maintaining aspect ratio
                img_width, img_height = screenshot_image.size
                scale = min(self.a4_width / img_width, self.a4_height / img_height)
                
                new_width = img_width * scale * 0.95  # 95% to add margins
                new_height = img_height * scale * 0.95
                
                # Center the image on the page
                x = (self.a4_width - new_width) / 2
                y = (self.a4_height - new_height) / 2
                
                # Convert to ImageReader for ReportLab
                img_reader = ImageReader(io.BytesIO(screenshot_bytes))
                
                # Draw image on PDF
                pdf_canvas.drawImage(
                    img_reader,
                    x, y,
                    width=new_width,
                    height=new_height,
                    preserveAspectRatio=True
                )
                
                # Add page number
                pdf_canvas.setFont("Helvetica", 10)
                pdf_canvas.drawString(
                    self.a4_width - 50, 20, 
                    f"Page {i + 1}"
                )
                
                # Start new page if not the last screenshot
                if i < len(screenshots) - 1:
                    pdf_canvas.showPage()
                    
            except Exception as e:
                print(f"❌ Failed to add screenshot {i + 1} to PDF: {e}")
                continue
        
        # Finalize PDF
        pdf_canvas.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    async def export_dashboard_to_pdf(
        self, 
        base_url: str = "http://localhost:8050",
        title: str = "Dashboard Export"
    ) -> bytes:
        """
        Export entire dashboard to PDF using screenshots.
        
        Args:
            base_url: Dashboard URL
            title: PDF document title
            
        Returns:
            PDF document as bytes
        """
        try:
            print("🔄 Starting screenshot-based PDF export...")
            
            # Capture screenshots of all tabs
            screenshots = await self.capture_tab_screenshots(base_url)
            
            if not screenshots:
                raise Exception("No screenshots captured")
            
            print(f"📊 Creating PDF from {len(screenshots)} screenshots...")
            
            # Create PDF from screenshots
            pdf_bytes = self.create_pdf_from_screenshots(screenshots, title)
            
            print(f"✅ PDF export complete ({len(pdf_bytes):,} bytes)")
            return pdf_bytes
            
        except Exception as e:
            print(f"❌ PDF export failed: {e}")
            raise


# Global instance for use throughout the application
screenshot_pdf_exporter = ScreenshotPDFExporter()