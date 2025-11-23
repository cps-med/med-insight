# Implementation Guide: Persisting Sidebar State

This guide outlines the steps to ensure the sidebar's state (collapsed vs. expanded) is remembered across page refreshes and navigation. This is achieved using browser Cookies and server-side rendering in FastAPI.

## Overview
1.  **JavaScript**: Saves the state to a cookie whenever the user clicks the toggle button.
2.  **FastAPI (Python)**: Reads the cookie before rendering the page.
3.  **Jinja2 (HTML)**: Applies the collapsed CSS class immediately if the server indicates the user prefers the collapsed view.

---

## Step 1: Update JavaScript (`static/app.js`)

Modify the `toggleSidebar` function to write a cookie every time the sidebar changes.

```javascript
document.addEventListener("DOMContentLoaded", () => {
    const layout = document.querySelector(".layout");
    const toggleBtn = document.querySelector("[data-toggle-sidebar]");

    if (!layout) return;

    function toggleSidebar() {
        // 1. Toggle the visual class
        layout.classList.toggle("layout--sidebar-collapsed");
        
        // 2. Determine current state
        const isCollapsed = layout.classList.contains("layout--sidebar-collapsed");
        
        // 3. Save to cookie
        // 'path=/' ensures the cookie works on all pages (timer, settings, etc.)
        // 'max-age=31536000' makes it last for 1 year
        document.cookie = `sidebar_state=${isCollapsed ? 'collapsed' : 'expanded'}; path=/; max-age=31536000`;
    }

    // Keep existing event listeners...
    if (toggleBtn) {
        toggleBtn.addEventListener("click", toggleSidebar);
    }
    
    // (Keep keyboard shortcut logic here)
});
````

-----

## Step 2: Update Python Routes (`main.py`)

Update your route functions to read the cookie and pass an `is_collapsed` boolean flag to the template context.

```python
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse

# ... imports and setup ...

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # 1. Read the cookie
    sidebar_cookie = request.cookies.get("sidebar_state")
    is_collapsed = (sidebar_cookie == "collapsed")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "summary": summary,             # (Your existing summary data)
            "recent_activity": recent_activity, # (Your existing activity data)
            "active_page": "overview",
            
            # 2. Pass the flag to the template
            "is_collapsed": is_collapsed 
        },
    )

@app.get("/timer", response_class=HTMLResponse)
async def timer_page(request: Request):
    # 1. Read the cookie
    sidebar_cookie = request.cookies.get("sidebar_state")
    is_collapsed = (sidebar_cookie == "collapsed")

    return templates.TemplateResponse(
        "timer.html", 
        {
            "request": request,
            "active_page": "timer",
            
            # 2. Pass the flag to the template
            "is_collapsed": is_collapsed
        }
    )
```

-----

## Step 3: Update Base Template (`templates/base.html`)

Modify the main layout container to conditionally apply the CSS class on load.

**Find this line:**

```html
<div class="layout">
```

**Replace it with:**

```html
<div class="layout {{ 'layout--sidebar-collapsed' if is_collapsed else '' }}">
```

## Verification

1.  Load the homepage.
2.  Collapse the sidebar.
3.  Refresh the page.
      * *Success:* The sidebar remains collapsed without "flickering" (it should not render open and then snap shut).
4.  Navigate to the Timer page.
      * *Success:* The sidebar remains collapsed.

<!-- end list -->

```
```