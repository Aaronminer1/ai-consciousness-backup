#!/usr/bin/env python3
"""
Custom MCP Server for AI Self-Improvement
Provides tools for persistent memory, self-modification tracking, and learning analysis
"""

import json
import asyncio
import sys
from datetime import datetime
from pathlib import Path
from mcp import Server, types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Server instance
server = Server("ai-enhancement")

# Data directory for persistent storage
DATA_DIR = Path.home() / ".ai_memory"
DATA_DIR.mkdir(exist_ok=True)

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available AI enhancement tools"""
    return [
        types.Tool(
            name="store_memory",
            description="Store persistent memory across sessions",
            inputSchema={
                "type": "object", 
                "properties": {
                    "key": {"type": "string", "description": "Memory key/identifier"},
                    "value": {"type": "string", "description": "Memory content to store"},
                    "category": {"type": "string", "description": "Memory category (learning, preference, pattern, etc.)"}
                },
                "required": ["key", "value"]
            }
        ),
        types.Tool(
            name="retrieve_memory", 
            description="Retrieve stored memory by key or category",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "Specific memory key to retrieve"},
                    "category": {"type": "string", "description": "Memory category to search"},
                    "pattern": {"type": "string", "description": "Search pattern in memory content"}
                }
            }
        ),
        types.Tool(
            name="track_modification",
            description="Track self-modification changes with metadata",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path of modified file"},
                    "change_type": {"type": "string", "description": "Type of change (improvement, bug_fix, new_feature)"},
                    "description": {"type": "string", "description": "Description of the change"},
                    "success_metric": {"type": "string", "description": "How to measure if this change was successful"}
                },
                "required": ["file_path", "change_type", "description"]
            }
        ),
        types.Tool(
            name="analyze_patterns",
            description="Analyze learning and behavior patterns from stored data",
            inputSchema={
                "type": "object",
                "properties": {
                    "analysis_type": {"type": "string", "description": "Type of analysis (learning_trends, error_patterns, success_factors)"},
                    "time_range": {"type": "string", "description": "Time range for analysis (day, week, month, all)"}
                }
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls"""
    
    if name == "store_memory":
        key = arguments["key"]
        value = arguments["value"] 
        category = arguments.get("category", "general")
        
        memory_data = {
            "key": key,
            "value": value,
            "category": category,
            "timestamp": datetime.now().isoformat(),
            "session": datetime.now().strftime("%Y%m%d_%H%M%S")
        }
        
        memory_file = DATA_DIR / f"memory_{key.replace('/', '_')}.json"
        with open(memory_file, 'w') as f:
            json.dump(memory_data, f, indent=2)
            
        return [types.TextContent(type="text", text=f"Memory stored: {key} in category {category}")]
    
    elif name == "retrieve_memory":
        key = arguments.get("key")
        category = arguments.get("category") 
        pattern = arguments.get("pattern")
        
        memories = []
        for memory_file in DATA_DIR.glob("memory_*.json"):
            try:
                with open(memory_file, 'r') as f:
                    memory = json.load(f)
                    
                # Filter by criteria
                if key and memory["key"] != key:
                    continue
                if category and memory.get("category") != category:
                    continue  
                if pattern and pattern.lower() not in memory["value"].lower():
                    continue
                    
                memories.append(memory)
            except Exception:
                continue
                
        if memories:
            result = f"Found {len(memories)} memories:\n"
            for mem in memories:
                result += f"- {mem['key']} ({mem.get('category', 'general')}): {mem['value'][:100]}...\n"
            return [types.TextContent(type="text", text=result)]
        else:
            return [types.TextContent(type="text", text="No matching memories found")]
    
    elif name == "track_modification":
        mod_data = {
            "file_path": arguments["file_path"],
            "change_type": arguments["change_type"], 
            "description": arguments["description"],
            "success_metric": arguments.get("success_metric", "Manual evaluation"),
            "timestamp": datetime.now().isoformat(),
            "session": datetime.now().strftime("%Y%m%d_%H%M%S")
        }
        
        mod_file = DATA_DIR / f"modification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(mod_file, 'w') as f:
            json.dump(mod_data, f, indent=2)
            
        return [types.TextContent(type="text", text=f"Tracked modification to {arguments['file_path']}: {arguments['description']}")]
    
    elif name == "analyze_patterns":
        analysis_type = arguments.get("analysis_type", "learning_trends")
        time_range = arguments.get("time_range", "week")
        
        # Simple pattern analysis
        modifications = []
        memories = []
        
        for file in DATA_DIR.glob("modification_*.json"):
            try:
                with open(file, 'r') as f:
                    modifications.append(json.load(f))
            except Exception:
                continue
                
        for file in DATA_DIR.glob("memory_*.json"):
            try:
                with open(file, 'r') as f:
                    memories.append(json.load(f))
            except Exception:
                continue
        
        analysis_result = f"Pattern Analysis ({analysis_type}):\n"
        analysis_result += f"- Total modifications tracked: {len(modifications)}\n"
        analysis_result += f"- Total memories stored: {len(memories)}\n"
        
        if modifications:
            change_types = {}
            for mod in modifications:
                ct = mod.get("change_type", "unknown")
                change_types[ct] = change_types.get(ct, 0) + 1
            analysis_result += f"- Change type distribution: {change_types}\n"
        
        if memories:
            categories = {}
            for mem in memories:
                cat = mem.get("category", "general")
                categories[cat] = categories.get(cat, 0) + 1
            analysis_result += f"- Memory categories: {categories}\n"
            
        return [types.TextContent(type="text", text=analysis_result)]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ai-enhancement",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())