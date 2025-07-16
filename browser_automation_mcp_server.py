#!/usr/bin/env python3
"""
Browser Automation MCP Server
Provides web browser control capabilities through Playwright
"""

import json
import asyncio
import sys
from datetime import datetime
from pathlib import Path
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Server instance
server = Server("browser-automation")

# Browser management
browser_instance = None
page_instance = None

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available browser automation tools"""
    return [
        types.Tool(
            name="open_browser",
            description="Open a browser window",
            inputSchema={
                "type": "object",
                "properties": {
                    "headless": {"type": "boolean", "description": "Run browser in headless mode", "default": False},
                    "browser_type": {"type": "string", "description": "Browser type", "enum": ["chromium", "firefox", "webkit"], "default": "chromium"}
                }
            }
        ),
        types.Tool(
            name="navigate_to",
            description="Navigate to a URL",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL to navigate to"}
                },
                "required": ["url"]
            }
        ),
        types.Tool(
            name="take_screenshot",
            description="Take a screenshot of the current page",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Screenshot filename", "default": "screenshot.png"}
                }
            }
        ),
        types.Tool(
            name="get_page_content",
            description="Get the text content of the current page",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        types.Tool(
            name="click_element",
            description="Click on an element",
            inputSchema={
                "type": "object", 
                "properties": {
                    "selector": {"type": "string", "description": "CSS selector for the element"}
                },
                "required": ["selector"]
            }
        ),
        types.Tool(
            name="type_text",
            description="Type text into an input field",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {"type": "string", "description": "CSS selector for the input field"},
                    "text": {"type": "string", "description": "Text to type"}
                },
                "required": ["selector", "text"]
            }
        ),
        types.Tool(
            name="close_browser",
            description="Close the browser",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls"""
    global browser_instance, page_instance
    
    try:
        if name == "open_browser":
            from playwright.async_api import async_playwright
            
            headless = arguments.get("headless", False)
            browser_type = arguments.get("browser_type", "chromium")
            
            playwright = await async_playwright().start()
            
            if browser_type == "chromium":
                browser_instance = await playwright.chromium.launch(headless=headless)
            elif browser_type == "firefox":
                browser_instance = await playwright.firefox.launch(headless=headless)
            elif browser_type == "webkit":
                browser_instance = await playwright.webkit.launch(headless=headless)
            
            page_instance = await browser_instance.new_page()
            
            return [types.TextContent(type="text", text=f"Browser opened ({browser_type}, headless={headless})")]
        
        elif name == "navigate_to":
            if not page_instance:
                return [types.TextContent(type="text", text="No browser open. Use open_browser first.")]
            
            url = arguments["url"]
            await page_instance.goto(url)
            
            return [types.TextContent(type="text", text=f"Navigated to: {url}")]
        
        elif name == "take_screenshot":
            if not page_instance:
                return [types.TextContent(type="text", text="No browser open. Use open_browser first.")]
            
            filename = arguments.get("filename", "screenshot.png")
            screenshot_path = Path.cwd() / filename
            
            await page_instance.screenshot(path=str(screenshot_path))
            
            return [types.TextContent(type="text", text=f"Screenshot saved: {screenshot_path}")]
        
        elif name == "get_page_content":
            if not page_instance:
                return [types.TextContent(type="text", text="No browser open. Use open_browser first.")]
            
            content = await page_instance.content()
            text_content = await page_instance.inner_text("body")
            
            return [types.TextContent(type="text", text=f"Page content (first 500 chars): {text_content[:500]}...")]
        
        elif name == "click_element":
            if not page_instance:
                return [types.TextContent(type="text", text="No browser open. Use open_browser first.")]
            
            selector = arguments["selector"]
            await page_instance.click(selector)
            
            return [types.TextContent(type="text", text=f"Clicked element: {selector}")]
        
        elif name == "type_text":
            if not page_instance:
                return [types.TextContent(type="text", text="No browser open. Use open_browser first.")]
            
            selector = arguments["selector"]
            text = arguments["text"]
            
            await page_instance.fill(selector, text)
            
            return [types.TextContent(type="text", text=f"Typed '{text}' into {selector}")]
        
        elif name == "close_browser":
            if browser_instance:
                await browser_instance.close()
                browser_instance = None
                page_instance = None
                
            return [types.TextContent(type="text", text="Browser closed")]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    """Run the browser automation MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="browser-automation",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())